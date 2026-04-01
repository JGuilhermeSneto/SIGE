import importlib

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import resolve
from django.urls.exceptions import Resolver404


class NotasUrlsTest(SimpleTestCase):

    def test_admin_url(self):
        resolver = resolve("/admin/")
        self.assertEqual(resolver.view_name, "admin:index")

    def test_core_root(self):
        resolver = resolve("/")
        self.assertIsNotNone(resolver)

    def test_url_invalida(self):
        with self.assertRaises(Resolver404):
            resolve("/nao-existe/")

    @override_settings(DEBUG=True)
    def test_static_urls_debug_true(self):
        import notas.urls

        importlib.reload(notas.urls)

        patterns = notas.urls.urlpatterns

        found = False
        for p in patterns:
            if settings.MEDIA_URL.strip("/") in str(p.pattern):
                found = True

        self.assertTrue(found)

    @override_settings(DEBUG=False)
    def test_static_urls_debug_false(self):
        import notas.urls

        importlib.reload(notas.urls)

        patterns = notas.urls.urlpatterns

        found = False
        for p in patterns:
            if settings.MEDIA_URL.strip("/") in str(p.pattern):
                found = True

        # 🔥 aqui garantimos o outro branch
        self.assertFalse(found)
