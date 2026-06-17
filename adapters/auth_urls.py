from django.urls import path
from .auth_views import (
    login_view, logout_view, dashboard_view, profile_view,
    signup_view, pendiente_view,
    password_reset_view, password_reset_confirm_view,
)
from .debug_view import debug_login

app_name = 'auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('pendiente/', pendiente_view, name='pendiente'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('debug/', debug_login, name='debug_login'),
]