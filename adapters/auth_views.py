from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from core.models import UserModel


# ─── Mapa de roles a URLs de destino ───────────────────────────────────────────
ROLE_URLS = {
    'administrador': '/admin-dashboard/',
    'entrenador':    '/entrenador-dashboard/',
    'deportista':    '/deportista-dashboard/',
    'acudiente':     '/acudiente-dashboard/',
    'pendiente':     '/auth/pendiente/',
}


def _redirect_to(url):
    """Devuelve una respuesta HTML que redirige inmediatamente sin usar reverse()"""
    return render_redirect(url)


def render_redirect(url):
    """Renderiza una página de redirección simple usando meta refresh"""
    from django.http import HttpResponse
    return HttpResponse(
        f'<!DOCTYPE html><html><head>'
        f'<meta http-equiv="refresh" content="0;url={url}">'
        f'</head><body></body></html>'
    )


# ─── LOGIN ──────────────────────────────────────────────────────────────────────

@csrf_protect
@never_cache
def login_view(request):
    """
    Vista de login.
    - Acepta EMAIL o USERNAME como identificador.
    - Redirige según el rol del usuario.
    - Muestra mensajes claros de error.
    """
    # Si ya está autenticado, redirigir a su dashboard
    if request.user.is_authenticated:
        url = ROLE_URLS.get(request.user.role, '/auth/login/')
        return render_redirect(url)

    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '').strip()

        # Validar campos vacíos
        if not identifier or not password:
            messages.error(request, 'El correo y la contraseña son obligatorios.')
            return render(request, 'auth/login.html', {'email': identifier})

        # Buscar usuario por email o username
        user_obj = None
        if '@' in identifier:
            user_obj = UserModel.objects.filter(email__iexact=identifier).first()
        else:
            user_obj = UserModel.objects.filter(username__iexact=identifier).first()

        if user_obj is None:
            messages.error(request, 'No existe una cuenta con ese correo.')
            return render(request, 'auth/login.html', {'email': identifier})

        # Autenticar con username real del objeto encontrado
        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            messages.error(request, 'Contraseña incorrecta. Intenta de nuevo.')
            return render(request, 'auth/login.html', {'email': identifier})

        if not user.is_active:
            messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
            return render(request, 'auth/login.html', {'email': identifier})

        # Login exitoso
        login(request, user)
        url = ROLE_URLS.get(user.role, '/auth/login/')
        return render_redirect(url)

    return render(request, 'auth/login.html')


# ─── SIGNUP ─────────────────────────────────────────────────────────────────────

