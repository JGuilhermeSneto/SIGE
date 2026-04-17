"""
URLconf raiz do SIGE — mapa de rotas HTTP do site inteiro.

O que é: lista de ``path()`` que o Django percorre na ordem até achar
uma view que atenda à URL.

Como funciona:
- ``admin/`` → painel administrativo do Django.
- ``''`` (raiz) → todas as URLs do app ``usuarios`` (login, painéis, etc.).
- ``academico/`` → turmas, disciplinas, notas, frequência, relatórios.
- ``calendario/`` → calendário acadêmico e eventos.
- ``api/ping/`` → JSON de verificação para o front-end (Vite/React).
- ``api/dashboard/resumo/`` → totais e lista de turmas (dados do banco).
Em modo DEBUG, acrescenta servir arquivos de ``MEDIA`` (uploads).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from config.api_views import dashboard_resumo, ping
from config.jwt_views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from apps.comunicacao.api import ComunicadoViewSet
from apps.academico.api import NotificacaoViewSet
from apps.biblioteca.api import BibliotecaViewSet, MeusEmprestimosViewSet
from apps.saude.api import SaudeViewSet

router = DefaultRouter()
router.register(r'comunicados', ComunicadoViewSet, basename='api-comunicados')
router.register(r'notificacoes', NotificacaoViewSet, basename='api-notificacoes')
router.register(r'biblioteca/acervo', BibliotecaViewSet, basename='api-biblioteca-acervo')
router.register(r'biblioteca/meus-livros', MeusEmprestimosViewSet, basename='api-biblioteca-meus-livros')
router.register(r'saude/minha-ficha', SaudeViewSet, basename='api-saude-ficha')

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("api/ping/", ping, name="api-ping"),
    path("api/dashboard/resumo/", dashboard_resumo, name="api-dashboard-resumo"),
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("", include("apps.usuarios.urls")),
    path("academico/", include("apps.academico.urls")),
    path("calendario/", include("apps.calendario.urls")),
    path("documentos/", include("apps.documentos.urls")),
    path("comunicacao/", include("apps.comunicacao.urls")),
    path("infraestrutura/", include("apps.infraestrutura.urls")),
    path("saude/", include("apps.saude.urls")),
    path("biblioteca/", include("apps.biblioteca.urls")),
    path("dashboards/", include("apps.dashboards.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
