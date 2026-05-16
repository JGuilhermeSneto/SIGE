from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Professor, Gestor

User = get_user_model()
from apps.academico.models import Turma


class RegistrosViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        self.super_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password=self.password
        )
        self.client.force_login(self.super_user)

        self.current_year = timezone.now().year
        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=self.current_year)

    def test_listar_usuarios_acesso(self):
        response = self.client.get(reverse("usuarios"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_alunos", response.context)

    def test_listar_professores(self):
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_alunos(self):
        response = self.client.get(reverse("listar_alunos"))
        self.assertEqual(response.status_code, 200)

    def test_listar_gestores(self):
        response = self.client.get(reverse("listar_gestores"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_professor_get(self):
        response = self.client.get(reverse("cadastrar_professor"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_aluno_get(self):
        response = self.client.get(reverse("cadastrar_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_desativar_usuario(self):
        other_user = User.objects.create_user(username="other", password=self.password)
        response = self.client.post(reverse("desativar_usuario", args=[other_user.id]))
        other_user.refresh_from_db()
        self.assertFalse(other_user.is_active)
        self.assertRedirects(response, reverse("usuarios"))

    def test_cadastrar_professor_post(self):
        data = {
            "email": "prof_novo@test.com",
            "senha": "senha123",
            "senha_confirmacao": "senha123",
            "nome_completo": "Novo Professor",
            "cpf": "893.434.452-02",
            "data_nascimento": "1980-01-01",
            "telefone": "84999999999",
            "area_atuacao": "matematica",
        }
        response = self.client.post(reverse("cadastrar_professor"), data)
        self.assertTrue(
            Professor.objects.filter(nome_completo="Novo Professor").exists()
        )
        self.assertRedirects(response, reverse("listar_professores"))

    def test_cadastrar_aluno_post(self):
        data = {
            "email": "aluno_novo@test.com",
            "senha": "senha123",
            "senha_confirmacao": "senha123",
            "nome_completo": "Novo Aluno",
            "cpf": "109.796.860-08",
            "data_nascimento": "2010-01-01",
            "turma": self.turma.id,
            "telefone": "84888888888",
            "responsavel1": "Mae do Aluno",
            # Ficha Médica (os campos são processados pela view no mesmo POST)
            "tipagem_sanguinea": "A+",
            "alergias": "Nenhuma",
        }
        response = self.client.post(reverse("cadastrar_aluno"), data)
        self.assertTrue(Aluno.objects.filter(nome_completo="Novo Aluno").exists())
        self.assertRedirects(response, reverse("listar_alunos"))

    def test_reativar_usuario(self):
        other_user = User.objects.create_user(
            username="inactive", password=self.password, is_active=False
        )
        response = self.client.post(reverse("reativar_usuario", args=[other_user.id]))
        other_user.refresh_from_db()
        self.assertTrue(other_user.is_active)
        self.assertRedirects(response, reverse("listar_desativados"))

    def test_excluir_professor(self):
        prof_user = User.objects.create_user(
            username="prof_del", password=self.password
        )
        prof = Professor.objects.create(
            user=prof_user, nome_completo="Del Prof", cpf="893.434.452-02"
        )
        response = self.client.post(reverse("excluir_professor", args=[prof.id]))
        self.assertFalse(Professor.objects.filter(id=prof.id).exists())
        self.assertRedirects(response, reverse("listar_professores"))

    def test_excluir_aluno(self):
        aluno_user = User.objects.create_user(
            username="aluno_del", password=self.password
        )
        aluno = Aluno.objects.create(
            user=aluno_user, nome_completo="Del Aluno", cpf="109.796.860-08",
            turma=self.turma
        )
        response = self.client.post(reverse("excluir_aluno", args=[aluno.id]))
        self.assertFalse(Aluno.objects.filter(id=aluno.id).exists())
        self.assertRedirects(response, reverse("listar_alunos"))

    def test_excluir_gestor(self):
        gestor_user = User.objects.create_user(
            username="gestor_del", password=self.password
        )
        gestor = Gestor.objects.create(
            user=gestor_user, nome_completo="Del Gestor", cpf="116.924.960-44"
        )
        response = self.client.post(reverse("excluir_gestor", args=[gestor.id]))
        self.assertFalse(Gestor.objects.filter(id=gestor.id).exists())

    def test_desativar_usuario_proprio(self):
        response = self.client.post(
            reverse("desativar_usuario", args=[self.super_user.id])
        )
        self.super_user.refresh_from_db()
        self.assertTrue(self.super_user.is_active)
        # Deve mostrar mensagem de erro
        messages = (
            list(response.context.get("messages", [])) if response.context else []
        )
        # Como é redirect, as mensagens estão no storage
        from django.contrib.messages import get_messages

        msgs = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "Você não pode desativar seu próprio acesso!" in m.message for m in msgs
            )
        )

    def test_cadastrar_professor_form_invalido(self):
        data = {"email": "invalido", "senha": "123"}
        response = self.client.post(reverse("cadastrar_professor"), data)
        self.assertEqual(response.status_code, 200)  # Volta para o form com erro
        self.assertTemplateUsed(response, "professor/cadastrar_professor.html")
