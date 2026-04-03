from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Professor

User = get_user_model()

class ViewsBasicasTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='admin', password='123')
        # Precisamos de um perfil para algumas views não quebrarem
        self.professor = Professor.objects.create(
            user=self.user, nome_completo="Admin Teste", cpf="000.000.000-00"
        )

    def test_acesso_painel_super_logado(self):
        # 1. Tenta acessar sem login (deve redirecionar)
        response = self.client.get(reverse('painel_super'))
        self.assertEqual(response.status_code, 302)

        # 2. Faz login
        self.client.login(username='admin', password='123')

        # 3. Acessa agora (deve dar 200 e executar o código da view)
        response = self.client.get(reverse('painel_super'))
        self.assertEqual(response.status_code, 200)