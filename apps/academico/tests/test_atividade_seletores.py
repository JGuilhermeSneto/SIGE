"""
Testes para apps.academico.selectors.atividade_seletores.

Cobre os três métodos estáticos de AtividadeSeletores:
- buscar_atividade_com_questoes
- buscar_entregas_por_atividade
- buscar_entrega_detalhada
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.academico.models import (
    Alternativa,
    AtividadeProfessor,
    Disciplina,
    EntregaAtividade,
    Questao,
    Turma,
)
from apps.academico.selectors.atividade_seletores import AtividadeSeletores
from apps.usuarios.models.perfis import Aluno, Professor

User = get_user_model()


class AtividadeSeletoresTest(TestCase):
    """Suite de testes para AtividadeSeletores."""

    def setUp(self):
        professor_user = User.objects.create_user(
            username="prof_sel", password="pass", email="prof_sel@test.com"
        )
        self.professor = Professor.objects.create(
            user=professor_user,
            nome_completo="Professor Seletor",
            cpf="321.654.987-00",
            data_nascimento="1980-05-05",
        )

        self.turma = Turma.objects.create(nome="2B", turno="manha", ano=2024)

        aluno_user = User.objects.create_user(
            username="aluno_sel", password="pass", email="aluno_sel@test.com"
        )
        self.aluno = Aluno.objects.create(
            user=aluno_user,
            nome_completo="Aluno Seletor",
            cpf="444.555.666-77",
            data_nascimento="2011-07-20",
            turma=self.turma,
        )

        self.disciplina = Disciplina.objects.create(
            nome="Ciências",
            professor=self.professor,
            turma=self.turma,
        )

        self.atividade = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Atividade Seletores",
            tipo="ATIVIDADE",
            data=timezone.now().date(),
            prazo_final=timezone.now() + timedelta(days=3),
        )

        # Questão objetiva com alternativas
        self.questao = Questao.objects.create(
            atividade=self.atividade,
            texto="Questão de seletor",
            tipo="OBJETIVA",
            valor=2.0,
            ordem=1,
        )
        self.alt_correta = Alternativa.objects.create(
            questao=self.questao, texto="Sim", eh_correta=True
        )
        Alternativa.objects.create(
            questao=self.questao, texto="Não", eh_correta=False
        )

        # Entrega do aluno
        self.entrega = EntregaAtividade.objects.create(
            aluno=self.aluno,
            atividade=self.atividade,
            status="ENTREGUE",
        )

    # ------------------------------------------------------------------
    # buscar_atividade_com_questoes
    # ------------------------------------------------------------------
    def test_buscar_atividade_com_questoes_retorna_atividade_correta(self):
        atividade = AtividadeSeletores.buscar_atividade_com_questoes(self.atividade.id)
        self.assertEqual(atividade.id, self.atividade.id)
        self.assertEqual(atividade.titulo, "Atividade Seletores")

    def test_buscar_atividade_com_questoes_prefetch_questoes(self):
        """O prefetch deve funcionar: questões e alternativas acessíveis sem queries extras."""
        atividade = AtividadeSeletores.buscar_atividade_com_questoes(self.atividade.id)
        # Acessando através do cache de prefetch — não deve levantar exceção
        questoes = list(atividade.questoes.all())
        self.assertEqual(len(questoes), 1)
        alternativas = list(questoes[0].alternativas.all())
        self.assertEqual(len(alternativas), 2)

    def test_buscar_atividade_com_questoes_levanta_erro_para_id_invalido(self):
        from apps.academico.models.academico import AtividadeProfessor
        with self.assertRaises(AtividadeProfessor.DoesNotExist):
            AtividadeSeletores.buscar_atividade_com_questoes(99999)

    # ------------------------------------------------------------------
    # buscar_entregas_por_atividade
    # ------------------------------------------------------------------
    def test_buscar_entregas_por_atividade_retorna_entrega(self):
        entregas = AtividadeSeletores.buscar_entregas_por_atividade(self.atividade.id)
        self.assertEqual(entregas.count(), 1)
        self.assertEqual(entregas.first().aluno, self.aluno)

    def test_buscar_entregas_por_atividade_sem_entregas_retorna_queryset_vazio(self):
        atividade2 = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Atividade sem entrega",
            tipo="TRABALHO",
            data=timezone.now().date(),
            prazo_final=timezone.now() + timedelta(days=1),
        )
        entregas = AtividadeSeletores.buscar_entregas_por_atividade(atividade2.id)
        self.assertEqual(entregas.count(), 0)

    def test_buscar_entregas_por_atividade_ordenado_por_nome(self):
        """Com múltiplos alunos, resultado deve estar ordenado pelo nome_completo."""
        u2 = User.objects.create_user(username="aluno_z", password="pass")
        aluno2 = Aluno.objects.create(
            user=u2,
            nome_completo="Zélia Aluno",
            cpf="777.888.999-00",
            data_nascimento="2012-01-01",
            turma=self.turma,
        )
        EntregaAtividade.objects.create(
            aluno=aluno2, atividade=self.atividade, status="ENTREGUE"
        )

        entregas = AtividadeSeletores.buscar_entregas_por_atividade(self.atividade.id)
        nomes = list(entregas.values_list("aluno__nome_completo", flat=True))
        self.assertEqual(nomes, sorted(nomes))

    # ------------------------------------------------------------------
    # buscar_entrega_detalhada
    # ------------------------------------------------------------------
    def test_buscar_entrega_detalhada_retorna_entrega_correta(self):
        entrega = AtividadeSeletores.buscar_entrega_detalhada(self.entrega.id)
        self.assertEqual(entrega.id, self.entrega.id)
        self.assertEqual(entrega.aluno, self.aluno)

    def test_buscar_entrega_detalhada_levanta_erro_para_id_invalido(self):
        with self.assertRaises(EntregaAtividade.DoesNotExist):
            AtividadeSeletores.buscar_entrega_detalhada(99999)

    def test_buscar_entrega_detalhada_tem_atividade_prefetchada(self):
        entrega = AtividadeSeletores.buscar_entrega_detalhada(self.entrega.id)
        # atividade e questoes devem ser acessíveis
        self.assertEqual(entrega.atividade.id, self.atividade.id)
        questoes = list(entrega.atividade.questoes.all())
        self.assertGreater(len(questoes), 0)
