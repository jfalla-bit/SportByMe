from django.db import models
from core.models import Pago, UserModel


class WompiTransaccion(models.Model):
    """Registra cada transacción iniciada con Wompi para un Pago existente."""
    ESTADO_CHOICES = [
        ('PENDING',   'Pendiente'),
        ('APPROVED',  'Aprobado'),
        ('DECLINED',  'Rechazado'),
        ('VOIDED',    'Anulado'),
        ('ERROR',     'Error'),
    ]
    pago             = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='wompi_transacciones')
    pagador          = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='wompi_transacciones')
    referencia       = models.CharField(max_length=100, unique=True)
    wompi_id         = models.CharField(max_length=100, blank=True)
    estado           = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDING')
    monto_en_centavos = models.PositiveBigIntegerField()
    metodo           = models.CharField(max_length=20, blank=True)
    creado           = models.DateTimeField(auto_now_add=True)
    actualizado      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wompi_transacciones'
        ordering = ['-creado']

    def __str__(self):
        return f'{self.referencia} — {self.estado}'
