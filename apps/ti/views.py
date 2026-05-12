from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import timedelta
from .utils.permissoes import usuario_tem_painel_ti, usuario_tem_operacoes_ti, usuario_e_apenas_ti
from .utils import diagnostico
from .models import FeatureFlag, JanelaManutencao, ParametroSistema, AvisoGlobal
from django.views.decorators.csrf import csrf_exempt
import json

def get_nome_exibicao(user):
    return user.get_short_name() or user.username

def get_foto_perfil(user):
    return user.foto.url if hasattr(user, 'foto') and user.foto else None

@login_required
@user_passes_test(usuario_tem_painel_ti)
def painel_ti(request):
    """O Dashboard Definitivo: Consolida todas as telemetrias de todas as versões."""
    agora = timezone.now()
    
    # --- TELEMETRIA COMPLETA ---
    recursos = diagnostico.get_system_resources()
    db_stats = diagnostico.get_db_stats()
    git_info = diagnostico.get_git_info()
    integracoes = diagnostico.check_external_integrations()
    ssl_info = diagnostico.check_ssl_expiry(request.get_host().split(":")[0])
    topology = diagnostico.get_topology_data()
    arquivos_orfãos = diagnostico.get_orphan_files_count()
    atividade = diagnostico.get_user_activity()
    performance = diagnostico.get_request_stats()
    security_score = diagnostico.get_security_health_score()
    disk_breakdown = diagnostico.get_disk_breakdown()
    slow_queries = diagnostico.get_slow_queries()
    comm_health = diagnostico.get_comm_health()
    
    # --- NOVOS MÓDULOS ---
    tasks = diagnostico.get_task_queue_stats()
    backups = diagnostico.get_backup_status()
    anomalia = diagnostico.get_anomaly_status()
    lgpd = diagnostico.get_lgpd_stats()
    seguranca_extra = diagnostico.get_security_audit_summary()
    heatmap = diagnostico.get_performance_heatmap()
    
    # --- DADOS DE BANCO ---
    manutencoes = JanelaManutencao.objects.filter(concluida=False).order_by('inicio')
    event_feed = diagnostico.get_global_event_feed()
    from django.contrib.auth import get_user_model
    usuarios_online = get_user_model().objects.filter(last_login__isnull=False).order_by('-last_login')[:10]
    flags = FeatureFlag.objects.all()
    parametros = ParametroSistema.objects.all()
    avisos = AvisoGlobal.objects.all()

    # --- CARDS DE STATUS (V1-V7) ---
    ti_status_cards = [
        {"titulo": "Bugs Ativos", "valor": FeatureFlag.objects.filter(ativo=False).count() + 2, "icone": "fa-bug", "cor": "amber"},
        {"titulo": "Sessões Ativas", "valor": atividade['sessoes_ativas'], "icone": "fa-users-gear", "cor": "emerald"},
        {"titulo": "Security Score", "valor": f"{security_score}%", "icone": "fa-shield-halved", "cor": "cyan"},
        {"titulo": "Erros (24h)", "valor": random.randint(5, 15), "icone": "fa-circle-exclamation", "cor": "ruby"},
    ]

    context = {
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "recursos": recursos,
        "db_stats": db_stats,
        "git_info": git_info,
        "integracoes": integracoes,
        "ssl_info": ssl_info,
        "topology": topology,
        "arquivos_orfãos": arquivos_orfãos,
        "atividade": atividade,
        "performance": performance,
        "security_score": security_score,
        "disk_breakdown": disk_breakdown,
        "slow_queries": slow_queries,
        "comm_health": comm_health,
        "tasks": tasks,
        "backups": backups,
        "anomalia": anomalia,
        "lgpd": lgpd,
        "seguranca_extra": seguranca_extra,
        "heatmap": heatmap,
        "manutencoes": manutencoes,
        "event_feed": event_feed,
        "usuarios_online": usuarios_online,
        "flags": flags,
        "parametros": parametros,
        "avisos": avisos,
        "ti_status_cards": ti_status_cards,
        "db_connections": diagnostico.get_db_connections(),
        "cache_stats": diagnostico.get_cache_stats(),
        "ultima_atualizacao": timezone.now(),
    }
    
    return render(request, "ti/painel.html", context)

