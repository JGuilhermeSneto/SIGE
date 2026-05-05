from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Gestor
from apps.financeiro.models import Fatura, Lancamento, CategoriaFinanceira

User = get_user_model()

class FinanceiroViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        
        # Gestor
        self.gestor_user = User.objects.create_user(
            username="gestor_fin", email="gestor@fin.com", password=self.password
        )
        self.gestor = Gestor.objects.create(
            user=self.gestor_user, nome_completo="Gestor Fin", cpf="111.111.111-11"
        )
        
        # Aluno
        self.aluno_user = User.objects.create_user(
            username="aluno_fin", email="aluno@fin.com", password=self.password
        )
        self.aluno = Aluno.objects.create(
            user=self.aluno_user, nome_completo="Aluno Fin", cpf="222.222.222-22"
        )
        
        # Categoria
        self.categoria = CategoriaFinanceira.objects.create(nome="Mensalidade")
        
        # Fatura
        self.fatura = Fatura.objects.create(
            aluno=self.aluno, valor=500.0, data_vencimento=timezone.now().date(),
            descricao="Mensalidade Maio"
        )

    def test_listar_faturas_aluno(self):
        self.client.login(username="aluno_fin", password=self.password)
        response = self.client.get(reverse('financeiro:listar_faturas'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fatura, response.context['faturas'])

    def test_listar_faturas_gestor(self):
        self.client.login(username="gestor_fin", password=self.password)
        response = self.client.get(reverse('financeiro:listar_faturas'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fatura, response.context['faturas'])

    def test_painel_financeiro_gestor(self):
        self.client.login(username="gestor_fin", password=self.password)
        response = self.client.get(reverse('financeiro:painel_financeiro'))
        self.assertEqual(response.status_code, 200)

    def test_detalhes_fatura(self):
        self.client.login(username="aluno_fin", password=self.password)
        response = self.client.get(reverse('financeiro:detalhes_fatura', args=[self.fatura.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['fatura'], self.fatura)

    def test_gestao_despesas_negado_aluno(self):
        self.client.login(username="aluno_fin", password=self.password)
        response = self.client.get(reverse('financeiro:gestao_despesas'))
        self.assertEqual(response.status_code, 403)

    def test_criar_lancamento_post(self):
        self.client.login(username="gestor_fin", password=self.password)
        data = {
            "tipo": "ENTRADA",
            "descricao": "Venda de Livro",
            "valor": "50.00",
            "categoria": self.categoria.id,
            "data_pagamento": "2024-05-10"
        }
        response = self.client.post(reverse('financeiro:criar_lancamento'), data)
        self.assertTrue(Lancamento.objects.filter(descricao="Venda de Livro").exists())
        self.assertRedirects(response, reverse('financeiro:painel_financeiro'))
