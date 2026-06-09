from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0021_pagoentrenador'),
    ]

    operations = [
        migrations.CreateModel(
            name='WompiTransaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=100, unique=True)),
                ('wompi_id', models.CharField(blank=True, max_length=100)),
                ('estado', models.CharField(choices=[('PENDING', 'Pendiente'), ('APPROVED', 'Aprobado'), ('DECLINED', 'Rechazado'), ('VOIDED', 'Anulado'), ('ERROR', 'Error')], default='PENDING', max_length=10)),
                ('monto_en_centavos', models.PositiveBigIntegerField()),
                ('metodo', models.CharField(blank=True, max_length=20)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wompi_transacciones', to='core.pago')),
                ('pagador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wompi_transacciones', to='core.usermodel')),
            ],
            options={
                'db_table': 'wompi_transacciones',
                'ordering': ['-creado'],
            },
        ),
    ]
