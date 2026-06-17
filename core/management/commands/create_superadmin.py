from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea el superusuario administrador para producción con role=administrador'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email    = 'admin@sportbyme.com'
        password = 'Admin2024!'

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Asegurar que tenga role correcto aunque ya exista
            changed = False
            if user.role != 'administrador':
                user.role = 'administrador'
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario "{username}" actualizado: role=administrador, is_superuser=True'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Usuario "{username}" ya existe y está configurado correctamente.'
                ))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='administrador',
        )
        self.stdout.write(self.style.SUCCESS(
            f'Superadmin creado — username: {username} / password: {password}'
        ))
