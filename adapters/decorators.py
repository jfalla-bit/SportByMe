from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(required_role):
    """
    Decorador que requiere un rol específico para acceder a la vista
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_active:
                messages.error(request, 'Tu cuenta está desactivada.')
                return redirect('login')
            
            if request.user.role != required_role:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                raise PermissionDenied("No tienes permisos para acceder a esta página.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorador que requiere rol de administrador
    """
    return role_required('administrador')(view_func)

def entrenador_required(view_func):
    """
    Decorador que requiere rol de entrenador
    """
    return role_required('entrenador')(view_func)

def deportista_required(view_func):
    """
    Decorador que requiere rol de deportista
    """
    return role_required('deportista')(view_func)

def admin_or_entrenador_required(view_func):
    """
    Decorador que permite acceso a administradores y entrenadores
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada.')
            return redirect('login')
        
        if request.user.role not in ['administrador', 'entrenador']:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            raise PermissionDenied("No tienes permisos para acceder a esta página.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view