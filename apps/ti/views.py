import platform
import sys
from datetime import timedelta

import django
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
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

    # Informações do Sistema
    sistema_info = {
        "python": sys.version.split(" ")[0],
        "django": django.get_version(),
        "os": platform.system(),
        "db_vendor": connection.vendor,
        "env": "Produção" if not django.conf.settings.DEBUG else "Desenvolvimento",
    }

    ti_status_cards = [
        {
            "titulo": "Bugs novos",
            "valor": BugReport.objects.filter(status="NOVO").count(),
            "descricao": "Relatórios novos aguardando triagem.",
            "cor": "var(--accent-amber)",
        },
        {
            "titulo": "Erros (7d)",
            "valor": LogErro.objects.filter(data_ocorrencia__gte=ultimos_sete_dias).count(),
            "descricao": "Exceções registradas recentemente.",
            "cor": "var(--accent-ruby)",
        },
        {
            "titulo": "IPs Ativos",
            "valor": BlacklistIP.objects.filter(
                Q(expira_em__isnull=True) | Q(expira_em__gte=agora)
            ).count(),
            "descricao": "Endereços na blacklist de segurança.",
            "cor": "var(--accent-violet)",
        },
        {
            "titulo": "Auditoria",
            "valor": LogAuditoria.objects.filter(data_evento__gte=ultimos_sete_dias).count(),
            "descricao": "Logs de ações sensíveis na semana.",
            "cor": "var(--accent-cyan)",
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
            "sistema_info": sistema_info,
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
@user_passes_test(usuario_tem_painel_ti)
def documentacao_api(request):
    """Landing page para a documentação do Swagger/API."""
    return render(
        request,
        "ti/api_docs.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "pode_operacoes": usuario_tem_operacoes_ti(request.user),
        },
    )


@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def operacoes_ti(request):
    """Rotinas avançadas."""
    operation_result = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "cleanup_logs_30":
            cutoff_date = timezone.now() - timedelta(days=30)
            deleted_logs = LogAuditoria.objects.filter(data_evento__lt=cutoff_date).delete()[0]
            deleted_errors = LogErro.objects.filter(data_ocorrencia__lt=cutoff_date).delete()[0]
            operation_result = f"Logs limpos:\n- Auditoria: {deleted_logs}\n- Erros: {deleted_errors}\nCorte: {cutoff_date.date()}"

        elif action == "cleanup_logs_90":
            cutoff_date = timezone.now() - timedelta(days=90)
            deleted_logs = LogAuditoria.objects.filter(data_evento__lt=cutoff_date).delete()[0]
            deleted_errors = LogErro.objects.filter(data_ocorrencia__lt=cutoff_date).delete()[0]
            operation_result = f"Logs limpos:\n- Auditoria: {deleted_logs}\n- Erros: {deleted_errors}\nCorte: {cutoff_date.date()}"

        elif action == "cleanup_sessions":
            from django.contrib.sessions.models import Session
            expired_sessions = Session.objects.filter(expire_date__lt=timezone.now()).delete()[0]
            operation_result = f"Sessões expiradas removidas: {expired_sessions}"

        elif action == "health_check":
            from django.db import connection
            from django.core.cache import cache
            health_status = []
            try:
                with connection.cursor() as cursor: cursor.execute("SELECT 1")
                health_status.append("✅ Banco de dados: OK")
            except Exception as e: health_status.append(f"❌ Banco de dados: {str(e)}")
            try:
                cache.set("health_check", "ok", 10)
                if cache.get("health_check") == "ok": health_status.append("✅ Cache: OK")
                else: health_status.append("❌ Cache: Falha na recuperação")
            except Exception as e: health_status.append(f"❌ Cache: {str(e)}")
            operation_result = "Health Check:\n\n" + "\n".join(health_status)

        elif action == "db_check":
            from django.db import connection
            db_info = []
            try:
                with connection.cursor() as cursor:
                    tables = ['usuarios_usuario', 'seguranca_logauditoria', 'seguranca_logerro']
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        db_info.append(f"✅ {table}: {cursor.fetchone()[0]} reg.")
            except Exception as e: db_info.append(f"❌ Erro: {str(e)}")
            operation_result = "DB Check:\n\n" + "\n".join(db_info)

        elif action == "cache_clear":
            from django.core.cache import cache
            cache.clear()
            operation_result = "✅ Cache limpo com sucesso"

        elif action == "toggle_maintenance":
            from apps.seguranca.models import ConfiguracaoSeguranca
            config = ConfiguracaoSeguranca.get_solo()
            config.manutencao_ativa = not config.manutencao_ativa
            config.save()
            operation_result = f"✅ Modo Manutenção: {'ATIVADO' if config.manutencao_ativa else 'DESATIVADO'}"

        elif action == "export_config":
            from django.conf import settings
            config_info = [f"DEBUG: {settings.DEBUG}", f"DB: {settings.DATABASES['default']['ENGINE']}", f"TZ: {settings.TIME_ZONE}"]
            operation_result = "Configurações:\n\n" + "\n".join(config_info)

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


@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_bugs(request):
    """Lista e gerencia os reports de bugs."""
    status_filtro = request.GET.get("status")
    bugs = BugReport.objects.select_related("usuario").all().order_by('-data_criacao')
    if status_filtro: bugs = bugs.filter(status=status_filtro)
    stats = {
        "total": BugReport.objects.count(),
        "novos": BugReport.objects.filter(status="NOVO").count(),
        "analise": BugReport.objects.filter(status="ANALISE").count(),
        "corrigidos": BugReport.objects.filter(status="CORRIGIDO").count(),
    }
    return render(
        request,
        "ti/gestao_bugs.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "bugs": bugs,
            "stats": stats,
            "status_atual": status_filtro,
            "pode_operacoes": usuario_tem_operacoes_ti(request.user),
        },
    )


@login_required
@user_passes_test(usuario_tem_painel_ti)
def atualizar_status_bug(request, bug_id):
    """Atualiza o status de um bug."""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    bug = get_object_or_404(BugReport, id=bug_id)
    novo_status = request.POST.get("status")
    if novo_status in dict(BugReport.STATUS_CHOICES):
        bug.status = novo_status
        bug.save()
        messages.success(request, f"Status do bug #{bug.id} atualizado.")
    return redirect("ti:gestao_bugs")
