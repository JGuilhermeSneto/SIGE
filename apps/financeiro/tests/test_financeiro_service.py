"""
Testes para apps.financeiro.services.financeiro_service.

Cobre:
- FinanceiroService.registrar_pagamento
- FinanceiroService.gerar_fatura_mensal
- FinanceiroService.criar_acordo
"""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.academico.models import Turma
from apps.financeiro.models import (
    AcordoFinanceiro,
    Fatura,
    Lancamento,
    Pagamento,
    ParcelaAcordo,
)
from apps.financeiro.services.financeiro_service import FinanceiroService
from apps.usuarios.models.perfis import Aluno

User = get_user_model()


def _make_aluno(username, cpf):
    user = User.objects.create_user(username=username, password="pass")
    turma = Turma.objects.get_or_create(nome="6A", turno="noite", ano=2024)[0]
    return Aluno.objects.create(
        user=user,
        nome_completo=f"Aluno {username}",
        cpf=cpf,
        data_nascimento="2003-06-15",
        turma=turma,
    )


class RegistrarPagamentoTest(TestCase):
    """Testa FinanceiroService.registrar_pagamento."""

    def setUp(self):
        self.aluno = _make_aluno("aluno_rp", "100.200.300-40")
        self.fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Julho",
            valor=Decimal("750.00"),
            data_vencimento=date.today() + timedelta(days=5),
            status="PENDENTE",
        )

    def test_registrar_pagamento_cria_objeto_pagamento(self):
        pag = FinanceiroService.registrar_pagamento(
            fatura_id=self.fatura.id,
            valor=Decimal("750.00"),
            metodo="PIX",
        )
        self.assertIsInstance(pag, Pagamento)
        self.assertEqual(pag.fatura, self.fatura)
        self.assertEqual(float(pag.valor_pago), 750.0)
        self.assertEqual(pag.metodo, "PIX")

    def test_registrar_pagamento_cria_lancamento_no_livro_diario(self):
        FinanceiroService.registrar_pagamento(
            fatura_id=self.fatura.id,
            valor=Decimal("750.00"),
            metodo="BOLETO",
        )
        lancamentos = Lancamento.objects.filter(fatura_origem=self.fatura)
        self.assertEqual(lancamentos.count(), 1)
        self.assertEqual(lancamentos.first().tipo, "ENTRADA")

    def test_registrar_pagamento_total_muda_status_fatura_para_pago(self):
        FinanceiroService.registrar_pagamento(
            fatura_id=self.fatura.id,
            valor=Decimal("750.00"),
            metodo="DINHEIRO",
        )
        self.fatura.refresh_from_db()
        self.assertEqual(self.fatura.status, "PAGO")

    def test_registrar_pagamento_parcial_nao_muda_status(self):
        FinanceiroService.registrar_pagamento(
            fatura_id=self.fatura.id,
            valor=Decimal("200.00"),
            metodo="CARTAO",
        )
        self.fatura.refresh_from_db()
        self.assertNotEqual(self.fatura.status, "PAGO")

    def test_registrar_pagamento_para_fatura_inexistente_levanta_erro(self):
        with self.assertRaises(Fatura.DoesNotExist):
            FinanceiroService.registrar_pagamento(
                fatura_id=99999, valor=Decimal("100.00"), metodo="PIX"
            )


class GerarFaturaMensalTest(TestCase):
    """Testa FinanceiroService.gerar_fatura_mensal."""

    def setUp(self):
        self.aluno = _make_aluno("aluno_gf", "200.300.400-50")

    def test_gerar_fatura_cria_fatura_no_banco(self):
        vencimento = date.today() + timedelta(days=30)
        fatura = FinanceiroService.gerar_fatura_mensal(
            aluno=self.aluno,
            descricao="Mensalidade Agosto",
            valor=Decimal("800.00"),
            data_vencimento=vencimento,
        )
        self.assertIsInstance(fatura, Fatura)
        self.assertEqual(fatura.aluno, self.aluno)
        self.assertEqual(fatura.descricao, "Mensalidade Agosto")
        self.assertEqual(float(fatura.valor), 800.0)
        self.assertEqual(fatura.data_vencimento, vencimento)
        self.assertEqual(fatura.status, "PENDENTE")  # default

    def test_gerar_fatura_persiste_no_banco(self):
        FinanceiroService.gerar_fatura_mensal(
            aluno=self.aluno,
            descricao="Mensalidade Setembro",
            valor=Decimal("800.00"),
            data_vencimento=date.today() + timedelta(days=60),
        )
        self.assertEqual(Fatura.objects.filter(aluno=self.aluno).count(), 1)


