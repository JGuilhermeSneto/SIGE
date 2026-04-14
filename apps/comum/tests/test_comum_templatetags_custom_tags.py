from django.test import TestCase
from apps.comum.templatetags.custom_tags import get_item, has_attr, unlocalize


class CustomTagsTest(TestCase):
    def test_get_item_com_chave_existente(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual(get_item(d, 'a'), 1)

    def test_get_item_com_chave_inexistente(self):
        d = {'a': 1}
        self.assertIsNone(get_item(d, 'b'))

    def test_get_item_com_dicionario_none(self):
        self.assertIsNone(get_item(None, 'a'))

    def test_has_attr_verdadeiro(self):
        class Obj:
            attr = True
        obj = Obj()
        self.assertTrue(has_attr(obj, 'attr'))

    def test_has_attr_falso(self):
        class Obj:
            pass
        obj = Obj()
        self.assertFalse(has_attr(obj, 'attr'))

    def test_unlocalize_numero(self):
        self.assertEqual(unlocalize(7.5), '7.5')

    def test_unlocalize_string(self):
        self.assertEqual(unlocalize('teste'), 'teste')