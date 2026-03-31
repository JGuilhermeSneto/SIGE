from django.test import TestCase
from django.contrib.auth import get_user_model

from core.forms import LoginForm, ProfessorForm, AlunoForm, GestorForm, EditarPerfilForm
from core.models import Professor, Aluno, Gestor

User = get_user_model()


class FormsEdgeTest(TestCase):

    # ===== LOGIN OK =====
    def test_login_valido(self):
        user = User.objects.create_user(
            username="user",
            email="user@email.com",
            password="Senha123"
        )

        form = LoginForm(data={
            "email": user.email,
            "password": "Senha123"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), user)

    # ===== PROFESSOR EDGE =====
    def test_professor_senha_sem_minuscula(self):
        form = ProfessorForm(data={
            "nome_completo": "Teste",
            "cpf": "123",
            "email": "x@x.com",
            "senha": "ABC123",
            "senha_confirmacao": "ABC123",
        })
        self.assertFalse(form.is_valid())

    def test_professor_senha_sem_numero(self):
        form = ProfessorForm(data={
            "nome_completo": "Teste",
            "cpf": "123",
            "email": "x2@x.com",
            "senha": "Abcdef",
            "senha_confirmacao": "Abcdef",
        })
        self.assertFalse(form.is_valid())

    def test_professor_update_user(self):
        user = User.objects.create_user(
            username="prof",
            email="old@email.com",
            password="123456"
        )

        professor = Professor.objects.create(
            nome_completo="Prof Teste",
            cpf="123",
            user=user
        )

        form = ProfessorForm(
            instance=professor,
            data={
                "nome_completo": "Prof Teste",
                "cpf": "123",
                "email": "novo@email.com",
            }
        )

        self.assertTrue(form.is_valid())
        obj = form.save()

        self.assertEqual(obj.user.email, "novo@email.com")

    # ===== ALUNO EDGE =====
    def test_aluno_senha_curta(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno",
            "cpf": "123",
            "email": "a@a.com",
            "senha": "123",
            "senha_confirmacao": "123",
        })

        self.assertFalse(form.is_valid())

    def test_aluno_update_user(self):
        user = User.objects.create_user(username="aluno", email="old@a.com")

        aluno = Aluno.objects.create(
            nome_completo="Aluno",
            cpf="123",
            user=user
        )

        form = AlunoForm(
            instance=aluno,
            data={
                "nome_completo": "Aluno",
                "cpf": "123",
                "email": "novo@a.com",
            }
        )

        self.assertTrue(form.is_valid())
        obj = form.save()

        self.assertEqual(obj.user.email, "novo@a.com")

    # ===== GESTOR EDGE =====
    def test_gestor_save_cria_user(self):
        form = GestorForm(data={
            "nome_completo": "Gestor Teste",
            "cpf": "123",
            "senha": "123456",
            "senha_confirmacao": "123456",
        })

        self.assertTrue(form.is_valid())
        gestor = form.save()

        self.assertIsNotNone(gestor.user)

    # ===== EDITAR PERFIL EDGE =====
    def test_editar_senha_curta(self):
        user = User.objects.create_user(username="u", email="u@u.com")

        form = EditarPerfilForm(
            instance=user,
            data={
                "email": "u@u.com",
                "nova_senha": "123",
                "confirmar_senha": "123",
            }
        )

        self.assertFalse(form.is_valid())