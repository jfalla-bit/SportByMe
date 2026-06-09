from django.urls import path
from . import views

urlpatterns = [
    path('pagar/<int:pago_id>/', views.iniciar_pago, name='wompi_iniciar'),
    path('retorno/', views.retorno_pago, name='wompi_retorno'),
    path('webhook/', views.webhook_wompi, name='wompi_webhook'),
]
