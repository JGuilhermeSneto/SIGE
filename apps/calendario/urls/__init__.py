"""
URLconf do app ``calendario`` — rotas sob ``/calendario/``.

O que é: delega ao módulo ``calendario.urls.calendario`` as paths de
visualização e gestão de eventos.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("apps.calendario.urls.calendario")),
]
