from django.urls import path
from ..views import seguranca_acoes

urlpatterns = [
    path("bloquear-ip/<str:ip>/", seguranca_acoes.bloquear_ip, name="bloquear_ip"),
    path("desbloquear-ip/<int:ip_id>/", seguranca_acoes.desbloquear_ip, name="desbloquear_ip"),
    path("bloquear-usuario/<int:user_id>/", seguranca_acoes.bloquear_usuario, name="bloquear_usuario"),
    path("resolver-bug/<int:bug_id>/", seguranca_acoes.resolver_bug, name="resolver_bug"),
    path("encaminhar-ti/<int:bug_id>/", seguranca_acoes.encaminhar_ti, name="encaminhar_ti"),
    path("detalhe-bug/<int:bug_id>/", seguranca_acoes.detalhe_bug, name="detalhe_bug"),
    path("limpar-erros/", seguranca_acoes.limpar_logs_erro, name="limpar_erros"),
    path("reportar-bug/", seguranca_acoes.reportar_bug, name="reportar_bug"),
    path("toggle-manutencao/", seguranca_acoes.toggle_manutencao, name="toggle_manutencao"),
]
