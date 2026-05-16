from django.urls import path

from apps.seguranca.views.dashboard import SecurityDashboardView

from . import views

app_name = "ti"

urlpatterns = [
    path("", views.painel_ti, name="painel"),
    path("seguranca/", SecurityDashboardView.as_view(), name="seguranca"),
    path("infraestrutura/", views.infraestrutura_ti, name="infraestrutura"),
    path("infraestrutura/executar/<str:script_id>/", views.executar_script, name="executar_script"),
    path("backups/", views.gestao_backups, name="gestao_backups"),
    path("backups/disparar/", views.disparar_backup, name="disparar_backup"),
    path("documentacao/", views.documentacao_ti, name="documentacao"),
    path("api-docs/", views.documentacao_api, name="api_docs"),
    path("bugs/", views.gestao_bugs, name="gestao_bugs"),
    path("bugs/<int:bug_id>/atualizar/", views.atualizar_status_bug, name="atualizar_status_bug"),
    path("api/lgpd-logs/", views.api_logs_lgpd, name="api_lgpd_logs"),
    path("flags/", views.gestao_flags, name="gestao_flags"),
    path("flags/nova/", views.criar_flag, name="criar_flag"),
    path("flags/<int:flag_id>/alternar/", views.alternar_flag, name="alternar_flag"),
    path("api/js-error/", views.api_js_error, name="api_js_error"),
    path("api/metrics/", views.api_ti_metrics, name="api_metrics"),
    path("erro/<int:erro_id>/correlacao/", views.logs_correlacionados, name="correlacao_logs"),
    
    # Novas Interfaces de Gestão
    path("soc/", views.painel_soc, name="soc"),
    path("soc/erro/<int:erro_id>/resolver/", views.resolver_erro, name="resolver_erro"),
    path("soc/bloquear-ip/", views.bloquear_ip, name="bloquear_ip"),
    path("soc/desbloquear-ip/<int:blacklist_id>/", views.desbloquear_ip, name="desbloquear_ip"),
    path("parametros/", views.gestao_parametros, name="gestao_parametros"),
    path("avisos/", views.gestao_avisos, name="gestao_avisos"),
    path("avisos/novo/", views.criar_aviso, name="criar_aviso"),
    path("auditoria/", views.central_auditoria, name="central_auditoria"),
    
    # Placeholders para Expansão v7.3
    path("hub/<slug:modulo_slug>/", views.placeholder_ti, name="placeholder_modulo"),
    path("backups/download/<int:backup_id>/", views.download_backup, name="download_backup"),
]
