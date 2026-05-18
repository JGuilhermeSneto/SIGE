from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sessions.models import Session
from django.utils import timezone
from apps.seguranca.models import BlacklistIP, BugReport, LogErro, ConfiguracaoSeguranca
from apps.comum.utils.network import get_client_ip
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.urls import reverse
from axes.models import AccessAttempt
from ..utils.hardening import validar_assinatura_arquivo
from apps.academico.services.notificacao_servico import NotificacaoServico
from apps.seguranca.utils.access import (
    pode_executar_acoes_seguranca,
    pode_ver_dashboard_seguranca,
)
from apps.seguranca.utils.ip_whitelist import garantir_ip_liberado, ip_esta_na_whitelist
import logging

logger = logging.getLogger("sige.audit")

User = get_user_model()


def is_security_admin(user):
    """Compat: ações sensíveis do Shield (gestor, super ou TI coordenação)."""
    return pode_executar_acoes_seguranca(user)


@user_passes_test(is_security_admin)
def bloquear_ip(request, ip):
    if ip_esta_na_whitelist(ip):
        garantir_ip_liberado(ip)
        messages.warning(
            request,
            f"O IP {ip} está na lista de IPs protegidos e não pode ser bloqueado.",
        )
        return redirect("ti:seguranca")

    motivo = request.POST.get("motivo", "Bloqueio manual via Shield Dashboard")
    BlacklistIP.objects.get_or_create(
        ip_endereco=ip, defaults={"motivo": motivo, "bloqueado_por": request.user}
    )

    AccessAttempt.objects.filter(ip_address=ip).delete()

    messages.success(request, f"O IP {ip} foi adicionado à Blacklist com sucesso.")
    return redirect("ti:seguranca")


@user_passes_test(is_security_admin)
def desbloquear_ip(request, ip_id):
    bloqueio = get_object_or_404(BlacklistIP, id=ip_id)
    bloqueio.delete()
    messages.success(request, f"O IP {bloqueio.ip_endereco} foi removido da Blacklist.")
    return redirect("ti:seguranca")


@user_passes_test(is_security_admin)
def bloquear_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()

    # Encerra todas as sessões do usuário
    [
        s.delete()
        for s in Session.objects.all()
        if s.get_decoded().get("_auth_user_id") == str(user.id)
    ]

    messages.warning(
        request,
        f"O usuário {user.username} foi bloqueado e todas as suas sessões foram encerradas.",
    )
    return redirect("ti:seguranca")


@user_passes_test(pode_ver_dashboard_seguranca)
def detalhe_bug(request, bug_id):
    """Página de detalhamento técnico para a equipe de TI."""
    bug = get_object_or_404(BugReport, id=bug_id)
    return render(
        request,
        "seguranca/bug_detalhe.html",
        {
            "bug": bug,
            "pode_executar_acoes_seguranca": pode_executar_acoes_seguranca(request.user),
        },
    )


@user_passes_test(is_security_admin)
def encaminhar_ti(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)
    bug.encaminhado_ti = True
    bug.data_encaminhamento = timezone.now()
    bug.save()

    # Notifica o usuário que reportou (se identificado)
    if bug.usuario:
        NotificacaoServico.notificar_usuario(
            user=bug.usuario,
            tipo="SISTEMA",
            titulo="Seu chamado foi recebido pela TI",
            mensagem=f"O bug '{bug.titulo}' foi recebido e está em análise técnica.",
        )

    messages.success(request, f"Bug #{bug.id} encaminhado para a equipe de TI.")
    return redirect("seguranca:detalhe_bug", bug_id=bug.id)


