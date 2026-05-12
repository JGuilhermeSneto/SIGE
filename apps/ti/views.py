from datetime import timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from apps.seguranca.models.blacklist import BlacklistIP
from apps.seguranca.models.bug_report import BugReport
from apps.seguranca.models.log_auditoria import LogAuditoria
from apps.seguranca.models.log_erro import LogErro
from apps.usuarios.utils.perfis import get_foto_perfil, get_nome_exibicao

from .utils.permissoes import (
    usuario_e_apenas_ti,
    usuario_tem_operacoes_ti,
    usuario_tem_painel_ti,
)


@login_required
@user_passes_test(usuario_tem_painel_ti)
@cache_page(300)  # Cache por 5 minutos
def painel_ti(request):
    """Visão geral da equipe de TI: links rápidos e status."""
    agora = timezone.now()
    ultimos_sete_dias = agora - timedelta(days=7)

    ti_status_cards = [
        {
            "titulo": "Bugs novos",
            "valor": BugReport.objects.filter(status="NOVO").count(),
            "descricao": "Relatórios novos aguardando triagem e priorização.",
        },
        {
            "titulo": "Erros recentes",
            "valor": LogErro.objects.filter(data_ocorrencia__gte=ultimos_sete_dias).count(),
            "descricao": "Erros registrados nos últimos 7 dias para investigação urgente.",
        },
        {
            "titulo": "IPs bloqueados",
            "valor": BlacklistIP.objects.filter(
                Q(expira_em__isnull=True) | Q(expira_em__gte=agora)
            ).count(),
            "descricao": "Endereços ativos na blacklist de segurança.",
        },
        {
            "titulo": "Acessos auditados",
            "valor": LogAuditoria.objects.filter(data_evento__gte=ultimos_sete_dias).select_related('usuario').count(),
            "descricao": "Entradas de auditoria geradas em rotinas sensíveis recentes.",
        },
    ]

    return render(
        request,
        "ti/painel.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "pode_operacoes": usuario_tem_operacoes_ti(request.user),
            "apenas_ti": usuario_e_apenas_ti(request.user),
            "ti_status_cards": ti_status_cards,
            "ultima_atualizacao": timezone.now(),
        },
    )


@login_required
@user_passes_test(usuario_tem_painel_ti)
def documentacao_ti(request):
    """Documentação interna e runbook para a equipe de TI."""
    return render(
        request,
        "ti/documentacao.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "pode_operacoes": usuario_tem_operacoes_ti(request.user),
            "apenas_ti": usuario_e_apenas_ti(request.user),
        },
    )


@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def operacoes_ti(request):
    """Rotinas avançadas (visível só com permissão de operações ou superusuário)."""
    operation_result = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "cleanup_logs_30":
            # Limpar logs com mais de 30 dias
            cutoff_date = timezone.now() - timedelta(days=30)
            deleted_logs = LogAuditoria.objects.filter(data_evento__lt=cutoff_date).delete()[0]
            deleted_errors = LogErro.objects.filter(data_ocorrencia__lt=cutoff_date).delete()[0]
            operation_result = f"Logs limpos:\n- Auditoria: {deleted_logs} registros\n- Erros: {deleted_errors} registros\n\nData de corte: {cutoff_date.date()}"

        elif action == "cleanup_logs_90":
            # Limpar logs com mais de 90 dias
            cutoff_date = timezone.now() - timedelta(days=90)
            deleted_logs = LogAuditoria.objects.filter(data_evento__lt=cutoff_date).delete()[0]
            deleted_errors = LogErro.objects.filter(data_ocorrencia__lt=cutoff_date).delete()[0]
            operation_result = f"Logs limpos:\n- Auditoria: {deleted_logs} registros\n- Erros: {deleted_errors} registros\n\nData de corte: {cutoff_date.date()}"

        elif action == "cleanup_sessions":
            # Limpar sessões expiradas
            from django.contrib.sessions.models import Session
            expired_sessions = Session.objects.filter(expire_date__lt=timezone.now()).delete()[0]
            operation_result = f"Sessões expiradas removidas: {expired_sessions}"

        elif action == "health_check":
            # Verificação básica de saúde
            from django.db import connection
            from django.core.cache import cache

            health_status = []

            # Verificar banco de dados
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                health_status.append("✅ Banco de dados: OK")
            except Exception as e:
                health_status.append(f"❌ Banco de dados: ERRO - {str(e)}")

            # Verificar cache
            try:
                cache.set("health_check", "ok", 10)
                cache_value = cache.get("health_check")
                if cache_value == "ok":
                    health_status.append("✅ Cache: OK")
                else:
                    health_status.append("❌ Cache: Valor não corresponde")
            except Exception as e:
                health_status.append(f"❌ Cache: ERRO - {str(e)}")

            # Verificar modelos
            try:
                user_count = request.user.__class__.objects.count()
                health_status.append(f"✅ Usuários: {user_count} registros")
            except Exception as e:
                health_status.append(f"❌ Usuários: ERRO - {str(e)}")

            operation_result = "Health Check Resultado:\n\n" + "\n".join(health_status)

        elif action == "db_check":
            # Verificação específica do banco
            from django.db import connection

            db_info = []
            try:
                with connection.cursor() as cursor:
                    # Verificar tabelas principais
                    tables = [
                        'usuarios_usuario',
                        'seguranca_logauditoria',
                        'seguranca_logerro',
                        'seguranca_blacklistip'
                    ]
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        db_info.append(f"✅ {table}: {count} registros")

                    # Verificar conexões ativas (PostgreSQL)
                    if connection.vendor == 'postgresql':
                        cursor.execute("SELECT COUNT(*) FROM pg_stat_activity")
                        active_conn = cursor.fetchone()[0]
                        db_info.append(f"ℹ️ Conexões ativas: {active_conn}")

            except Exception as e:
                db_info.append(f"❌ Erro na verificação: {str(e)}")

            operation_result = "Verificação do Banco de Dados:\n\n" + "\n".join(db_info)

        elif action == "cache_clear":
            # Limpar cache
            from django.core.cache import cache
            try:
                cache.clear()
                operation_result = "✅ Cache limpo com sucesso"
            except Exception as e:
                operation_result = f"❌ Erro ao limpar cache: {str(e)}"

        elif action == "toggle_maintenance":
            # Toggle modo manutenção (simulado)
            operation_result = "⚠️ Modo manutenção não implementado ainda.\n\nPara implementar:\n- Criar modelo MaintenanceMode\n- Adicionar middleware\n- Atualizar template base"

        elif action == "export_config":
            # Exportar configurações (simulado)
            import os
            from django.conf import settings

            config_info = []
            config_info.append(f"DEBUG: {getattr(settings, 'DEBUG', 'N/A')}")
            config_info.append(f"DATABASE: {settings.DATABASES['default']['ENGINE'].split('.')[-1] if 'default' in settings.DATABASES else 'N/A'}")
            config_info.append(f"CACHE: {settings.CACHES['default']['BACKEND'].split('.')[-1] if 'default' in settings.CACHES else 'N/A'}")
            config_info.append(f"TIME_ZONE: {getattr(settings, 'TIME_ZONE', 'N/A')}")

            operation_result = "Configurações do Sistema:\n\n" + "\n".join(config_info)

    return render(
        request,
        "ti/operacoes.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "pode_operacoes": True,
            "apenas_ti": usuario_e_apenas_ti(request.user),
            "operation_result": operation_result,
        },
    )
