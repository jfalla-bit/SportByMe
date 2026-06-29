from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='julian',
            email='julian@gmail.com',
            password='Contraseña1*'
        )

    def test_login_correcto(self):
        response = self.client.post(
            reverse('auth:login'),
            {
                'email': 'julian@gmail.com',
                'password': 'Contraseña1*'
            }
        )

        self.assertEqual(response.status_code, 302)
