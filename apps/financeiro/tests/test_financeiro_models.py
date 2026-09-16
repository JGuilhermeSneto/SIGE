"""
Testes para apps.financeiro.models.

Cobre:
- Fatura.esta_atrasada (vencida + pendente vs. pago vs. futura)
- Fatura.__str__
- FolhaPagamento.salario_liquido
- Pagamento.save() — cria Lancamento e atualiza status da Fatura
- Pagamento.__str__
- CategoriaFinanceira.__str__
- CentroCusto.__str__
- AcordoFinanceiro.__str__
- ParcelaAcordo.__str__
- ConfiguracaoGateway.__str__
"""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.academico.models import Turma
from apps.financeiro.models import (
    AcordoFinanceiro,
    CategoriaFinanceira,
    CentroCusto,
    ConfiguracaoGateway,
    Fatura,
    FolhaPagamento,
    Lancamento,
    Pagamento,
    ParcelaAcordo,
)
from apps.usuarios.models.perfis import Aluno

User = get_user_model()


def _make_aluno(username, cpf):
    user = User.objects.create_user(username=username, password="pass")
    turma = Turma.objects.get_or_create(nome="5B", turno="tarde", ano=2024)[0]
    return Aluno.objects.create(
        user=user,
        nome_completo=f"Aluno {username}",
        cpf=cpf,
        data_nascimento="2005-01-01",
        turma=turma,
    )


class FaturaEstAAtrasadaTest(TestCase):
    """Testa a propriedade `esta_atrasada` de Fatura."""

    def setUp(self):
        self.aluno = _make_aluno("aluno_fat", "123.123.123-12")

    def test_fatura_pendente_e_vencida_esta_atrasada(self):
        fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Jan",
            valor=Decimal("500.00"),
            data_vencimento=date.today() - timedelta(days=5),
            status="PENDENTE",
        )
        self.assertTrue(fatura.esta_atrasada)

    def test_fatura_pendente_nao_vencida_nao_esta_atrasada(self):
        fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Fev",
            valor=Decimal("500.00"),
            data_vencimento=date.today() + timedelta(days=10),
            status="PENDENTE",
        )
        self.assertFalse(fatura.esta_atrasada)

    def test_fatura_paga_e_vencida_nao_esta_atrasada(self):
        fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Mar",
            valor=Decimal("500.00"),
            data_vencimento=date.today() - timedelta(days=3),
            status="PAGO",
        )
        self.assertFalse(fatura.esta_atrasada)

    def test_fatura_cancelada_nao_esta_atrasada(self):
        fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Abr",
            valor=Decimal("500.00"),
            data_vencimento=date.today() - timedelta(days=1),
            status="CANCELADO",
        )
        self.assertFalse(fatura.esta_atrasada)

    def test_fatura_str(self):
        fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Mai",
            valor=Decimal("500.00"),
            data_vencimento=date.today(),
            status="PENDENTE",
        )
        resultado = str(fatura)
        self.assertIn("Aluno aluno_fat", resultado)
        self.assertIn("PENDENTE", resultado)


class FolhaPagamentoSalarioLiquidoTest(TestCase):
    """Testa a propriedade `salario_liquido` de FolhaPagamento."""

    def setUp(self):
        self.funcionario = User.objects.create_user("func1", password="pass")

    def test_salario_liquido_calculo_basico(self):
        folha = FolhaPagamento.objects.create(
            funcionario=self.funcionario,
            mes_referencia=1,
            ano_referencia=2024,
            salario_base=Decimal("3000.00"),
            bonus=Decimal("500.00"),
            descontos=Decimal("200.00"),
            impostos_encargos=Decimal("300.00"),
        )
        # (3000 + 500) - (200 + 300) = 3000
        self.assertAlmostEqual(float(folha.salario_liquido), 3000.0, places=2)

    def test_salario_liquido_sem_bonus_e_descontos(self):
        folha = FolhaPagamento.objects.create(
            funcionario=self.funcionario,
            mes_referencia=2,
            ano_referencia=2024,
            salario_base=Decimal("2500.00"),
        )
        self.assertAlmostEqual(float(folha.salario_liquido), 2500.0, places=2)

    def test_salario_liquido_com_descontos_maiores_que_salario(self):
        folha = FolhaPagamento.objects.create(
            funcionario=self.funcionario,
            mes_referencia=3,
            ano_referencia=2024,
            salario_base=Decimal("1000.00"),
            descontos=Decimal("800.00"),
            impostos_encargos=Decimal("300.00"),
        )
        # (1000 + 0) - (800 + 300) = -100
        self.assertAlmostEqual(float(folha.salario_liquido), -100.0, places=2)


