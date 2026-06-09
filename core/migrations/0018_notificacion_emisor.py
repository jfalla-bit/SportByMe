import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_observacion_deportista'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='emisor',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='notificaciones_enviadas',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
