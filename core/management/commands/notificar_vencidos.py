from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Pago, Notificacion


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        total = 0

        # 1. Marcar vencidos
        Pago.marcar_vencidos()

        # 2. Notificar pagos recién vencidos (vencieron hoy)
        vencidos_hoy = Pago.objects.filter(
            estado='vencido',
            fecha_vencimiento=hoy,
        ).select_related('jugador__usuario')

        for pago in vencidos_hoy:
            usuario = pago.jugador.usuario
            ya_notificado = Notificacion.objects.filter(
                usuario=usuario,
                asunto__startswith='⚠️ Pago vencido',
                creado__date=hoy,
            ).filter(mensaje__contains=pago.descripcion).exists()

            if not ya_notificado:
                Notificacion.objects.create(
                    usuario=usuario,
                    asunto='⚠️ Pago vencido',
                    mensaje=(
                        f'Tu pago "{pago.descripcion}" por ${pago.monto} '
                        f'venció el {pago.fecha_vencimiento.strftime("%d/%m/%Y")}. '
                        f'Por favor regulariza tu situación lo antes posible.'
                    ),
                )
                total += 1

        # 3. Notificar pagos próximos a vencer (en 3 días)
        en_3_dias = hoy + timedelta(days=3)
        proximos = Pago.objects.filter(
            estado='pendiente',
            fecha_vencimiento=en_3_dias,
        ).select_related('jugador__usuario')

        for pago in proximos:
            usuario = pago.jugador.usuario
            ya_notificado = Notificacion.objects.filter(
                usuario=usuario,
                asunto__startswith='🔔 Pago próximo a vencer',
                creado__date=hoy,
            ).filter(mensaje__contains=pago.descripcion).exists()

            if not ya_notificado:
                Notificacion.objects.create(
                    usuario=usuario,
                    asunto='🔔 Pago próximo a vencer',
                    mensaje=(
                        f'Tu pago "{pago.descripcion}" por ${pago.monto} '
                        f'vence el {pago.fecha_vencimiento.strftime("%d/%m/%Y")} '
                        f'(en 3 días). Recuerda realizar el pago a tiempo.'
                    ),
                )
                total += 1

        self.stdout.write(f'Notificaciones generadas: {total}')