class PagamentoSaveTest(TestCase):
    """Testa o método save() customizado de Pagamento."""

    def setUp(self):
        self.aluno = _make_aluno("aluno_pag", "456.456.456-45")
        self.fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Jun",
            valor=Decimal("600.00"),
            data_vencimento=date.today() + timedelta(days=10),
            status="PENDENTE",
        )

    def test_pagamento_cria_lancamento_automaticamente(self):
        Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("300.00"),
            metodo="PIX",
            data_pagamento=timezone.now(),
        )
        lancamentos = Lancamento.objects.filter(fatura_origem=self.fatura)
        self.assertEqual(lancamentos.count(), 1)
        lancamento = lancamentos.first()
        self.assertEqual(lancamento.tipo, "ENTRADA")
        self.assertEqual(float(lancamento.valor), 300.0)

    def test_pagamento_total_atualiza_status_para_pago(self):
        Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("600.00"),
            metodo="BOLETO",
            data_pagamento=timezone.now(),
        )
        self.fatura.refresh_from_db()
        self.assertEqual(self.fatura.status, "PAGO")

    def test_pagamento_parcial_nao_muda_status(self):
        Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("200.00"),
            metodo="DINHEIRO",
            data_pagamento=timezone.now(),
        )
        self.fatura.refresh_from_db()
        # Pagamento parcial não deve marcar como pago
        self.assertNotEqual(self.fatura.status, "PAGO")

    def test_pagamento_dois_parciais_completam_fatura(self):
        Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("300.00"),
            metodo="PIX",
            data_pagamento=timezone.now(),
        )
        Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("300.00"),
            metodo="PIX",
            data_pagamento=timezone.now(),
        )
        self.fatura.refresh_from_db()
        self.assertEqual(self.fatura.status, "PAGO")

    def test_pagamento_str(self):
        pag = Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("100.00"),
            metodo="CARTAO",
            data_pagamento=timezone.now(),
        )
        resultado = str(pag)
        self.assertIn(str(pag.id), resultado)
        self.assertIn(str(self.fatura.id), resultado)

    def test_segundo_save_nao_cria_lancamento_duplicado(self):
        """Re-salvar um Pagamento existente não deve criar novo Lancamento."""
        pag = Pagamento.objects.create(
            fatura=self.fatura,
            valor_pago=Decimal("100.00"),
            metodo="PIX",
            data_pagamento=timezone.now(),
        )
        count_antes = Lancamento.objects.filter(fatura_origem=self.fatura).count()
        pag.save()  # Re-save
        count_depois = Lancamento.objects.filter(fatura_origem=self.fatura).count()
        self.assertEqual(count_antes, count_depois)


class FinanceiroModelsStrTest(TestCase):
    """Testa os __str__ dos models auxiliares."""

    def test_categoria_financeira_str(self):
        cat = CategoriaFinanceira.objects.create(nome="Energia", tipo="DESPESA")
        self.assertIn("Energia", str(cat))
        self.assertIn("DESPESA", str(cat))

    def test_centro_custo_str(self):
        cc = CentroCusto.objects.create(nome="Administrativo")
        self.assertEqual(str(cc), "Administrativo")

    def test_acordo_financeiro_str(self):
        aluno = _make_aluno("aluno_acordo", "789.789.789-78")
        fatura = Fatura.objects.create(
            aluno=aluno,
            descricao="Fatura base",
            valor=Decimal("1000.00"),
            data_vencimento=date.today(),
        )
        acordo = AcordoFinanceiro.objects.create(
            aluno=aluno,
            valor_total_original=Decimal("1000.00"),
            valor_com_desconto=Decimal("900.00"),
            numero_parcelas=2,
        )
        acordo.faturas_originais.add(fatura)
        resultado = str(acordo)
        self.assertIn("Acordo", resultado)
        self.assertIn("Aluno aluno_acordo", resultado)

    def test_parcela_acordo_str(self):
        aluno = _make_aluno("aluno_parcela", "321.321.321-32")
        acordo = AcordoFinanceiro.objects.create(
            aluno=aluno,
            valor_total_original=Decimal("500.00"),
            valor_com_desconto=Decimal("450.00"),
            numero_parcelas=1,
        )
        parcela = ParcelaAcordo.objects.create(
            acordo=acordo,
            valor=Decimal("450.00"),
            data_vencimento=date.today() + timedelta(days=30),
        )
        resultado = str(parcela)
        self.assertIn("Parcela", resultado)
        self.assertIn(str(acordo.id), resultado)

    def test_configuracao_gateway_str_ativo(self):
        gw = ConfiguracaoGateway.objects.create(
            nome="ASAAS", api_key="chave-secreta-teste", ativo=True
        )
        resultado = str(gw)
        self.assertIn("Asaas", resultado)
        self.assertIn("Ativo", resultado)

    def test_configuracao_gateway_str_inativo(self):
        gw = ConfiguracaoGateway.objects.create(
            nome="STRIPE", api_key="chave-stripe-teste", ativo=False
        )
        resultado = str(gw)
        self.assertIn("Inativo", resultado)
