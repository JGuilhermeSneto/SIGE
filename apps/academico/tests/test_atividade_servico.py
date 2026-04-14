from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.academico.models.academico import (
    Alternativa,
    AtividadeProfessor,
    Disciplina,
    EntregaAtividade,
    Questao,
    RespostaAluno,
    Turma,
)
from apps.academico.services.atividade_servico import AtividadeServico
from apps.usuarios.models.perfis import Aluno, Professor

User = get_user_model()


class AtividadeServicoTest(TestCase):
    def setUp(self):
        self.professor_user = User.objects.create_user(
            username="professor", email="professor@example.com", password="password123"
        )
        self.professor = Professor.objects.create(
            user=self.professor_user,
            nome_completo="Professor Teste",
            cpf="123.456.789-10",
            data_nascimento="1980-01-01",
        )

        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)

        self.aluno_user = User.objects.create_user(
            username="aluno", email="aluno@example.com", password="password123"
        )
        self.aluno = Aluno.objects.create(
            user=self.aluno_user,
            nome_completo="Aluno Teste",
            cpf="111.222.333-44",
            data_nascimento="2010-01-01",
            turma=self.turma,
        )

        self.disciplina = Disciplina.objects.create(
            nome="Matemática",
            professor=self.professor,
            turma=self.turma,
        )

        self.atividade = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Atividade 1",
            tipo="ATIVIDADE",
            data=timezone.now().date(),
            prazo_final=timezone.now() + timedelta(days=1),
        )

    def test_processar_entrega_aluno_salva_entrega_com_respostas(self):
        questao_obj = Questao.objects.create(
            atividade=self.atividade,
            texto="Qual é a cor do céu?",
            tipo="OBJETIVA",
            valor=2.0,
            ordem=1,
        )
        alternativa_correta = Alternativa.objects.create(
            questao=questao_obj,
            texto="Azul",
            eh_correta=True,
        )
        Alternativa.objects.create(
            questao=questao_obj,
            texto="Verde",
            eh_correta=False,
        )

        questao_disc = Questao.objects.create(
            atividade=self.atividade,
            texto="Explique por que o céu é azul.",
            tipo="DISCURSIVA",
            valor=3.0,
            ordem=2,
        )

        data_post = {
            "comentario": "Entrega com resposta e arquivo.",
            f"questao_{questao_obj.id}": str(alternativa_correta.id),
            f"questao_{questao_disc.id}": "Porque a atmosfera dispersa a luz azul.",
        }
        arquivos = {
            "arquivo": SimpleUploadedFile(
                "resposta.txt", b"Conteudo da entrega.", content_type="text/plain"
            )
        }

        entrega = AtividadeServico.processar_entrega_aluno(
            self.aluno, self.atividade.id, data_post, arquivos
        )

        self.assertEqual(entrega.status, "ENTREGUE")
        self.assertEqual(entrega.comentario_aluno, "Entrega com resposta e arquivo.")
        self.assertTrue(entrega.arquivo)
        self.assertTrue(entrega.arquivo.name.startswith("entregas/atividades/resposta_"))
        self.assertTrue(entrega.arquivo.name.endswith(".txt"))
        self.assertEqual(entrega.respostas.count(), 2)

        resposta_obj = entrega.respostas.get(questao=questao_obj)
        self.assertEqual(resposta_obj.alternativa_escolhida, alternativa_correta)

        resposta_disc = entrega.respostas.get(questao=questao_disc)
        self.assertEqual(resposta_disc.texto_resposta, "Porque a atmosfera dispersa a luz azul.")

    def test_processar_entrega_aluno_levanta_erro_quando_prazo_terminado(self):
        atividade_expirada = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Atividade expirada",
            tipo="ATIVIDADE",
            data=timezone.now().date(),
            prazo_final=timezone.now() - timedelta(hours=1),
        )

        with self.assertRaises(ValueError):
            AtividadeServico.processar_entrega_aluno(
                self.aluno, atividade_expirada.id, {}, {}
            )

    def test_salvar_banco_questoes_cria_questoes_e_alternativas(self):
        data_post = {
            "questoes_count": "2",
            "questao_texto_1": "Qual o maior planeta?",
            "questao_tipo_1": "OBJETIVA",
            "questao_valor_1": "2.5",
            "alt_1_1": "Júpiter",
            "alt_1_2": "Marte",
            "alt_1_3": "Vênus",
            "alt_1_4": "Terra",
            "alt_1_5": "Saturno",
            "correta_1": "1",
            "questao_texto_2": "Descreva o sistema solar.",
            "questao_tipo_2": "DISCURSIVA",
            "questao_valor_2": "3",
        }

        AtividadeServico.salvar_banco_questoes(self.atividade, data_post)

        self.assertEqual(self.atividade.questoes.count(), 2)

        questao_obj = self.atividade.questoes.get(ordem=1)
        self.assertEqual(questao_obj.tipo, "OBJETIVA")
        self.assertEqual(questao_obj.alternativas.count(), 5)
        self.assertTrue(
            questao_obj.alternativas.filter(texto="Júpiter", eh_correta=True).exists()
        )

        questao_disc = self.atividade.questoes.get(ordem=2)
        self.assertEqual(questao_disc.tipo, "DISCURSIVA")
        self.assertEqual(questao_disc.valor, Decimal("3"))

    def test_finalizar_correcao_atribui_pontos_e_cria_nota(self):
        questao_obj = Questao.objects.create(
            atividade=self.atividade,
            texto="Marque a resposta correta.",
            tipo="OBJETIVA",
            valor=1.0,
            ordem=1,
        )
        alternativa_correta = Alternativa.objects.create(
            questao=questao_obj,
            texto="Certo",
            eh_correta=True,
        )

        questao_disc = Questao.objects.create(
            atividade=self.atividade,
            texto="Explique o funcionamento.",
            tipo="DISCURSIVA",
            valor=2.5,
            ordem=2,
        )

        entrega = EntregaAtividade.objects.create(
            aluno=self.aluno,
            atividade=self.atividade,
            status="ENTREGUE",
        )

        RespostaAluno.objects.create(
            entrega=entrega,
            questao=questao_obj,
            alternativa_escolhida=alternativa_correta,
        )
        RespostaAluno.objects.create(
            entrega=entrega,
            questao=questao_disc,
        )

        data_post = {
            f"feedback_{questao_obj.id}": "Muito bom.",
            f"pontos_{questao_disc.id}": "2,5",
            "obs_geral": "Correção concluída.",
            "status": "CORRIGIDO",
        }

        total_pontos = AtividadeServico.finalizar_correcao(entrega, data_post)

        self.assertAlmostEqual(float(total_pontos), 3.5, places=5)

        entrega.refresh_from_db()
        self.assertEqual(entrega.status, "CORRIGIDO")
        self.assertEqual(entrega.feedback_professor, "Correção concluída.")

        nota = self.atividade.notas_alunos.get(aluno=self.aluno)
        self.assertEqual(float(nota.valor), 3.5)
        self.assertEqual(nota.observacao, "Correção concluída.")

    def test_salvar_banco_questoes_levanta_erro_para_prova_sem_questoes(self):
        atividade_prova = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Prova 1",
            tipo="PROVA",
            data=timezone.now().date() - timedelta(days=1),
        )

        data_post = {"questoes_count": "0"}
        with self.assertRaises(ValueError) as cm:
            AtividadeServico.salvar_banco_questoes(atividade_prova, data_post)

        self.assertIn("Provas precisam ter ao menos uma questão de gabarito", str(cm.exception))

    def test_atividade_prova_exibe_gabarito_apos_data(self):
        atividade_prova = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Prova 2",
            tipo="PROVA",
            data=timezone.now().date() - timedelta(days=1),
        )

        questao = Questao.objects.create(
            atividade=atividade_prova,
            texto="Qual é a soma?",
            tipo="OBJETIVA",
            valor=2.0,
            ordem=1,
        )
        Alternativa.objects.create(questao=questao, texto="4", eh_correta=True)
        Alternativa.objects.create(questao=questao, texto="5", eh_correta=False)

        self.assertTrue(atividade_prova.possui_gabarito)
        self.assertTrue(atividade_prova.prazo_encerrado)
        self.assertTrue(atividade_prova.exibir_gabarito_para_aluno)

    def test_atividade_exibe_gabarito_quando_liberado_manual(self):
        atividade = AtividadeProfessor.objects.create(
            disciplina=self.disciplina,
            titulo="Atividade com liberação manual",
            tipo="ATIVIDADE",
            data=timezone.now().date(),
            prazo_final=timezone.now() + timedelta(days=2),
            gabarito_liberado=True,
            gabarito_liberado_em=timezone.now(),
        )

        questao = Questao.objects.create(
            atividade=atividade,
            texto="Quanto é 2 + 2?",
            tipo="OBJETIVA",
            valor=1.0,
            ordem=1,
        )
        Alternativa.objects.create(questao=questao, texto="4", eh_correta=True)
        Alternativa.objects.create(questao=questao, texto="5", eh_correta=False)

        self.assertTrue(atividade.possui_gabarito)
        self.assertFalse(atividade.prazo_encerrado)
        self.assertTrue(atividade.exibir_gabarito_para_aluno)
