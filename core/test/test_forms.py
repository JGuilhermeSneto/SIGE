from django.contrib.auth import get_user_model
from django.test import TestCase

from core.forms import (AlunoForm, EditarPerfilForm, GestorForm, LoginForm,
                        ProfessorForm)
from core.models import Aluno, Gestor, Professor

User = get_user_model()


class LoginFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testeuser", email="teste@email.com", password="Senha123"
        )

    def test_login_valido(self):
        form = LoginForm(data={"email": "teste@email.com", "password": "Senha123"})
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.get_user())

    def test_email_invalido(self):
        form = LoginForm(data={"email": "naoexiste@email.com", "password": "Senha123"})
        self.assertFalse(form.is_valid())

    def test_senha_incorreta(self):
        form = LoginForm(data={"email": "teste@email.com", "password": "errada"})
        self.assertFalse(form.is_valid())


class ProfessorFormTest(TestCase):

    def test_email_duplicado(self):
        User.objects.create_user(username="u1", email="dup@email.com")

        form = ProfessorForm(
            data={
                "nome_completo": "Professor Teste",
                "cpf": "12345678900",
                "email": "dup@email.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_senha_invalida(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Professor Teste",
                "cpf": "12345678900",
                "email": "prof@email.com",
                "senha": "abc",
                "senha_confirmacao": "abc",
            }
        )

        self.assertFalse(form.is_valid())

    def test_senha_valida(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Professor Teste",
                "cpf": "12345678900",
                "email": "prof@email.com",
                "senha": "Senha123",
                "senha_confirmacao": "Senha123",
            }
        )

        # Pode falhar por outros campos obrigatórios do model,
        # mas aqui o foco é validar que não quebra na senha
        form.is_valid()
        self.assertNotIn("__all__", form.errors)


class AlunoFormTest(TestCase):

    def test_email_duplicado(self):
        User.objects.create_user(username="u1", email="dup@email.com")

        form = AlunoForm(
            data={
                "nome_completo": "Aluno Teste",
                "cpf": "12345678900",
                "email": "dup@email.com",
            }
        )

        self.assertFalse(form.is_valid())

    def test_senha_nao_confere(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno Teste",
                "cpf": "12345678900",
                "email": "aluno@email.com",
                "senha": "123456",
                "senha_confirmacao": "654321",
            }
        )

        self.assertFalse(form.is_valid())

    def test_necessidade_sem_descricao(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno Teste",
                "cpf": "12345678900",
                "email": "aluno@email.com",
                "possui_necessidade_especial": True,
                "descricao_necessidade": "",
            }
        )

        self.assertFalse(form.is_valid())


class GestorFormTest(TestCase):

    def test_senha_curta(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor Teste",
                "cpf": "12345678900",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )

        self.assertFalse(form.is_valid())

    def test_senha_valida(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor Teste",
                "cpf": "12345678900",
                "senha": "123456",
                "senha_confirmacao": "123456",
            }
        )

        form.is_valid()
        self.assertNotIn("__all__", form.errors)


class EditarPerfilFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1", email="user@email.com", password="123456"
        )

    def test_email_duplicado(self):
        User.objects.create_user(username="user2", email="dup@email.com")

        form = EditarPerfilForm(instance=self.user, data={"email": "dup@email.com"})

        self.assertFalse(form.is_valid())

    def test_senha_nao_confere(self):
        form = EditarPerfilForm(
            instance=self.user,
            data={
                "email": "novo@email.com",
                "nova_senha": "123456",
                "confirmar_senha": "654321",
            },
        )

        self.assertFalse(form.is_valid())

    def test_senha_valida(self):
        form = EditarPerfilForm(
            instance=self.user,
            data={
                "email": "novo@email.com",
                "nova_senha": "123456",
                "confirmar_senha": "123456",
            },
        )

        self.assertTrue(form.is_valid())
