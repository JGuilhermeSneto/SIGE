import importlib
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

class NotasUrlsTest(SimpleTestCase):

    def test_admin_url(self):
        """Testa se a URL do admin está acessível"""
        resolver = resolve("/admin/")
        # O admin do Django geralmente resolve para 'admin:index'
        self.assertEqual(resolver.app_name, "admin")

    def test_core_root(self):
        """
        CORREÇÃO: Como não há uma rota para '/', testamos a rota de login 
        ou qualquer outra que seja a 'entrada' do seu sistema.
        """
        # Se você quer testar a raiz e ela não existe, o teste deve esperar 404
        # Mas o ideal é testar uma URL que existe, como '/login/'
        url = reverse('login') # Isso busca a URL nomeada 'login'
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'login')

    def test_url_invalida(self):
        """Testa se uma URL inexistente levanta 404 corretamente"""
        with self.assertRaises(Resolver404):
            resolve("/nao-existe-mesmo-123/")

    @override_settings(DEBUG=True)
    def test_static_urls_debug_true(self):
        """Testa se as URLs de Media são adicionadas quando DEBUG=True"""
        import notas.urls
        importlib.reload(notas.urls)
        patterns = notas.urls.urlpatterns

        # Verifica se existe algum padrão que contenha o caminho de MEDIA
        media_path = settings.MEDIA_URL.strip("/")
        found = any(media_path in str(p.pattern) for p in patterns)

        self.assertTrue(found, f"Media URL '{media_path}' não encontrada no urlpatterns com DEBUG=True")

    @override_settings(DEBUG=False)
    def test_static_urls_debug_false(self):
        """Testa se as URLs de Media NÃO são adicionadas quando DEBUG=False"""
        import notas.urls
        importlib.reload(notas.urls)
        patterns = notas.urls.urlpatterns

        media_path = settings.MEDIA_URL.strip("/")
        found = any(media_path in str(p.pattern) for p in patterns)

        self.assertFalse(found, f"Media URL '{media_path}' foi encontrada mesmo com DEBUG=False")

    def tearDown(self):
        """Garante que o estado das URLs volte ao normal após os testes de DEBUG"""
        import notas.urls
        importlib.reload(notas.urls)