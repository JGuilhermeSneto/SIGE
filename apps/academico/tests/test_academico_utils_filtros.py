from django.test import TestCase, RequestFactory
from apps.academico.utils.filtros import _get_anos_filtro, _get_ano_filtro_professor


class FiltrosUtilsTest(TestCase):
    def test_get_anos_filtro_com_ano_valido(self):
        anos_disponiveis = {2020, 2021, 2022}
        ano_selecionado = "2021"
        ano_atual = 2023

        ano_filtro, lista_anos = _get_anos_filtro(anos_disponiveis, ano_selecionado, ano_atual)

        self.assertEqual(ano_filtro, 2021)
        self.assertIn(2023, lista_anos)
        self.assertIn(2021, lista_anos)
        self.assertEqual(sorted(lista_anos, reverse=True), lista_anos)

    def test_get_anos_filtro_com_ano_invalido(self):
        anos_disponiveis = {2020, 2021}
        ano_selecionado = "invalido"
        ano_atual = 2022

        ano_filtro, lista_anos = _get_anos_filtro(anos_disponiveis, ano_selecionado, ano_atual)

        self.assertEqual(ano_filtro, 2022)
        self.assertIn(2022, lista_anos)

    def test_get_ano_filtro_professor_com_parametro(self):
        factory = RequestFactory()
        request = factory.get('/?ano=2021')
        request.session = {}
        anos_disponiveis = [2020, 2022]
        ano_atual = 2023

        ano_filtro, anos_list = _get_ano_filtro_professor(request, anos_disponiveis, ano_atual)

        self.assertEqual(ano_filtro, 2021)
        self.assertIn(2021, anos_list)

    def test_get_ano_filtro_professor_sem_parametro(self):
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}
        anos_disponiveis = [2020, 2022]
        ano_atual = 2023

        ano_filtro, anos_list = _get_ano_filtro_professor(request, anos_disponiveis, ano_atual)

        self.assertEqual(ano_filtro, 2023)
        self.assertIn(2023, anos_list)