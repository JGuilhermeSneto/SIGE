from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from apps.usuarios.forms.autenticacao import LoginForm, EditarPerfilForm

User = get_user_model()


class AutenticacaoFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.factory = RequestFactory()
        self.request = self.factory.post('/login/')

    def test_login_form_valido(self):
        form_data = {"email": "test@example.com", "password": "password123"}
        form = LoginForm(data=form_data, request=self.request)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_login_form_email_invalido(self):
        form_data = {"email": "invalid@example.com", "password": "password123"}
        form = LoginForm(data=form_data, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertIn("E-mail não encontrado.", form.errors['__all__'])

    def test_login_form_senha_incorreta(self):
        form_data = {"email": "test@example.com", "password": "wrongpassword"}
        form = LoginForm(data=form_data, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertIn("Senha incorreta.", form.errors['__all__'])

    def test_editar_perfil_form_valido(self):
        form_data = {"email": "newemail@example.com"}
        form = EditarPerfilForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_editar_perfil_form_email_duplicado(self):
        User.objects.create_user(username="other", email="other@example.com", password="pass")
        form_data = {"email": "other@example.com"}
        form = EditarPerfilForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("E-mail já está em uso.", form.errors['email'])

    def test_editar_perfil_form_senhas_nao_coincidem(self):
        form_data = {
            "email": "test@example.com",
            "nova_senha": "newpass",
            "confirmar_senha": "different"
        }
        form = EditarPerfilForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("As senhas não coincidem.", form.errors['__all__'])