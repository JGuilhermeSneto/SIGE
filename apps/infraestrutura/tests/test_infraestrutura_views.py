from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.infraestrutura.models.patrimonio import ItemPatrimonio
from apps.usuarios.models.perfis import Gestor

User = get_user_model()


class InfraestruturaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        self.gestor_user = User.objects.create_superuser(
            username="gestor", password=self.password
        )
        self.gestor = Gestor.objects.create(
            user=self.gestor_user,
            nome_completo="Gestor 1",
            cpf="1",
            data_nascimento="1980-01-01",
        )

    def test_painel_infraestrutura_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse("painel_infraestrutura"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_patrimonio(self):
        self.client.login(username="gestor", password=self.password)
        data = {
            "nome": "Cadeira",
            "codigo": "PAT001",
            "estado": "BOM",
            "valor_estimado": "100.00",
        }
        response = self.client.post(reverse("cadastrar_patrimonio"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemPatrimonio.objects.filter(nome="Cadeira").count(), 1)
