from django.test import SimpleTestCase
from core.templatetags import dict_get  # importa o módulo


class DictGetTest(SimpleTestCase):

    def test_chave_existente(self):
        d = {"a": 10}
        self.assertEqual(dict_get.get_item(d, "a"), 10)

    def test_chave_inexistente(self):
        d = {"a": 10}
        self.assertEqual(dict_get.get_item(d, "b"), "")

    def test_dict_none(self):
        self.assertEqual(dict_get.get_item(None, "a"), "")

    def test_nao_dict(self):
        self.assertEqual(dict_get.get_item("string", "a"), "")

    def test_dict_vazio(self):
        self.assertEqual(dict_get.get_item({}, "a"), "")