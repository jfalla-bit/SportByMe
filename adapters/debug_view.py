from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from core.models import UserModel


@csrf_exempt
def debug_login(request):
    """
    Vista temporal de diagnóstico. Eliminar después de resolver el problema.
    GET  /auth/debug/         → muestra usuarios en BD
    POST /auth/debug/ con username + password → muestra resultado de authenticate()
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Buscar el objeto usuario
        user_obj = UserModel.objects.filter(username__iexact=username).first()

        if user_obj is None:
            return JsonResponse({
                'error': f'Usuario "{username}" no existe en la BD',
                'usuarios_existentes': list(
                    UserModel.objects.values('username', 'email', 'role', 'is_active', 'is_superuser')
                ),
            })

        # Verificar password manualmente
        password_ok = user_obj.check_password(password)

        # Intentar authenticate
        try:
            user = authenticate(request, username=user_obj.username, password=password)
            auth_result = str(user)
        except Exception as e:
            auth_result = f'EXCEPCION: {e}'

        return JsonResponse({
            'usuario_encontrado': user_obj.username,
            'email': user_obj.email,
            'role': user_obj.role,
            'is_active': user_obj.is_active,
            'is_superuser': user_obj.is_superuser,
            'password_check_password': password_ok,
            'authenticate_result': auth_result,
        })

    # GET: mostrar todos los usuarios
    usuarios = list(
        UserModel.objects.values('id', 'username', 'email', 'role', 'is_active', 'is_superuser')
    )
    return JsonResponse({'usuarios': usuarios, 'total': len(usuarios)})
