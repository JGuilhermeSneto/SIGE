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
        mock_user.filter.return_value.count.side_effect = [50, 10]  # ativos, inativos
        mock_aluno.filter.return_value.count.side_effect = [5, 2]  # ingressantes, concluintes

        metricas = get_metricas_gerais(2024, 10)

        self.assertIsInstance(metricas, dict)
        self.assertEqual(metricas['total_alunos'], 100)
        self.assertEqual(metricas['total_turmas'], 10)
        self.assertEqual(metricas['total_disciplinas'], 20)
        self.assertEqual(metricas['usuarios_ativos'], 50)
        self.assertEqual(metricas['usuarios_inativos'], 10)
        self.assertEqual(metricas['ingressantes'], 5)
        self.assertEqual(metricas['concluintes'], 2)