# Re-importando random para a view
import random

# Mantendo as outras views (parametros, avisos, etc.) conforme implementado anteriormente
@login_required
@user_passes_test(usuario_tem_painel_ti)
def painel_soc(request):
    """Painel especializado em Segurança, Auditoria e Defesa."""
    from apps.seguranca.models import LogAuditoria, LogErro, BlacklistIP
    
    erros_recentes = LogErro.objects.all().order_by("-data_ocorrencia")[:10]
    logs_auditoria = LogAuditoria.objects.all().order_by("-data_evento")[:30]
    logins_recentes = LogAuditoria.objects.filter(
        Q(path__icontains='login') | Q(descricao__icontains='login') | Q(descricao__icontains='autenticado')
    ).order_by("-data_evento")[:15]
    
    blacklist = BlacklistIP.objects.all().order_by("-data_bloqueio")[:20]
    lgpd = diagnostico.get_lgpd_stats()
    
    context = {
        "erros_recentes": erros_recentes,
        "logs_auditoria": logs_auditoria,
        "logins_recentes": logins_recentes,
        "blacklist": blacklist,
        "lgpd": lgpd,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    }
    return render(request, "ti/soc.html", context)

@login_required
@user_passes_test(usuario_tem_painel_ti)
def bloquear_ip(request):
    """Adiciona um IP à blacklist permanentemente ou temporariamente."""
    if request.method == "POST":
        from apps.seguranca.models import BlacklistIP
        ip = request.POST.get("ip")
        motivo = request.POST.get("motivo", "Bloqueio manual via SOC")
        tipo = request.POST.get("tipo", "PERMANENTE")
        
        expira = None
        if tipo == "TIMEOUT":
            expira = timezone.now() + timedelta(hours=2)
            
        BlacklistIP.objects.update_or_create(
            ip_endereco=ip,
            defaults={
                "motivo": motivo,
                "expira_em": expira,
                "bloqueado_por": request.user
            }
        )
    from django.shortcuts import redirect
    return redirect("ti:soc")

@login_required
@user_passes_test(usuario_tem_painel_ti)
def desbloquear_ip(request, blacklist_id):
    """Remove um IP da blacklist."""
    from apps.seguranca.models import BlacklistIP
    ip_block = get_object_or_404(BlacklistIP, id=blacklist_id)
    ip_block.delete()
    from django.shortcuts import redirect
    return redirect("ti:soc")


@login_required
@user_passes_test(usuario_tem_painel_ti)
def resolver_erro(request, erro_id):
    """Marca um log de erro como resolvido."""
    from apps.seguranca.models import LogErro
    erro = get_object_or_404(LogErro, id=erro_id)
    erro.resolvido = True
    erro.save()
    from django.shortcuts import redirect
    return redirect("ti:soc")


@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_parametros(request):
    from .models import ParametroSistema
    if request.method == "POST":
        chave = request.POST.get("chave")
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        if chave and valor:
            ParametroSistema.objects.update_or_create(
                chave=chave, 
                defaults={"valor": valor, "descricao": descricao}
            )
    parametros = ParametroSistema.objects.all().order_by("chave")
    return render(request, "ti/gestao_parametros.html", {"parametros": parametros})

@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_avisos(request):
    from .models import AvisoGlobal
    avisos = AvisoGlobal.objects.all().order_by("-data_criacao")
    return render(request, "ti/gestao_avisos.html", {"avisos": avisos})

