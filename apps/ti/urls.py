from django.urls import path

from apps.seguranca.views.dashboard import SecurityDashboardView

from . import views

app_name = "ti"

urlpatterns = [
    path("", views.painel_ti, name="painel"),
    path("seguranca/", SecurityDashboardView.as_view(), name="seguranca"),
    path("operacoes/", views.operacoes_ti, name="operacoes"),
    path("documentacao/", views.documentacao_ti, name="documentacao"),
]
