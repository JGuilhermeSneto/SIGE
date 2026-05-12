from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.usuarios.models.perfis import Aluno, Professor, Gestor, Responsavel
from apps.academico.models.academico import Turma, Disciplina

User = get_user_model()


class PaineisViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"

        # Superusuário
        self.super_user = User.objects.create_superuser(
            username="super", email="super@test.com", password=self.password
        )

        # Professor
        self.prof_user = User.objects.create_user(
            username="prof", email="prof@test.com", password=self.password
        )
        self.professor = Professor.objects.create(
            user=self.prof_user,
            nome_completo="Prof Teste",
            cpf="111.111.111-11",
            data_nascimento="1980-01-01",
        )

        # Aluno e Turma
        from django.utils import timezone

        self.turma = Turma.objects.create(
            nome="1A", turno="manha", ano=timezone.now().year
        )
        self.aluno_user = User.objects.create_user(
            username="aluno", email="aluno@test.com", password=self.password
        )
        self.aluno = Aluno.objects.create(
            user=self.aluno_user,
            nome_completo="Aluno Teste",
            cpf="222.222.222-22",
            data_nascimento="2010-01-01",
            turma=self.turma,
        )

        # Responsável
        self.resp_user = User.objects.create_user(
            username="resp", email="resp@test.com", password=self.password
        )
        self.responsavel = Responsavel.objects.create(
            user=self.resp_user,
            nome_completo="Resp Teste",
            cpf="333.333.333-33",
            data_nascimento="1975-01-01",
        )
        self.responsavel.alunos.add(self.aluno)

    def test_painel_super_acesso(self):
        self.client.login(username="super", password=self.password)
        response = self.client.get(reverse("painel_super"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "superusuario/painel_super.html")
        self.assertIn("bi_turmas_labels", response.context)

    def test_painel_professor_acesso(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(reverse("painel_professor"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/painel_professor.html")
        self.assertEqual(response.context["professor"], self.professor)

    def test_painel_aluno_acesso(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("painel_aluno"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aluno/painel_aluno.html")
        self.assertEqual(response.context["aluno"], self.aluno)

    def test_painel_responsavel_acesso(self):
        self.client.login(username="resp", password=self.password)
        response = self.client.get(reverse("painel_responsavel"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "responsavel/painel_responsavel.html")
        self.assertTrue(len(response.context["dependentes"]) > 0)

    def test_dashboard_redirect_super(self):
        self.client.login(username="super", password=self.password)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("painel_super"))

    def test_dashboard_redirect_aluno(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("painel_aluno"))

    def test_painel_professor_sem_perfil(self):
        # Usuário logado mas sem ser professor
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("painel_professor"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/sem_perfil.html")

    def test_painel_aluno_sem_perfil(self):
        # Usuário logado mas sem ser aluno
        self.client.login(username="prof", password=self.password)
        response = self.client.get(reverse("painel_aluno"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/sem_perfil.html")

    def test_painel_responsavel_sem_perfil(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("painel_responsavel"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/sem_perfil.html")

    def test_painel_aluno_acesso_responsavel(self):
        # Responsável acessando o painel do aluno (dependente)
        self.client.login(username="resp", password=self.password)
        response = self.client.get(
            reverse("painel_aluno") + f"?aluno_id={self.aluno.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aluno/painel_aluno.html")
        self.assertEqual(response.context["aluno"], self.aluno)

    def test_painel_usuarios_acesso(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("painel_usuarios"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/usuarios.html")