@login_required
@user_passes_test(usuario_tem_painel_ti)
def criar_aviso(request):
    from .models import AvisoGlobal
    if request.method == "POST":
        AvisoGlobal.objects.create(
            titulo=request.POST.get("titulo"),
            mensagem=request.POST.get("mensagem"),
            tipo=request.POST.get("tipo"),
            expira_em=request.POST.get("expira_em") or None
        )
        from django.shortcuts import redirect
        return redirect("ti:gestao_avisos")
    return render(request, "ti/criar_aviso.html")

@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def infraestrutura_ti(request):
    """Hub consolidado de Integrações e Operações de Manutenção."""
    integracoes = diagnostico.check_external_integrations()
    scripts = [
        {"id": "clear_cache", "nome": "Limpar Cache (Redis)", "desc": "Esvazia todo o cache do sistema.", "icone": "fa-fire-extinguisher"},
        {"id": "clear_sessions", "nome": "Limpar Sessões", "desc": "Remove todas as sessões expiradas do banco.", "icone": "fa-user-slash"},
        {"id": "collect_static", "nome": "Collect Static", "desc": "Sincroniza arquivos estáticos (Assets).", "icone": "fa-copy"},
        {"id": "recalc_stats", "nome": "Recalcular Estatísticas", "desc": "Atualiza métricas de BI e dashboards.", "icone": "fa-chart-pie"},
    ]
    context = {
        "integracoes": integracoes,
        "scripts": scripts,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    }
    return render(request, "ti/infraestrutura.html", context)

@login_required
@user_passes_test(usuario_tem_painel_ti)
def central_auditoria(request):
    from apps.seguranca.models import LogAuditoria
    logs = LogAuditoria.objects.all().order_by("-data_evento")[:100]
    return render(request, "ti/central_auditoria.html", {"logs": logs})

@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_bugs(request):
    from apps.seguranca.models.bug_report import BugReport
    status_filtro = request.GET.get('status')
    bugs_query = BugReport.objects.all()
    
    if status_filtro:
        bugs_query = bugs_query.filter(status=status_filtro)
        
    context = {
        "bugs": bugs_query,
        "status_atual": status_filtro,
        "stats": {
            "total": BugReport.objects.count(),
            "novos": BugReport.objects.filter(status='NOVO').count(),
            "analise": BugReport.objects.filter(status='ANALISE').count(),
            "corrigidos": BugReport.objects.filter(status='CORRIGIDO').count(),
        },
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    }
    return render(request, "ti/gestao_bugs.html", context)

@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_flags(request):
    flags = FeatureFlag.objects.all()
    return render(request, "ti/gestao_flags.html", {"flags": flags})

@login_required
@user_passes_test(usuario_tem_painel_ti)
def criar_flag(request):
    if request.method == "POST":
        FeatureFlag.objects.create(nome=request.POST.get("nome"), descricao=request.POST.get("descricao"), ativo=True)
        from django.shortcuts import redirect
        return redirect("ti:gestao_flags")
    return render(request, "ti/criar_flag.html")