class CriarAcordoTest(TestCase):
    """Testa FinanceiroService.criar_acordo."""

    def setUp(self):
        self.aluno = _make_aluno("aluno_ac", "300.400.500-60")

        # Criar faturas atrasadas
        self.fatura1 = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Jan atrasada",
            valor=Decimal("500.00"),
            data_vencimento=date.today() - timedelta(days=60),
            status="PENDENTE",
        )
        self.fatura2 = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Fev atrasada",
            valor=Decimal("500.00"),
            data_vencimento=date.today() - timedelta(days=30),
            status="PENDENTE",
        )

    def test_criar_acordo_retorna_objeto_acordo(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=3,
            valor_com_desconto=Decimal("900.00"),
        )
        self.assertIsInstance(acordo, AcordoFinanceiro)
        self.assertEqual(acordo.aluno, self.aluno)
        self.assertEqual(float(acordo.valor_total_original), 1000.0)
        self.assertEqual(float(acordo.valor_com_desconto), 900.0)

    def test_criar_acordo_cancela_faturas_originais(self):
        FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=2,
            valor_com_desconto=Decimal("800.00"),
        )
        self.fatura1.refresh_from_db()
        self.fatura2.refresh_from_db()
        self.assertEqual(self.fatura1.status, "CANCELADO")
        self.assertEqual(self.fatura2.status, "CANCELADO")

    def test_criar_acordo_gera_parcelas_corretas(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=4,
            valor_com_desconto=Decimal("800.00"),
        )
        parcelas = ParcelaAcordo.objects.filter(acordo=acordo)
        self.assertEqual(parcelas.count(), 4)

    def test_criar_acordo_valor_parcelas_dividido_corretamente(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=5,
            valor_com_desconto=Decimal("1000.00"),
        )
        parcelas = ParcelaAcordo.objects.filter(acordo=acordo)
        for parcela in parcelas:
            self.assertAlmostEqual(float(parcela.valor), 200.0, places=2)

    def test_criar_acordo_vincula_faturas_originais(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=2,
            valor_com_desconto=Decimal("900.00"),
        )
        ids_vinculadas = set(acordo.faturas_originais.values_list("id", flat=True))
        self.assertIn(self.fatura1.id, ids_vinculadas)
        self.assertIn(self.fatura2.id, ids_vinculadas)

    def test_criar_acordo_com_observacoes(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id],
            numero_parcelas=1,
            valor_com_desconto=Decimal("450.00"),
            observacoes="Desconto por pontualidade futura.",
        )
        self.assertEqual(acordo.observacoes, "Desconto por pontualidade futura.")

    def test_parcelas_tem_datas_de_vencimento_crescentes(self):
        acordo = FinanceiroService.criar_acordo(
            aluno=self.aluno,
            fatura_ids=[self.fatura1.id, self.fatura2.id],
            numero_parcelas=3,
            valor_com_desconto=Decimal("900.00"),
        )
        datas = list(
            ParcelaAcordo.objects.filter(acordo=acordo)
            .order_by("data_vencimento")
            .values_list("data_vencimento", flat=True)
        )
        self.assertEqual(datas, sorted(datas))
        # Cada parcela deve ter vencimento 30 dias depois da anterior
        for i in range(1, len(datas)):
            diff = (datas[i] - datas[i - 1]).days
            self.assertEqual(diff, 30)
