from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_finanza_pago_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='role',
            field=models.CharField(
                choices=[
                    ('administrador', 'Administrador'),
                    ('entrenador', 'Entrenador'),
                    ('deportista', 'Deportista'),
                    ('pendiente', 'Pendiente'),
                ],
                default='deportista',
                max_length=20,
            ),
        ),
    ]
