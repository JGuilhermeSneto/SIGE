from django.test import TestCase
from apps.comum.templatetags.get_item import get_item


class GetItemTest(TestCase):
    def test_get_item_com_chave_existente(self):
        d = {'x': 10, 'y': 20}
        self.assertEqual(get_item(d, 'x'), 10)

    def test_get_item_com_chave_inexistente(self):
        d = {'x': 10}
        self.assertIsNone(get_item(d, 'z'))

    def test_get_item_com_dicionario_none(self):
        self.assertIsNone(get_item(None, 'x'))