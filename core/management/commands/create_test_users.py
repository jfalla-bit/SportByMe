from django.core.management.base import BaseCommand
from core.models import UserModel

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para cada rol'

    def handle(self, *args, **options):
        # Crear administrador
        if not UserModel.objects.filter(username='admin').exists():
            admin = UserModel.objects.create_user(
                username='admin',
                email='admin@deportes.com',
                password='admin123',
                first_name='Admin',
                last_name='Sistema',
                role='administrador'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Usuario administrador creado: {admin.username}')
            )

        # Crear entrenador
        if not UserModel.objects.filter(username='entrenador').exists():
            entrenador = UserModel.objects.create_user(
                username='entrenador',
                email='entrenador@deportes.com',
                password='entrenador123',
                first_name='Carlos',
                last_name='Entrenador',
                role='entrenador'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Usuario entrenador creado: {entrenador.username}')
            )

        # Crear deportista
        if not UserModel.objects.filter(username='deportista').exists():
            deportista = UserModel.objects.create_user(
                username='deportista',
                email='deportista@deportes.com',
                password='deportista123',
                first_name='Juan',
                last_name='Deportista',
                role='deportista'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Usuario deportista creado: {deportista.username}')
            )

        self.stdout.write(
            self.style.SUCCESS('Usuarios de prueba creados exitosamente!')
        )