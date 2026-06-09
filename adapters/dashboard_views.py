from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, entrenador_required, deportista_required
from core.models import UserModel

@admin_required
def admin_dashboard(request):
    """
    Dashboard para administradores
    """
    # Estadísticas para el admin
    total_users = UserModel.objects.count()
    total_admins = UserModel.objects.filter(role='administrador').count()
    total_entrenadores = UserModel.objects.filter(role='entrenador').count()
    total_deportistas = UserModel.objects.filter(role='deportista').count()
    
    context = {
        'user': request.user,
        'role': 'Administrador',
        'total_users': total_users,
        'total_admins': total_admins,
        'total_entrenadores': total_entrenadores,
        'total_deportistas': total_deportistas,
        'permissions': [
            'Gestión total de usuarios',
            'Reportes y configuración del sistema',
            'Administración de equipos y torneos',
            'Control de entrenadores y deportistas'
        ],
        'quick_actions': [
            {'name': 'Gestionar Usuarios', 'url': 'auth:manage_users', 'icon': 'fas fa-users'},
            {'name': 'Ver Reportes', 'url': '#', 'icon': 'fas fa-chart-bar'},
            {'name': 'Configuración', 'url': '#', 'icon': 'fas fa-cog'},
            {'name': 'Respaldos', 'url': '#', 'icon': 'fas fa-database'}
        ]
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

@entrenador_required
def entrenador_dashboard(request):
    """
    Dashboard para entrenadores
    """
    context = {
        'user': request.user,
        'role': 'Entrenador',
        'permissions': [
            'Creación de rutinas de entrenamiento',
            'Seguimiento de deportistas',
            'Asignación de ejercicios',
            'Gestión de equipos asignados'
        ],
        'quick_actions': [
            {'name': 'Mis Equipos', 'url': '#', 'icon': 'fas fa-users-cog'},
            {'name': 'Crear Entrenamiento', 'url': '#', 'icon': 'fas fa-plus-circle'},
            {'name': 'Ver Deportistas', 'url': '#', 'icon': 'fas fa-running'},
            {'name': 'Calendario', 'url': '#', 'icon': 'fas fa-calendar-alt'}
        ],
        'recent_activities': [
            'Entrenamiento creado para Equipo A',
            'Nuevo deportista asignado',
            'Rutina actualizada para Juan Pérez'
        ]
    }
    return render(request, 'dashboards/entrenador_dashboard.html', context)

@deportista_required
def deportista_dashboard(request):
    """
    Dashboard para deportistas
    """
    context = {
        'user': request.user,
        'role': 'Deportista',
        'permissions': [
            'Visualización de perfil personal',
            'Rutinas asignadas',
            'Registro de progreso',
            'Historial de entrenamientos'
        ],
        'quick_actions': [
            {'name': 'Mi Perfil', 'url': '#', 'icon': 'fas fa-user'},
            {'name': 'Mis Rutinas', 'url': '#', 'icon': 'fas fa-dumbbell'},
            {'name': 'Progreso', 'url': '#', 'icon': 'fas fa-chart-line'},
            {'name': 'Calendario', 'url': '#', 'icon': 'fas fa-calendar'}
        ],
        'upcoming_trainings': [
            {'date': 'Hoy 16:00', 'activity': 'Entrenamiento de fuerza'},
            {'date': 'Mañana 18:00', 'activity': 'Cardio y resistencia'},
            {'date': 'Viernes 17:00', 'activity': 'Técnica y táctica'}
        ]
    }
    return render(request, 'dashboards/deportista_dashboard.html', context)