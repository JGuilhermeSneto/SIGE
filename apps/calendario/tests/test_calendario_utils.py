from datetime import date
from django.test import SimpleTestCase
from apps.calendario.utils.calendario import (
    get_pascoa,
    get_feriados_nacionais,
    is_fim_semana,
    gerar_base_calendario,
)


class CalendarioUtilsTest(SimpleTestCase):
    def test_get_pascoa(self):
        # Datas conhecidas da Páscoa
        self.assertEqual(get_pascoa(2023), date(2023, 4, 9))
        self.assertEqual(get_pascoa(2024), date(2024, 3, 31))
        self.assertEqual(get_pascoa(2025), date(2025, 4, 20))

    def test_get_feriados_nacionais(self):
        feriados = get_feriados_nacionais(2023)
        self.assertEqual(feriados[date(2023, 1, 1)], "Confraternização Universal")
        self.assertEqual(feriados[date(2023, 12, 25)], "Natal")
        # Feriado móvel (Páscoa 2023 é 09/04, Sexta Santa é 07/04)
        self.assertEqual(feriados[date(2023, 4, 7)], "Sexta-feira Santa")

    def test_is_fim_semana(self):
        self.assertTrue(is_fim_semana(date(2023, 4, 8)))  # Sábado
        self.assertTrue(is_fim_semana(date(2023, 4, 9)))  # Domingo
        self.assertFalse(is_fim_semana(date(2023, 4, 10)))  # Segunda

    def test_gerar_base_calendario(self):
        base = gerar_base_calendario(2023)
        self.assertEqual(len(base), 365)

        # Testar um dia letivo comum
        self.assertEqual(base[date(2023, 4, 10)]["tipo"], "DI_LETIVO")

        # Testar um feriado
        self.assertEqual(base[date(2023, 1, 1)]["tipo"], "FERIADO")
        self.assertTrue(base[date(2023, 1, 1)]["aula_suspensa"])

        # Testar um final de semana
        self.assertEqual(base[date(2023, 4, 9)]["tipo"], "FIM_SEMANA")
        self.assertTrue(base[date(2023, 4, 9)]["aula_suspensa"])  # Domingo
