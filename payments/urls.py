from django.urls import path
from . import views

urlpatterns = [
    path('pagar/<int:pago_id>/', views.iniciar_pago, name='wompi_iniciar'),
    path('retorno/', views.retorno_pago, name='wompi_retorno'),
    path('webhook/', views.webhook_wompi, name='wompi_webhook'),
    path('pagar-nomina/<int:nomina_id>/', views.iniciar_pago_nomina, name='wompi_nomina'),
    path('retorno-nomina/', views.retorno_pago_nomina, name='wompi_retorno_nomina'),
]
