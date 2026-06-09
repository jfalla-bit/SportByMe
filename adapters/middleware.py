from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class NoCacheMiddleware(MiddlewareMixin):
    """
    Agrega headers de no-cache en todas las respuestas.
    Evita que el navegador muestre páginas protegidas al presionar "Atrás" tras cerrar sesión.
    """
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class RoleValidationMiddleware(MiddlewareMixin):
    """
    Middleware opcional para validación global de roles
    """
    
    # URLs que requieren roles específicos
    ROLE_PROTECTED_URLS = {
        '/auth/admin/': 'administrador',
        '/auth/entrenador/': 'entrenador', 
        '/auth/deportista/': 'deportista',
        '/api/users/': 'administrador',  # Solo admin puede gestionar usuarios
    }
    
    # URLs que no requieren autenticación
    EXEMPT_URLS = [
        '/auth/login/',
        '/admin/',
        '/',
    ]
    
    def process_request(self, request):
        # Saltar validación para URLs exentas
        if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return None
        
        # Saltar si el usuario no está autenticado (Django auth se encarga)
        if not request.user.is_authenticated:
            return None
        
        # Verificar si la URL requiere un rol específico
        for url_pattern, required_role in self.ROLE_PROTECTED_URLS.items():
            if request.path.startswith(url_pattern):
                if request.user.role != required_role:
                    messages.error(request, f'Acceso denegado. Se requiere rol: {required_role}')
                    return redirect('auth:dashboard')
        
        return None