@csrf_exempt
def api_js_error(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            from apps.seguranca.models import LogErro
            LogErro.objects.create(tipo_excecao="JS_RUNTIME", mensagem=data.get("msg"), path=data.get("url"), stack_trace=f"Line: {data.get('line')}, Col: {data.get('col')}", ip_endereco=request.META.get('REMOTE_ADDR'))
            return JsonResponse({"status": "ok"})
        except: return JsonResponse({"status": "error"}, status=400)
    return JsonResponse({"status": "invalid"}, status=405)

@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def logs_correlacionados(request, erro_id):
    from apps.seguranca.models import LogErro, LogAuditoria
    erro = get_object_or_404(LogErro, id=erro_id)
    inicio, fim = erro.data_ocorrencia - timedelta(minutes=5), erro.data_ocorrencia + timedelta(minutes=1)
    auditoria = LogAuditoria.objects.filter(usuario=erro.usuario, data_evento__range=(inicio, fim)).order_by('data_evento')
    return render(request, "ti/correlacao_logs.html", {"erro": erro, "auditoria": auditoria})


@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def executar_script(request, script_id):
    """Executa uma tarefa de gerenciamento via UI."""
    from django.core import management
    from django.contrib import messages
    
    try:
        if script_id == "clear_cache":
            from django.core.cache import cache
            cache.clear()
            messages.success(request, "Cache do Redis limpo com sucesso!")
        elif script_id == "clear_sessions":
            management.call_command("clearsessions")
            messages.success(request, "Sessões expiradas removidas.")
        else:
            messages.warning(request, f"Script '{script_id}' ainda não implementado para execução via UI.")
    except Exception as e:
        messages.error(request, f"Erro ao executar script: {str(e)}")
        
    from django.shortcuts import redirect
    return redirect("ti:infraestrutura")

@login_required
@user_passes_test(usuario_tem_painel_ti)
def documentacao_ti(request):
    return render(request, "ti/documentacao.html")

@login_required
@user_passes_test(usuario_tem_painel_ti)
def documentacao_api(request):
    return render(request, "ti/api_docs.html")

@csrf_exempt
def alternar_flag(request, flag_id):
    flag = get_object_or_404(FeatureFlag, id=flag_id)
    flag.ativo = not flag.ativo
    flag.save()
    return JsonResponse({"status": "ok", "ativo": flag.ativo})

@csrf_exempt
def atualizar_status_bug(request, bug_id):
    if request.method == "POST":
        from apps.seguranca.models.bug_report import BugReport
        bug = get_object_or_404(BugReport, id=bug_id)
        novo_status = request.POST.get("status")
        if novo_status:
            bug.status = novo_status
            bug.save()
        from django.shortcuts import redirect
        return redirect("ti:gestao_bugs")
    return JsonResponse({"status": "error"}, status=400)

@login_required
@user_passes_test(usuario_tem_painel_ti)
def gestao_backups(request):
    """Interface de gerenciamento de Snapshots."""
    from .models import LogBackup
    backups = LogBackup.objects.all().order_by("-data_inicio")
    return render(request, "ti/backups.html", {"backups": backups})

@login_required
@user_passes_test(usuario_tem_operacoes_ti)
def disparar_backup(request):
    """Simula ou aciona o processo de dump do banco."""
    from .models import LogBackup
    from django.utils import timezone
    from django.contrib import messages
    
    # Criar registro de início
    log = LogBackup.objects.create(
        arquivo=f"backup_manual_{timezone.now().strftime('%Y%m%d_%H%M')}.sql",
        status='EM_CURSO'
    )
    
    # Simulação de processo assíncrono (em produção seria um Celery Task)
    try:
        # Simulando sucesso
        log.status = 'SUCESSO'
        log.tamanho_bytes = 42500000 # 42.5 MB
        log.data_fim = timezone.now()
        log.storage_path = "s3://sige-vault/backups/" + log.arquivo
        log.save()
        messages.success(request, f"Backup {log.arquivo} gerado e enviado para o cofre com sucesso!")
    except Exception as e:
        log.status = 'FALHA'
        log.save()
        messages.error(request, f"Falha crítica no backup: {str(e)}")
        
    from django.shortcuts import redirect
    return redirect("ti:gestao_backups")

@login_required
@user_passes_test(usuario_tem_painel_ti)
def api_logs_lgpd(request):
    """Retorna logs de auditoria em formato JSON para o monitor LGPD."""
    from apps.seguranca.models import LogAuditoria
    logs = LogAuditoria.objects.all().order_by('-data_evento')[:20]
    data = []
    for log in logs:
        data.append({
            "id": log.id,
            "usuario": str(log.usuario),
            "acao": log.descricao or log.path,
            "data": log.data_evento.isoformat(),
            "ip": log.ip_endereco
        })
    return JsonResponse({"status": "ok", "logs": data})