@csrf_protect
@never_cache
def signup_view(request):
    """
    Vista de registro de nueva cuenta.
    - Crea usuarios con rol 'deportista' por defecto.
    - Valida email único, username único y contraseñas coincidentes.
    """
    if request.user.is_authenticated:
        url = ROLE_URLS.get(request.user.role, '/auth/login/')
        return render_redirect(url)

    if request.method == 'POST':
        email      = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        password1  = request.POST.get('password1', '').strip()
        password2  = request.POST.get('password2', '').strip()
        birth_date_raw = request.POST.get('birth_date', '').strip()

        birth_date = None
        if birth_date_raw:
            try:
                from datetime import date as _date
                birth_date = _date.fromisoformat(birth_date_raw)
            except ValueError:
                birth_date = None

        form_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date_raw,
        }

        # Validaciones
        if not all([email, password1, password2]):
            messages.error(request, 'El correo y las contraseñas son obligatorios.')
            return render(request, 'auth/signup.html', form_data)

        if not birth_date:
            messages.error(request, 'La fecha de nacimiento es obligatoria y debe ser válida.')
            return render(request, 'auth/signup.html', form_data)

        if not request.POST.get('acepta_politica'):
            messages.error(request, 'Debes aceptar la política de tratamiento de datos personales para registrarte.')
            return render(request, 'auth/signup.html', form_data)

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'auth/signup.html', form_data)

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'auth/signup.html', form_data)

        # Validar criterios de contraseña
        import re
        if not re.search(r'[A-Z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
            return render(request, 'auth/signup.html', form_data)
        if not re.search(r'[a-z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula.')
            return render(request, 'auth/signup.html', form_data)
        if not re.search(r'[0-9]', password1):
            messages.error(request, 'La contraseña debe contener al menos un número.')
            return render(request, 'auth/signup.html', form_data)
        if not re.search(r'[^A-Za-z0-9]', password1):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial (ej: @, #, $, !).')
            return render(request, 'auth/signup.html', form_data)

        if UserModel.objects.filter(email__iexact=email).exists():
            messages.error(request, f'El correo "{email}" ya está registrado.')
            return render(request, 'auth/signup.html', form_data)

        # Generar username automático con formato usuario001, usuario002...
        count = UserModel.objects.filter(role='pendiente').count() + 1
        username = f"usuario{count:03d}"
        while UserModel.objects.filter(username=username).exists():
            count += 1
            username = f"usuario{count:03d}"

        # Crear usuario con rol pendiente hasta que el admin asigne uno
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            role='pendiente',
            birth_date=birth_date,
        )

        # Redirigir al login con mensaje de éxito (sin login automático)
        messages.success(request, f'¡Cuenta creada exitosamente! Ya puedes iniciar sesión, {first_name or username}.')
        return render(request, 'auth/login.html', {'email': email})

    return render(request, 'auth/signup.html')


# ─── LOGOUT ─────────────────────────────────────────────────────────────────────

@login_required
def logout_view(request):
    """Cierra la sesión y redirige al login"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return render(request, 'auth/login.html')


# ─── DASHBOARD GENÉRICO ─────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """Redirige al dashboard según el rol del usuario"""
    url = ROLE_URLS.get(request.user.role, '/auth/login/')
    return render_redirect(url)


# ─── PERFIL ─────────────────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    return render(request, 'auth/profile.html', {'user': request.user})


# ─── PENDIENTE ───────────────────────────────────────────────────────────────────────────

@login_required
def pendiente_view(request):
    """Vista para usuarios con rol pendiente esperando asignación de rol por el admin"""
    if request.user.role != 'pendiente':
        url = ROLE_URLS.get(request.user.role, '/auth/login/')
        return render_redirect(url)
    return render(request, 'auth/pendiente.html')


# ─── RECUPERAR CONTRASEÑA ────────────────────────────────────────────────────────

@csrf_protect
@never_cache
def password_reset_view(request):
    """
    Paso 1: El usuario ingresa su correo.
    Se genera un token y se envía el enlace por email.
    Funciona para todos los roles.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'Ingresa tu correo electrónico.')
            return render(request, 'auth/password_reset.html')

        user_obj = UserModel.objects.filter(email__iexact=email).first()

        # Siempre mostrar el mismo mensaje para no revelar si el email existe
        if user_obj:
            uid   = urlsafe_base64_encode(force_bytes(user_obj.pk))
            token = default_token_generator.make_token(user_obj)
            link  = f"{request.scheme}://{request.get_host()}/auth/password-reset/{uid}/{token}/"

            try:
                send_mail(
                    subject='Recuperación de contraseña - Sistema Deportivo',
                    message=(
                        f'Hola {user_obj.first_name or user_obj.username},\n\n'
                        f'Recibimos una solicitud para restablecer tu contraseña.\n'
                        f'Hacé clic en el siguiente enlace (válido por 24 horas):\n\n'
                        f'{link}\n\n'
                        f'Si no solicitaste esto, ignorá este mensaje.\n\n'
                        f'Sistema Deportivo'
                    ),
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_obj.email],
                    fail_silently=False,
                )
            except Exception:
                messages.error(request, 'No se pudo enviar el correo. Contactá al administrador.')
                return render(request, 'auth/password_reset.html', {'email': email})

        messages.success(request, 'Si ese correo está registrado, recibirás un enlace en breve.')
        return render(request, 'auth/login.html')

    return render(request, 'auth/password_reset.html')


@csrf_protect
@never_cache
def password_reset_confirm_view(request, uidb64, token):
    """
    Paso 2: El usuario llega desde el enlace del email.
    Valida el token y permite ingresar la nueva contraseña.
    """
    import re

    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except Exception:
        user = None

    token_valido = user is not None and default_token_generator.check_token(user, token)

    if not token_valido:
        messages.error(request, 'El enlace es inválido o ya expiró. Solicitá uno nuevo.')
        return render(request, 'auth/login.html')

    if request.method == 'POST':
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        errores = []
        if not password1 or not password2:
            errores.append('Ambas contraseñas son obligatorias.')
        elif password1 != password2:
            errores.append('Las contraseñas no coinciden.')
        elif len(password1) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres.')
        elif not re.search(r'[A-Z]', password1):
            errores.append('Debe contener al menos una letra mayúscula.')
        elif not re.search(r'[a-z]', password1):
            errores.append('Debe contener al menos una letra minúscula.')
        elif not re.search(r'[0-9]', password1):
            errores.append('Debe contener al menos un número.')
        elif not re.search(r'[^A-Za-z0-9]', password1):
            errores.append('Debe contener al menos un carácter especial (ej: @, #, $, !).')

        if errores:
            for e in errores:
                messages.error(request, e)
            return render(request, 'auth/password_reset_confirm.html', {
                'uidb64': uidb64, 'token': token
            })

        user.set_password(password1)
        user.save()
        messages.success(request, '¡Contraseña actualizada correctamente! Ya podés iniciar sesión.')
        return render(request, 'auth/login.html')

    return render(request, 'auth/password_reset_confirm.html', {
        'uidb64': uidb64, 'token': token
    })
