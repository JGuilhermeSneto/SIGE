from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.saude.models.ficha_medica import FichaMedica, AtestadoMedico
from apps.usuarios.models.perfis import Aluno, Gestor
from apps.academico.models.academico import Turma
from django.utils import timezone

User = get_user_model()


class SaudeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"

        # Gestor
        self.gestor_user = User.objects.create_superuser(
            username="gestor", password=self.password
        )
        self.gestor = Gestor.objects.create(
            user=self.gestor_user,
            nome_completo="Gestor 1",
            cpf="1",
            data_nascimento="1980-01-01",
        )

        # Aluno
        self.aluno_user = User.objects.create_user(
            username="aluno", password=self.password
        )
        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)
        self.aluno = Aluno.objects.create(
            user=self.aluno_user,
            nome_completo="Aluno 1",
            cpf="2",
            data_nascimento="2010-01-01",
            turma=self.turma,
        )

        # Ficha Médica
        self.ficha = FichaMedica.objects.create(aluno=self.aluno, tipo_sanguineo="O+")

    def test_visualizar_saude_aluno_proprio(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(
            reverse("visualizar_saude_aluno", args=[self.aluno.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O+")

    def test_visualizar_saude_aluno_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(
            reverse("visualizar_saude_aluno", args=[self.aluno.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_ficha_medica_gestor(self):
        self.client.login(username="gestor", password=self.password)
        data = {
            "tipo_sanguineo": "A-",
            "alergias": "Nenhuma",
            "medicacoes": "Nenhuma",
            "observacoes": "Tudo ok",
        }
        response = self.client.post(
            reverse("editar_ficha_medica", args=[self.aluno.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.tipo_sanguineo, "A-")

    def test_gestao_atestados_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse("gestao_atestados"))
        self.assertEqual(response.status_code, 200)
