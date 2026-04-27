from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.academico.models.academico import Turma
from apps.usuarios.forms.perfis import ProfessorForm, AlunoForm, GestorForm
from apps.usuarios.models.perfis import Professor, Aluno, Gestor

User = get_user_model()


class PerfisFormsTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)

    def test_professor_form_criacao_valida(self):
        form_data = {
            "nome_completo": "Professor Teste",
            "cpf": "730.835.289-73",
            "data_nascimento": "1980-01-01",
            "email": "prof@example.com",
            "senha": "password123",
            "senha_confirmacao": "password123",
        }
        form = ProfessorForm(data=form_data)
        self.assertTrue(form.is_valid())
        prof = form.save()
        self.assertIsInstance(prof, Professor)
        self.assertEqual(prof.user.email, "prof@example.com")

    def test_aluno_form_criacao_valida(self):
        form_data = {
            "nome_completo": "Aluno Teste",
            "cpf": "844.660.319-59",
            "data_nascimento": "2010-01-01",
            "email": "aluno@example.com",
            "senha": "password123",
            "senha_confirmacao": "password123",
            "turma": self.turma.pk,
        }
        form = AlunoForm(data=form_data)
        self.assertTrue(form.is_valid())
        aluno = form.save()
        self.assertIsInstance(aluno, Aluno)
        self.assertEqual(aluno.user.email, "aluno@example.com")

    def test_gestor_form_criacao_valida(self):
        form_data = {
            "nome_completo": "Gestor Teste",
            "cpf": "048.492.642-04",
            "data_nascimento": "1975-01-01",
            "cargo": "diretor",
            "email": "gestor@example.com",
            "senha": "password123",
            "senha_confirmacao": "password123",
        }
        form = GestorForm(data=form_data)
        self.assertTrue(form.is_valid())
        gestor = form.save()
        self.assertIsInstance(gestor, Gestor)
        self.assertEqual(gestor.user.email, "gestor@example.com")

    def test_professor_form_email_duplicado(self):
        User.objects.create_user(username="existing", email="existing@example.com", password="pass")
        form_data = {
            "nome_completo": "Professor Teste",
            "cpf": "123.456.789-00",
            "data_nascimento": "1980-01-01",
            "email": "existing@example.com",
        }
        form = ProfessorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("E-mail em uso.", form.errors['email'])