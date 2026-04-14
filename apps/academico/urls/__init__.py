"""
URLconf do app ``academico`` — rotas sob o prefixo ``/academico/``.

O que é: inclui cadastros acadêmicos, desempenho (notas/frequência) e
relatórios em sub-roteadores separados.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("apps.academico.urls.academico")),
    path("", include("apps.academico.urls.desempenho")),
    path("relatorios/", include("apps.academico.urls.relatorios")),
]
