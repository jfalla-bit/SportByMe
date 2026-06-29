from django.test import TestCase, Client
from django.urls import reverse
from core.models import UserModel


class CrearUsuarioIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Administrador que realizará la creación
        self.admin = UserModel.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="Admin123*"
        )

        self.client.force_login(self.admin)

    def test_crear_usuario(self):

        respuesta = self.client.post(
            reverse("usuario_crear"),
            {
                "email": "nuevo@test.com",
                "password": "Password123*",
                "first_name": "Julian",
                "last_name": "Falla",
                "documento": "1234567890",
                "phone": "3001234567",
                "birth_date": "2002-05-20",
                "role": "deportista",
            },
            follow=True
        )

        self.assertEqual(respuesta.status_code, 200)

        self.assertTrue(
            UserModel.objects.filter(
                email="nuevo@test.com"
            ).exists()
        )