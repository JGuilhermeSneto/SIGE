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

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("api/ping/", ping, name="api-ping"),
    path("api/dashboard/resumo/", dashboard_resumo, name="api-dashboard-resumo"),
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include("apps.usuarios.urls")),
    path("academico/", include("apps.academico.urls")),
    path("calendario/", include("apps.calendario.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
