from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Gestor
from apps.saude.models.ficha_medica import FichaMedica, AtestadoMedico

User = get_user_model()


class SaudeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"

        # Gestor
        self.gestor_user = User.objects.create_user(
            username="gestor_saude", email="gestor@saude.com", password=self.password
        )
        self.gestor = Gestor.objects.create(
            user=self.gestor_user, nome_completo="Gestor Saude", cpf="111.111.111-11"
        )

        # Aluno
        self.aluno_user = User.objects.create_user(
            username="aluno_saude", email="aluno@saude.com", password=self.password
        )
        self.aluno = Aluno.objects.create(
            user=self.aluno_user, nome_completo="Aluno Saude", cpf="222.222.222-22"
        )

        # Ficha Médica
        self.ficha = FichaMedica.objects.create(
            aluno=self.aluno, tipagem_sanguinea="O+"
        )

    def test_visualizar_saude_aluno_gestor(self):
        self.client.login(username="gestor_saude", password=self.password)
        response = self.client.get(
            reverse("visualizar_saude_aluno", args=[self.aluno.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["aluno"], self.aluno)

    def test_enviar_atestado_get(self):
        self.client.login(username="aluno_saude", password=self.password)
        response = self.client.get(reverse("enviar_atestado"))
        self.assertEqual(response.status_code, 200)

    def test_gestao_atestados_negado_aluno(self):
        self.client.login(username="aluno_saude", password=self.password)
        response = self.client.get(reverse("gestao_atestados"))
        self.assertEqual(
            response.status_code, 302
        )  # Redireciona por falta de permissão (user_passes_test)

    def test_listar_atestados_aluno(self):
        self.client.login(username="aluno_saude", password=self.password)
        response = self.client.get(reverse("listar_atestados_aluno"))
        self.assertEqual(response.status_code, 200)
