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
            user.set_password(password)
            user.email        = email
            user.role         = 'administrador'
            user.is_superuser = True
            user.is_staff     = True
            user.is_active    = True
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Usuario "{username}" actualizado — password reseteado, role=administrador'
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
