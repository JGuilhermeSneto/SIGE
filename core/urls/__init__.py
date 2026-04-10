"""
URL initialization for the core app.
Combines all modularized URL patterns.
"""

from django.urls import path, include

urlpatterns = [
    path("", include("core.urls.autenticacao")),
    path("", include("core.urls.perfis")),
    path("", include("core.urls.academico")),
    path("", include("core.urls.desempenho")),
    path("", include("core.urls.calendario")),
]
