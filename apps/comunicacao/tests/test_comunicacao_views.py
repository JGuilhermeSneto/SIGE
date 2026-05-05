from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.comunicacao.models.comunicado import Comunicado
from apps.usuarios.models.perfis import Gestor

User = get_user_model()

class ComunicacaoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        self.gestor_user = User.objects.create_superuser(username="gestor", password=self.password)
        self.gestor = Gestor.objects.create(user=self.gestor_user, nome_completo="Gestor 1", cpf="1", data_nascimento="1980-01-01")

    def test_listar_comunicados_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse('listar_comunicados_gestao'))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_comunicado(self):
        self.client.login(username="gestor", password=self.password)
        data = {
            'titulo': 'Comunicado Teste',
            'conteudo': 'Conteudo do comunicado',
            'tipo': 'GERAL'
        }
        response = self.client.post(reverse('cadastrar_comunicado'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comunicado.objects.filter(titulo='Comunicado Teste').count(), 1)
