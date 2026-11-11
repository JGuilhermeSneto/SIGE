"""
Testes Unitários dos 3 Motores Analíticos do ELISE IA.
Valida precisão determinística (ORM) sem dependência de serviços externos ou LLM.
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.academico.models.academico import Turma
from apps.usuarios.models.perfis import Aluno
from apps.infraestrutura.models.patrimonio import Ambiente, ItemPatrimonio, UnidadeEscolar, CategoriaBem
from apps.financeiro.models import Fatura
from apps.ia.models import PropostaDecisao
from apps.ia.services.enturmacao_service import (
    diagnosticar_enturmacao,
    gerar_propostas_enturmacao,
    CAPACIDADE_MINIMA,
    CAPACIDADE_MAXIMA,
)
from apps.ia.services.infraestrutura_service import (
    diagnosticar_infraestrutura,
    gerar_propostas_infraestrutura,
)
from apps.ia.services.financeiro_service import (
    diagnosticar_financeiro,
    gerar_propostas_financeiro,
    BREAK_EVEN_ALUNOS,
)

User = get_user_model()


class MotoresDSSTestCase(TestCase):
    """Testes dos Motores 1, 2 e 3 do Sistema de Apoio à Decisão."""

    @classmethod
    def setUpTestData(cls):
        # 1. Configurar Turmas de 2026
        cls.turma_a = Turma.objects.create(nome="1o Ano A", ano=2026, turno="manha")
        cls.turma_b = Turma.objects.create(nome="1o Ano B", ano=2026, turno="manha")

        # Turma A: 20 alunos ativos (sendo 2 PCDs) -> Equilibrada
        for i in range(20):
            user_a = User.objects.create_user(
                username=f"aluno_a_{i}",
                password="123"
            )
            Aluno.objects.create(
                user=user_a,
                nome_completo=f"Aluno A{i}",
                turma=cls.turma_a,
                status_matricula="ATIVO",
                possui_necessidade_especial=(i < 2)
            )

        # Turma B: 10 alunos ativos (0 PCDs) -> Sublotada (< 15)
        for i in range(10):
            user_b = User.objects.create_user(
                username=f"aluno_b_{i}",
                password="123"
            )
            Aluno.objects.create(
                user=user_b,
                nome_completo=f"Aluno B{i}",
                turma=cls.turma_b,
                status_matricula="ATIVO",
                possui_necessidade_especial=False
            )

        # 2. Configurar Infraestrutura
        cls.unidade = UnidadeEscolar.objects.create(nome="Unidade Central", eh_sede=True)
        cls.categoria = CategoriaBem.objects.create(nome="Mobiliário Escolar")
        cls.sala_101 = Ambiente.objects.create(nome="Sala 101", unidade=cls.unidade)

        # 10 itens na Sala 101, sendo 3 danificados (taxa de 30% avaria)
        for i in range(10):
            ItemPatrimonio.objects.create(
                tombamento=f"PAT-TEST-{i}",
                nome=f"Cadeira Escolar {i}",
                categoria=cls.categoria,
                unidade=cls.unidade,
                ambiente=cls.sala_101,
                estado_conservacao="DANIFICADO" if i < 3 else "BOM"
            )

        # 3. Configurar Financeiro
        # Faturas para alunos da Turma B (10 alunos * 500 = 5000 faturado vs 7500 custo -> deficitária)
        for aluno in cls.turma_b.alunos.all():
            Fatura.objects.create(
                aluno=aluno,
                valor=Decimal("500.00"),
                status="PAGO",
                data_vencimento="2026-03-10"
            )

    def test_motor1_enturmacao_diagnostico(self):
        """Verifica identificação correta de turmas sublotadas e assimetrias."""
        diag = diagnosticar_enturmacao(ano=2026)
        self.assertEqual(diag["total_turmas_avaliadas"], 2)
        self.assertEqual(diag["total_sublotadas"], 1)  # Turma B (10 alunos < 15)

        # Verifica se detectou o desbalanceamento (20 vs 10 = delta de 10 >= 8)
        self.assertTrue(len(diag["desbalanceamentos"]) >= 1)
        desbalanceamento = diag["desbalanceamentos"][0]
        self.assertEqual(desbalanceamento["delta_alunos"], 10)
        self.assertEqual(desbalanceamento["sugestao_remanejamento"], 5)

    def test_motor1_geracao_proposta_human_in_the_loop(self):
        """Verifica se o Motor 1 gera PropostaDecisao PENDENTE com justificativa."""
        propostas = gerar_propostas_enturmacao(ano=2026, persistir=True)
        self.assertTrue(len(propostas) >= 1)
        prop = propostas[0]
        self.assertEqual(prop.status, "PENDENTE")
        self.assertEqual(prop.tipo, "ENTURMACAO")
        self.assertIn("1o Ano", prop.titulo)
        self.assertTrue(len(prop.justificativa) > 30)

    def test_motor2_infraestrutura_diagnostico(self):
        """Verifica cálculo determinístico de índice de avaria na Sala 101."""
        diag = diagnosticar_infraestrutura()
        self.assertEqual(diag["total_ambientes"], 1)
        self.assertEqual(diag["total_patrimonio"], 10)
        self.assertEqual(diag["itens_avariados"], 3)
        self.assertAlmostEqual(diag["indice_avaria_global_pct"], 30.0, places=1)

    def test_motor2_geracao_proposta_infraestrutura(self):
        """Verifica se o Motor 2 gera proposta de reparo patrimonial quando avaria > 15%."""
        propostas = gerar_propostas_infraestrutura(persistir=True)
        self.assertTrue(len(propostas) >= 1)
        prop = propostas[0]
        self.assertEqual(prop.tipo, "INFRAESTRUTURA")
        self.assertEqual(prop.status, "PENDENTE")
        self.assertIn("Sala 101", prop.titulo)

    def test_motor3_financeiro_diagnostico(self):
        """Verifica cálculo determinístico de Break-Even e detecção de déficit."""
        diag = diagnosticar_financeiro(ano=2026)
        self.assertEqual(diag["break_even_alunos_por_turma"], BREAK_EVEN_ALUNOS)
        # Turma B tem 10 alunos (< 15) -> deve ser classificada como deficitária
        self.assertTrue(len(diag["turmas_deficitarias"]) >= 1)
        turma_def = next(t for t in diag["turmas_deficitarias"] if t["turma_id"] == self.turma_b.id)
        self.assertEqual(turma_def["alunos_faltantes_breakeven"], 5)  # 15 - 10 = 5

    def test_motor3_geracao_proposta_financeira(self):
        """Verifica se o Motor 3 gera proposta PENDENTE para turmas deficitárias."""
        propostas = gerar_propostas_financeiro(ano=2026, persistir=True)
        self.assertTrue(len(propostas) >= 1)
        prop = propostas[0]
        self.assertEqual(prop.tipo, "FINANCEIRO")
        self.assertEqual(prop.status, "PENDENTE")
        self.assertIn("Sustentabilidade", prop.titulo)

