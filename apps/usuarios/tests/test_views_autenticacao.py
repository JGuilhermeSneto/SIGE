from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.usuarios.models.perfis import Aluno, Professor, Gestor

User = get_user_model()


class AutenticacaoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password=self.password
        )
        # Cria um perfil para o redirecionamento funcionar
        self.gestor = Gestor.objects.create(
            user=self.user,
            nome_completo="Test Gestor",
            cpf="123.123.123-12",
            cargo="diretor",
        )

    def test_login_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post(
            reverse("login"), {"email": "test@test.com", "password": self.password}
        )
        self.assertRedirects(response, reverse("painel_gestor"))

    def test_logout(self):
        self.client.login(username="testuser", password=self.password)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_redirect_user_view(self):
        self.client.login(username="testuser", password=self.password)
        response = self.client.get(reverse("redirect_user"))
        self.assertRedirects(response, reverse("painel_gestor"))