@user_passes_test(is_security_admin)
def resolver_bug(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)
    bug.resolvido = True
    bug.data_resolucao = timezone.now()
    bug.save()

    # Notifica o usuário que reportou
    if bug.usuario:
        NotificacaoServico.notificar_usuario(
            user=bug.usuario,
            tipo="SISTEMA",
            titulo="Bug Resolvido!",
            mensagem=f"Temos boas notícias! O bug '{bug.titulo}' que você reportou foi corrigido.",
        )

    messages.success(request, f"Bug #{bug.id} marcado como resolvido.")
    return redirect("seguranca:detalhe_bug", bug_id=bug.id)


@user_passes_test(is_security_admin)
def toggle_manutencao(request):
    """Ativa ou desativa o modo manutenção do sistema."""
    if request.method == "POST":
        config = ConfiguracaoSeguranca.get_solo()
        config.manutencao_ativa = not config.manutencao_ativa
        config.save()

        status = "ATIVADO" if config.manutencao_ativa else "DESATIVADO"

        # Notifica todos os usuários Staff (Gestores e Professores)
        NotificacaoServico.notificar_grupo(
            usuarios_queryset=User.objects.filter(is_staff=True),
            tipo="SISTEMA",
            titulo=f"Modo Manutenção {status}",
            mensagem=(
                f"O sistema entrou em modo de manutenção e o acesso externo está restrito."
                if config.manutencao_ativa
                else "O sistema está operando normalmente agora."
            ),
            url_destino=reverse("ti:seguranca"),
        )

        messages.warning(request, f"O Modo Manutenção foi {status} com sucesso.")

    return redirect("ti:seguranca")


@user_passes_test(is_security_admin)
def limpar_logs_erro(request):
    LogErro.objects.all().delete()
    messages.info(request, "Todos os logs de erro foram limpos.")
    return redirect("ti:seguranca")


def honeypot_view(request):
    """
    View que captura acessos a caminhos maliciosos comuns e bloqueia o IP instantaneamente.
    """
    ip = get_client_ip(request)
    path = request.path

    if not ip_esta_na_whitelist(ip):
        BlacklistIP.objects.get_or_create(
            ip_endereco=ip,
            defaults={
                "motivo": f"Honeypot Triggered: Acesso ao caminho proibido [{path}]",
                "bloqueado_por": None,
            },
        )
        logger.warning(
            f"HONEYPOT: IP {ip} bloqueado automaticamente ao tentar acessar {path}"
        )
    return HttpResponseForbidden(
        "Acesso Proibido. Seu IP foi permanentemente bloqueado por atividade suspeita."
    )


def reportar_bug(request):
    """
    Recebe o relatório de bug enviado pelo usuário via modal.
    """
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        prioridade = request.POST.get("prioridade", "MEDIA")
        url_origem = request.POST.get("url_origem")

        user = request.user if request.user.is_authenticated else None
        ip = get_client_ip(request)
        browser_info = request.META.get("HTTP_USER_AGENT", "Desconhecido")

        screenshot = request.FILES.get("screenshot")

        # Validação de segurança do arquivo (Magic Numbers)
        if screenshot and not validar_assinatura_arquivo(screenshot):
            messages.error(
                request, "O arquivo de evidência parece ser inválido ou malicioso."
            )
            return redirect(url_origem or reverse("ti:painel"))

        bug = BugReport.objects.create(
            usuario=user,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            url_origem=url_origem,
            ip_endereco=ip,
            browser_info=browser_info,
            screenshot=screenshot,
        )

        # Notifica Gestores sobre o novo bug
        NotificacaoServico.notificar_gestores(
            tipo="SISTEMA",
            titulo=f"Novo Bug Reportado: {titulo}",
            mensagem=f"O usuário {user.username if user else 'Anônimo'} reportou um bug com prioridade {prioridade}.",
            url_destino=reverse("seguranca:detalhe_bug", kwargs={"bug_id": bug.id}),
        )

        messages.success(
            request,
            "Obrigado! Seu relatório de bug foi enviado para nossa equipe de segurança.",
        )
        return redirect(url_origem or reverse("ti:painel"))

    return redirect(reverse("ti:painel"))
