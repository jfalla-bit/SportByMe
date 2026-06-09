import hashlib
import hmac
import json
import uuid

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from core.models import Finanza, Notificacion, Pago
from .models import WompiTransaccion


def _firma_integridad(referencia, monto_centavos, moneda='COP'):
    """Genera la firma SHA256 requerida por Wompi para el widget."""
    secreto = getattr(settings, 'WOMPI_INTEGRITY_SECRET', settings.WOMPI_EVENTS_SECRET)
    cadena = f'{referencia}{monto_centavos}{moneda}{secreto}'
    return hashlib.sha256(cadena.encode()).hexdigest()


def _puede_pagar(user, pago):
    """Verifica que el usuario tenga permiso para pagar este pago."""
    from core.views import _deportista_es_mayor_de_edad
    if user.role == 'deportista':
        try:
            return pago.jugador == user.jugador and _deportista_es_mayor_de_edad(user)
        except Exception:
            return False
    if user.role == 'acudiente':
        try:
            from core.models import Acudiente
            return Acudiente.objects.filter(usuario=user, jugador=pago.jugador).exists()
        except Exception:
            return False
    return False


@login_required
def iniciar_pago(request, pago_id):
    """Muestra el widget de Wompi para pagar un Pago pendiente."""
    pago = get_object_or_404(Pago, id=pago_id)

    if not _puede_pagar(request.user, pago):
        return render(request, 'payments/error.html', {
            'mensaje': 'No tienes permiso para pagar este cobro.'
        })

    if pago.estado == 'pagado':
        return render(request, 'payments/error.html', {
            'mensaje': 'Este pago ya fue procesado.'
        })

    referencia     = f'PAG-{pago.id}-{uuid.uuid4().hex[:8].upper()}'
    monto_centavos = int(pago.monto * 100)

    WompiTransaccion.objects.create(
        pago=pago,
        pagador=request.user,
        referencia=referencia,
        monto_en_centavos=monto_centavos,
    )

    if request.user.role == 'acudiente':
        redirect_url = request.build_absolute_uri('/payments/retorno/')
    else:
        redirect_url = request.build_absolute_uri('/payments/retorno/')

    return render(request, 'payments/checkout.html', {
        'pago':           pago,
        'referencia':     referencia,
        'monto_centavos': monto_centavos,
        'public_key':     settings.WOMPI_PUBLIC_KEY,
        'redirect_url':   redirect_url,
        'descripcion':    pago.descripcion,
        'email':          request.user.email,
        'firma':          _firma_integridad(referencia, monto_centavos),
    })


@login_required
def retorno_pago(request):
    """Wompi redirige aquí tras el pago. Consulta el estado real y muestra resultado."""
    referencia = request.GET.get('id') or request.GET.get('reference', '')

    transaccion = (
        WompiTransaccion.objects.filter(wompi_id=referencia).first()
        or WompiTransaccion.objects.filter(referencia=referencia).first()
    )
    if not transaccion:
        # Wompi también puede enviar el transaction id directamente
        wompi_tx_id = request.GET.get('id', '')
        transaccion = WompiTransaccion.objects.filter(wompi_id=wompi_tx_id).first()
    if not transaccion:
        return redirect('/deportista/pagos/')

    _actualizar_desde_wompi(transaccion)

    return render(request, 'payments/resultado.html', {
        'exito':       transaccion.estado == 'APPROVED',
        'pago':        transaccion.pago,
        'transaccion': transaccion,
    })


@csrf_exempt
def webhook_wompi(request):
    """Recibe eventos de Wompi y actualiza el estado del Pago."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    body      = request.body
    firma     = request.headers.get('X-Event-Checksum', '')
    esperada  = hmac.new(
        settings.WOMPI_EVENTS_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(esperada, firma):
        return HttpResponse(status=401)

    try:
        data = json.loads(body)
    except Exception:
        return HttpResponse(status=400)

    if data.get('event') != 'transaction.updated':
        return HttpResponse(status=200)

    tx         = data.get('data', {}).get('transaction', {})
    wompi_id   = tx.get('id', '')
    referencia = tx.get('reference', '')
    estado_w   = tx.get('status', '')
    metodo     = tx.get('payment_method_type', '')

    transaccion = (
        WompiTransaccion.objects.filter(wompi_id=wompi_id).first()
        or WompiTransaccion.objects.filter(referencia=referencia).first()
    )
    if not transaccion:
        return HttpResponse(status=200)

    transaccion.wompi_id = wompi_id
    transaccion.estado   = estado_w
    transaccion.metodo   = metodo
    transaccion.save()

    if estado_w == 'APPROVED':
        _confirmar_pago(transaccion)

    return HttpResponse(status=200)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _actualizar_desde_wompi(transaccion):
    """Consulta el estado actual de la transacción en la API de Wompi."""
    try:
        headers = {'Authorization': f'Bearer {settings.WOMPI_PRIVATE_KEY}'}
        if transaccion.wompi_id:
            url = f'{settings.WOMPI_API_URL}/transactions/{transaccion.wompi_id}'
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                tx = resp.json().get('data', {})
        else:
            url = f'{settings.WOMPI_API_URL}/transactions?reference={transaccion.referencia}'
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                lista = resp.json().get('data', [])
                tx = lista[0] if lista else {}
            else:
                return

        transaccion.wompi_id = tx.get('id', transaccion.wompi_id)
        transaccion.estado   = tx.get('status', transaccion.estado)
        transaccion.metodo   = tx.get('payment_method_type', transaccion.metodo)
        transaccion.save()

        if transaccion.estado == 'APPROVED':
            _confirmar_pago(transaccion)
    except Exception:
        pass


def _confirmar_pago(transaccion):
    """Marca el Pago como pagado y genera el ingreso en Finanzas."""
    pago = transaccion.pago
    if pago.estado == 'pagado':
        return

    metodo_display = 'tarjeta' if 'CARD' in transaccion.metodo.upper() else 'transferencia'
    pago.estado      = 'pagado'
    pago.fecha_pago  = timezone.now().date()
    pago.metodo_pago = metodo_display
    pago.save()

    concepto_cat = {
        'cuota_mensual': 'cuota',
        'inscripcion':   'otro',
        'equipamiento':  'equipamiento',
        'torneo':        'otro',
        'otro':          'otro',
    }
    if not Finanza.objects.filter(pago=pago).exists():
        Finanza.objects.create(
            tipo='ingreso',
            categoria=concepto_cat.get(pago.concepto, 'otro'),
            descripcion=f'Wompi: {pago.descripcion} — {pago.jugador.usuario.get_full_name() or pago.jugador.usuario.username}',
            monto=pago.monto,
            fecha=pago.fecha_pago,
            registrado_por=None,
            pago=pago,
        )

    Notificacion.objects.create(
        usuario=pago.jugador.usuario,
        asunto=f'Pago confirmado: {pago.descripcion}',
        mensaje=(
            f'Tu pago fue procesado exitosamente.\n\n'
            f'Concepto: {pago.get_concepto_display()}\n'
            f'Monto:    ${pago.monto}\n'
            f'Fecha:    {pago.fecha_pago.strftime("%d/%m/%Y")}\n'
            f'Método:   Wompi ({transaccion.metodo})'
        ),
        emisor=None,
    )
