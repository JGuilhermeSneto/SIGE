from django.urls import path

from apps.seguranca.views.dashboard import SecurityDashboardView

from . import views

app_name = "ti"

urlpatterns = [
    path("", views.painel_ti, name="painel"),
    path("seguranca/", SecurityDashboardView.as_view(), name="seguranca"),
    path("operacoes/", views.operacoes_ti, name="operacoes"),
    path("documentacao/", views.documentacao_ti, name="documentacao"),
    path("api-docs/", views.documentacao_api, name="api_docs"),
    path("bugs/", views.gestao_bugs, name="gestao_bugs"),
    path("bugs/<int:bug_id>/atualizar/", views.atualizar_status_bug, name="atualizar_status_bug"),
]
