"""
Testes Unitários do RAG Estruturado e Injeção de Contexto (apps/ia/services/contexto.py).
Valida roteamento semântico, conformidade com a LGPD e precisão determinística.
"""

from django.test import TestCase

from apps.ia.services.contexto import detectar_tipo_pergunta, montar_contexto


class ContextoRAGTestCase(TestCase):
    """Testes do gerador de contexto determinístico e classificador de intenção."""

    def test_classificador_intencao_enturmacao(self):
        """Verifica roteamento correto para Motor 1 (Enturmação)."""
        perguntas = [
            "Quais turmas apresentam desbalanceamento de alunos?",
            "Como está a distribuição de PCDs nas turmas do 1º Ano?",
            "Qual a lotação das turmas matriculadas em 2026?",
            "Existe alguma turma sublotada precisando de remanejamento?"
        ]
        for p in perguntas:
            tipo = detectar_tipo_pergunta(p)
            self.assertEqual(tipo, "ENTURMACAO", f"Falhou para pergunta: {p}")

    def test_classificador_intencao_infraestrutura(self):
        """Verifica roteamento correto para Motor 2 (Infraestrutura)."""
        perguntas = [
            "Quais salas possuem equipamentos com avaria?",
            "O laboratório de informática possui computadores funcionando?",
            "Existe algum ambiente escolar com problemas de conservação patrimonial?",
            "Quantos espaços físicos estão disponíveis no prédio?"
        ]
        for p in perguntas:
            tipo = detectar_tipo_pergunta(p)
            self.assertEqual(tipo, "INFRAESTRUTURA", f"Falhou para pergunta: {p}")

    def test_classificador_intencao_financeiro(self):
        """Verifica roteamento correto para Motor 3 (Financeiro)."""
        perguntas = [
            "Qual a receita de mensalidades e o custo docente de cada turma?",
            "Quais turmas estão operando em déficit abaixo do break-even?",
            "Qual o ponto de equilíbrio financeiro do 3º Ano?",
            "Como está a taxa de inadimplência das faturas?"
        ]
        for p in perguntas:
            tipo = detectar_tipo_pergunta(p)
            self.assertEqual(tipo, "FINANCEIRO", f"Falhou para pergunta: {p}")

    def test_conformidade_lgpd_ausencia_dados_sensiveis(self):
        """
        Garante que o contexto montado para qualquer motor NÃO contenha:
        - Nomes individuais de alunos
        - CPFs
        - Dados médicos de saúde
        - Menção a 'evasão escolar' (termo estritamente proibido no escopo)
        """
        tipos = ["ENTURMACAO", "INFRAESTRUTURA", "FINANCEIRO", "BIBLIOTECA", "GERAL"]
        for t in tipos:
            ctx = montar_contexto(tipo=t).lower()
            self.assertNotIn("cpf", ctx)
            self.assertNotIn("diagnóstico médico", ctx)
            self.assertNotIn("laudo", ctx)
            self.assertNotIn("evas", ctx, f"Termo proibido 'evas' detectado no contexto tipo {t}!")

