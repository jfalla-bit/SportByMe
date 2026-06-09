from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_acudiente_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoEntrenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveIntegerField(help_text='Mes (1-12)')),
                ('anio', models.PositiveIntegerField(help_text='Año')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], default='pendiente', max_length=10)),
                ('metodo_pago', models.CharField(blank=True, choices=[('efectivo', 'Efectivo'), ('transferencia', 'Transferencia'), ('tarjeta', 'Tarjeta'), ('otro', 'Otro')], default='', max_length=20)),
                ('descripcion', models.CharField(blank=True, max_length=300)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('entrenador', models.ForeignKey(limit_choices_to={'role': 'entrenador'}, on_delete=django.db.models.deletion.CASCADE, related_name='pagos_nomina', to=settings.AUTH_USER_MODEL)),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nominas_registradas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pagos_entrenador',
                'ordering': ['-anio', '-mes'],
                'unique_together': {('entrenador', 'mes', 'anio')},
            },
        ),
    ]
