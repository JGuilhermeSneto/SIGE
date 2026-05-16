from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.financeiro.models import Fatura, Pagamento, Lancamento, CategoriaFinanceira
from apps.usuarios.models.perfis import Aluno, Gestor
from apps.academico.models import Turma
from django.utils import timezone

User = get_user_model()


class FinanceiroViewsTest(TestCase):
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

        # Fatura
        self.fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Jan",
            valor=500.00,
            data_vencimento=timezone.now().date() + timezone.timedelta(days=5),
        )

        # Categoria
        self.categoria = CategoriaFinanceira.objects.create(nome="Educação")

    def test_listar_faturas_aluno(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("financeiro:listar_faturas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mensalidade Jan")

    def test_painel_financeiro_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse("financeiro:painel_financeiro"))
        self.assertEqual(response.status_code, 200)

    def test_painel_financeiro_aluno_negado(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("financeiro:painel_financeiro"))
        self.assertEqual(response.status_code, 403)

    def test_criar_lancamento_gestor(self):
        self.client.login(username="gestor", password=self.password)
        data = {
            "tipo": "ENTRADA",
            "descricao": "Venda de material",
            "valor": "100.00",
            "categoria": self.categoria.id,
            "data_pagamento": timezone.now().date(),
        }
        response = self.client.post(reverse("financeiro:criar_lancamento"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Lancamento.objects.filter(descricao="Venda de material").count(), 1
        )

    def test_detalhes_fatura(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(
            reverse("financeiro:detalhes_fatura", args=[self.fatura.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mensalidade Jan")
