from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect

class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin base que requiere un rol específico
    """
    required_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada.')
            return redirect('login')
        
        if self.required_role and request.user.role != self.required_role:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            raise PermissionDenied("No tienes permisos para acceder a esta página.")
        
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin que requiere rol de administrador
    """
    required_role = 'administrador'

class EntrenadorRequiredMixin(RoleRequiredMixin):
    """
    Mixin que requiere rol de entrenador
    """
    required_role = 'entrenador'

class DeportistaRequiredMixin(RoleRequiredMixin):
    """
    Mixin que requiere rol de deportista
    """
    required_role = 'deportista'

class AdminOrEntrenadorMixin(LoginRequiredMixin):
    """
    Mixin que permite acceso a administradores y entrenadores
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_active:
            messages.error(request, 'Tu cuenta está desactivada.')
            return redirect('login')
        
        if request.user.role not in ['administrador', 'entrenador']:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            raise PermissionDenied("No tienes permisos para acceder a esta página.")
        
        return super().dispatch(request, *args, **kwargs)