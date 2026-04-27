from django.test import TestCase
from unittest.mock import patch
from apps.academico.selectors.relatorios import get_metricas_gerais


class RelatoriosSelectorsTest(TestCase):
    @patch('apps.academico.selectors.relatorios.Aluno.objects')
    @patch('apps.academico.selectors.relatorios.Turma.objects')
    @patch('apps.academico.selectors.relatorios.Disciplina.objects')
    @patch('apps.academico.selectors.relatorios.User.objects')
    def test_get_metricas_gerais_retorna_dicionario_com_metricas(self, mock_user, mock_disciplina, mock_turma, mock_aluno):
        # Setup mocks
        mock_aluno.count.return_value = 100
        mock_turma.filter.return_value.count.return_value = 10
        mock_disciplina.filter.return_value.count.return_value = 20
        
        # User.objects.filter(...).count() chamado 2 vezes (Ativos, Inativos)
        mock_user.filter.return_value.count.side_effect = [50, 10]
        
        # Aluno.objects.filter(...).count() chamado 7 vezes:
        # 1. Ingressantes
        # 2. Ativos (Status)
        # 3. Evadidos (Status)
        # 4. Transferidos (Status)
        # 5. Formados (Status)
        # 6. Inativos (Status)
        # 7. Concluintes
        mock_aluno.filter.return_value.count.side_effect = [
            5,   # Ingressantes
            80,  # Ativos
            5,   # Evadidos
            2,   # Transferidos
            8,   # Formados
            5,   # Inativos
            12   # Concluintes
        ]

        metricas = get_metricas_gerais(2024, 10)

        self.assertIsInstance(metricas, dict)
        self.assertEqual(metricas['total_alunos'], 100)
        self.assertEqual(metricas['total_turmas'], 10)
        self.assertEqual(metricas['usuarios_ativos'], 50)
        self.assertEqual(metricas['ingressantes'], 5)
        self.assertEqual(metricas['alunos_ativos'], 80)
        self.assertEqual(metricas['alunos_evadidos'], 5)
        self.assertEqual(metricas['taxa_evasao'], 5.0) # (5 / 100) * 100
        self.assertEqual(metricas['concluintes'], 12)