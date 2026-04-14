"""
URLconf do app ``usuarios`` — agrega rotas de autenticação e de perfis/painéis.

O que é: ponto único incluído na raiz do site (``config.urls``); repassa
para submódulos ``autenticacao`` e ``perfis``.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("apps.usuarios.urls.autenticacao")),
    path("", include("apps.usuarios.urls.perfis")),
]
