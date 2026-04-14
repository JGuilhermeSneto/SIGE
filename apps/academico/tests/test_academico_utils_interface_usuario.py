from django.test import TestCase
from unittest.mock import patch, MagicMock
from datetime import date
from apps.academico.utils.interface_usuario import gerar_calendario


class InterfaceUsuarioUtilsTest(TestCase):
    @patch('apps.calendario.models.calendario.EventoCalendario.objects.filter')
    def test_gerar_calendario_sem_eventos(self, mock_filter):
        mock_filter.return_value = []

        calendario = gerar_calendario(2023, 10)

        self.assertIsInstance(calendario, list)
        self.assertGreater(len(calendario), 0)
        # Verificar se tem dias do mês
        dias_outubro = [d for d in calendario if not d['vazio']]
        self.assertGreaterEqual(len(dias_outubro), 28)

    @patch('apps.calendario.models.calendario.EventoCalendario.objects.filter')
    def test_gerar_calendario_com_eventos(self, mock_filter):
        mock_evento = MagicMock()
        mock_evento.data = date(2023, 10, 16)  # Segunda-feira
        mock_evento.tipo = 'FERIADO'
        mock_evento.descricao = 'Dia das Crianças'
        mock_filter.return_value = [mock_evento]

        calendario = gerar_calendario(2023, 10)

        dia_16 = next((d for d in calendario if d['numero'] == 16 and not d['vazio']), None)
        self.assertIsNotNone(dia_16)
        self.assertEqual(dia_16['tipo'], 'FERIADO')
        self.assertEqual(dia_16['descricao'], 'Dia das Crianças')