from django.test import SimpleTestCase
from core.templatetags.custom_tags import get_item, has_attr


class CustomTagsTest(SimpleTestCase):

    # 🔹 get_item
    def test_get_item_existente(self):
        d = {"a": 1}
        self.assertEqual(get_item(d, "a"), 1)

    def test_get_item_inexistente(self):
        d = {"a": 1}
        self.assertIsNone(get_item(d, "b"))

    def test_get_item_dict_vazio(self):
        self.assertIsNone(get_item({}, "a"))

    # 🔹 has_attr
    def test_has_attr_true(self):
        class Obj:
            x = 10

        self.assertTrue(has_attr(Obj(), "x"))

    def test_has_attr_false(self):
        class Obj:
            pass

        self.assertFalse(has_attr(Obj(), "y"))

    def test_has_attr_builtin(self):
        self.assertTrue(has_attr("abc", "upper"))