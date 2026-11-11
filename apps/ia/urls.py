from django.urls import path
from . import views

app_name = "ia"

urlpatterns = [
    path("", views.dashboard_ia, name="dashboard"),
    path("relatorio/", views.relatorio_executivo_dss, name="relatorio"),
    path("status/", views.assistente_status, name="status"),
    path("status/detalhado/", views.StatusIAView.as_view(), name="status-detalhado"),
    path("chat/", views.AssistenteChatView.as_view(), name="chat"),
    path("propostas/", views.PropostaDecisaoListView.as_view(), name="propostas-lista"),
    path("propostas/<int:pk>/acao/", views.PropostaDecisaoAcaoView.as_view(), name="proposta-acao"),
]
