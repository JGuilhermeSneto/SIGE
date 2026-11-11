"""
Testes Unitários dos Modelos do Módulo ELISE IA.
Valida integridade relacional, conformidade LGPD e fluxo Human-in-the-Loop.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.ia.models import SessaoAssistente, MensagemAssistente, PropostaDecisao

User = get_user_model()


class EliseIAModelsTestCase(TestCase):
    """Testes unitários dos modelos do DSS ELISE IA."""

    def setUp(self):
        self.gestor = User.objects.create_user(
            username="gestor_teste_unit",
            password="senha_segura_123",
            first_name="Guilherme",
            last_name="Gestor"
        )

    def test_criacao_sessao_assistente(self):
        """Verifica se a SessaoAssistente é criada com defaults corretos."""
        sessao = SessaoAssistente.objects.create(
            usuario=self.gestor,
            titulo="Consulta sobre turmas do 1o Ano"
        )
        self.assertEqual(sessao.usuario, self.gestor)
        self.assertTrue(sessao.ativo)
        self.assertIn("1o Ano", str(sessao))

    def test_criacao_mensagem_assistente(self):
        """Verifica registro de mensagens com rastreabilidade de latência e contexto."""
        sessao = SessaoAssistente.objects.create(
            usuario=self.gestor,
            titulo="Sessão Auditoria"
        )
        msg_user = MensagemAssistente.objects.create(
            sessao=sessao,
            papel="user",
            conteudo="Qual a situação da Sala 101?",
            contexto_utilizado="[Infraestrutura] Total de ambientes: 7"
        )
        msg_ia = MensagemAssistente.objects.create(
            sessao=sessao,
            papel="assistant",
            conteudo="A Sala 101 possui 33% de avaria.",
            latencia_segundos=12.45
        )

        self.assertEqual(msg_user.papel, "user")
        self.assertEqual(msg_ia.papel, "assistant")
        self.assertEqual(msg_ia.latencia_segundos, 12.45)
        self.assertEqual(sessao.mensagens.count(), 2)

    def test_fluxo_human_in_the_loop_proposta_decisao(self):
        """
        Valida o princípio Human-in-the-Loop:
        1. Proposta é criada obrigatoriamente com status PENDENTE.
        2. Proposta contém justificativa explícita (Art. 20 LGPD).
        3. Aprovação requer registro de autoria humana e data de decisão.
        """
        proposta = PropostaDecisao.objects.create(
            tipo="ENTURMACAO",
            titulo="Remanejamento de Alunos do 1o Ano",
            descricao="Assimetria de 17 alunos entre 1oA e 1oB.",
            justificativa="Turma 1oA possui 29 alunos e 1oB possui 12 alunos.",
            dados_proposta={"origem": "1oA", "destino": "1oB", "quantidade": 8}
        )

        # 1. Deve iniciar PENDENTE
        self.assertEqual(proposta.status, "PENDENTE")
        self.assertIsNone(proposta.decidido_por)
        self.assertIsNone(proposta.decidido_em)

        # 2. Homologação pelo gestor humano
        proposta.status = "APROVADA"
        proposta.decidido_por = self.gestor
        proposta.decidido_em = timezone.now()
        proposta.observacao_gestor = "Aprovado conforme parecer da coordenação pedagógica."
        proposta.save()

        # 3. Verificação no banco
        proposta_recarregada = PropostaDecisao.objects.get(id=proposta.id)
        self.assertEqual(proposta_recarregada.status, "APROVADA")
        self.assertEqual(proposta_recarregada.decidido_por, self.gestor)
        self.assertIsNotNone(proposta_recarregada.decidido_em)
        self.assertIn("Aprovado conforme parecer", proposta_recarregada.observacao_gestor)

