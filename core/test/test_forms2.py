from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from core.forms import AlunoForm, EditarPerfilForm, GestorForm, LoginForm, ProfessorForm
from core.models import Aluno, Gestor, Professor

User = get_user_model()


class FormsExtraTest(TestCase):

    # ================= LOGIN =================

    def test_login_email_nao_encontrado(self):
        form = LoginForm(data={"email": "x@email.com", "password": "123"})
        self.assertFalse(form.is_valid())

    def test_login_sem_dados(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_senha_incorreta(self):
        user = User.objects.create_user(
            username="teste", email="teste@email.com", password="123456"
        )

        form = LoginForm(data={"email": user.email, "password": "errada"})
        self.assertFalse(form.is_valid())

    # ================= PROFESSOR =================

    def test_professor_senha_curta(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "a@a.com",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_professor_senha_sem_maiuscula(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "a@a.com",
                "senha": "abcdef1",
                "senha_confirmacao": "abcdef1",
            }
        )
        self.assertFalse(form.is_valid())

    def test_professor_email_duplicado(self):
        User.objects.create_user(username="u1", email="dup@email.com")

        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "dup@email.com",
            }
        )

        self.assertFalse(form.is_valid())

    def test_professor_save_cria_user(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Teste Nome",
                "cpf": "123",
                "email": "novo@email.com",
                "senha": "Senha123",
                "senha_confirmacao": "Senha123",
            }
        )

        self.assertTrue(form.is_valid())
        obj = form.save()

        self.assertIsNotNone(obj.user)
        self.assertEqual(obj.user.email, "novo@email.com")

    # ================= ALUNO =================

    def test_aluno_necessidade_sem_descricao(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno",
                "cpf": "123",
                "email": "aluno@email.com",
                "possui_necessidade_especial": True,
                "descricao_necessidade": "",
            }
        )

        self.assertFalse(form.is_valid())

    def test_aluno_senha_diferente(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno",
                "cpf": "123",
                "email": "a@a.com",
                "senha": "123456",
                "senha_confirmacao": "654321",
            }
        )

        self.assertFalse(form.is_valid())

    def test_aluno_save_cria_user(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno Teste",
                "cpf": "123",
                "email": "aluno2@email.com",
            }
        )

        self.assertTrue(form.is_valid())
        aluno = form.save()

        self.assertIsNotNone(aluno.user)

    # ================= GESTOR =================

    def test_gestor_senha_curta(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor",
                "cpf": "123",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )

        self.assertFalse(form.is_valid())

    def test_gestor_senha_diferente(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor",
                "cpf": "123",
                "senha": "123456",
                "senha_confirmacao": "654321",
            }
        )

        self.assertFalse(form.is_valid())

    # ================= EDITAR PERFIL =================

    def test_editar_email_duplicado(self):
        u1 = User.objects.create_user(username="u1", email="a@a.com")
        u2 = User.objects.create_user(username="u2", email="b@b.com")

        form = EditarPerfilForm(instance=u2, data={"email": "a@a.com"})

        self.assertFalse(form.is_valid())

    def test_editar_senha_diferente(self):
        user = User.objects.create_user(username="u", email="x@x.com")

        form = EditarPerfilForm(
            instance=user,
            data={
                "email": "x@x.com",
                "nova_senha": "123456",
                "confirmar_senha": "654321",
            },
        )

        self.assertFalse(form.is_valid())
