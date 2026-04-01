from django.test import SimpleTestCase

from core.templatetags.get_item import get_item


class GetItemTest(SimpleTestCase):

    # 🔴 1. dict vazio / None
    def test_dict_none(self):
        self.assertIsNone(get_item(None, "a"))

    def test_dict_vazio(self):
        self.assertIsNone(get_item({}, "a"))

    # 🟢 2. chave direta
    def test_chave_direta(self):
        d = {"a": 10}
        self.assertEqual(get_item(d, "a"), 10)

    # 🟡 3. chave como int (key string → int)
    def test_chave_int_convertida(self):
        d = {1: "valor"}
        self.assertEqual(get_item(d, "1"), "valor")

    # 🔵 4. chave como string fallback
    def test_chave_string_fallback(self):
        d = {"1": "valor"}
        self.assertEqual(get_item(d, 1), "valor")

    # ⚫ 5. chave inexistente
    def test_chave_inexistente(self):
        d = {"a": 1}
        self.assertIsNone(get_item(d, "b"))

    # ⚠️ 6. key que não pode virar int
    def test_key_nao_convertivel(self):
        d = {"x": 99}
        self.assertIsNone(get_item(d, "abc"))

    # 🔁 7. key já int direto
    def test_key_int_direto(self):
        d = {2: "ok"}
        self.assertEqual(get_item(d, 2), "ok")
