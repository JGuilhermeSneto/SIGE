import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache
import hashlib
import traceback
from apps.seguranca.models import (
    LogAuditoria,
    BlacklistIP,
    ConfiguracaoSeguranca,
    LogErro,
)
from apps.comum.utils.network import get_client_ip
from .utils.hardening import sanitizar_pii, validar_assinatura_arquivo

logger = logging.getLogger("sige.security")


class SecurityHardeningMiddleware(MiddlewareMixin):
    """
    Camada extra de proteção para identificar comportamentos maliciosos:
    - Admin Honeypot: Bloqueia bots tentando acessar o admin sem login.
    - Rate Limiting: Identifica e pune IPs com volume anormal de erros.
    """

    def process_request(self, request):
        path = request.path
        ip = get_client_ip(request)
        
        # Ignora localhost (Desenvolvimento)
        if ip in ["127.0.0.1", "::1"]:
            return None

        # 1. HONEYPOT: Acesso ao admin sem estar logado
        if path.startswith("/admin/") and hasattr(request, "user") and not request.user.is_authenticated:
            # Incrementa contador de ameaça no cache
            key = f"threat_count_{ip}"
            count = cache.get(key, 0) + 1
            cache.set(key, count, 3600)  # Expira em 1h

            if count >= 3:
                # Banimento automático por 24h após 3 tentativas de invasão
                BlacklistIP.objects.get_or_create(
                    ip_endereco=ip,
                    defaults={
                        "motivo": "Honeypot: Tentativas persistentes de acesso ao admin sem login.",
                        "expira_em": timezone.now() + timezone.timedelta(days=1),
                    },
                )
                logger.warning(
                    f"SECURITY: IP {ip} banido automaticamente por tentativa de invasão no Admin."
                )

        return None


class ManutencaoMiddleware(MiddlewareMixin):
    """
    Verifica se o sistema está em modo manutenção.
    Redireciona usuários comuns para a página de manutenção.
    """

    def process_request(self, request):
        path = request.path
        if any(
            p in path
            for p in [
                "/static/",
                "/media/",
                "/admin/",
                "/seguranca/",
                "/ti/",
                "/login/",
                "/logout/",
            ]
        ):
            return None

        config = ConfiguracaoSeguranca.get_solo()
        if config.manutencao_ativa:
            from apps.ti.utils.permissoes import usuario_tem_operacoes_ti

            pode_acessar = False
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    pode_acessar = True
                elif (
                    config.permite_login_gestor
                    and hasattr(request.user, "perfil")
                    and request.user.perfil == "gestor"
                ):
                    pode_acessar = True
                elif usuario_tem_operacoes_ti(request.user):
                    pode_acessar = True

            if not pode_acessar:
                return render(
                    request,
                    "seguranca/manutencao.html",
                    {"mensagem": config.mensagem_manutencao, "config": config},
                    status=503,
                )

        return None


class AuditMiddleware(MiddlewareMixin):
    """Registra acessos a views sensíveis para conformidade com a LGPD."""

    SENSITIVE_PATHS = [
        "/saude/",
        "/financeiro/",
        "/infraestrutura/",
        "/admin/",
        "/seguranca/",
        "/ti/",
        "/usuarios/perfil/",
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            path = request.path
            if any(sensitive in path for sensitive in self.SENSITIVE_PATHS):
                ip = get_client_ip(request)
                LogAuditoria.objects.create(
                    usuario=request.user,
                    path=path,
                    metodo=request.method,
                    ip_endereco=ip,
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    descricao=f"Acesso à área sensível: {path}",
                )
        return None


class ExceptionMiddleware(MiddlewareMixin):
    """Captura exceções, sanitiza PII e gerencia auto-blacklist por erros repetitivos."""

    def process_exception(self, request, exception):
        import traceback

        ip = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        # Ignora localhost (Desenvolvimento)
        if ip in ["127.0.0.1", "::1"]:
            return None

        # Monitora volume de erros para Auto-Blacklist (Rate Limiting de erros)
        key = f"error_count_{ip}"
        count = cache.get(key, 0) + 1
        cache.set(key, count, 60)  # Janela de 1 minuto

        if count >= 10:
            # Se gerar 10 erros em 1 minuto, banimento preventivo de 1h
            BlacklistIP.objects.get_or_create(
                ip_endereco=ip,
                defaults={
                    "motivo": "Auto-Blacklist: Volume anormal de erros gerados (Possível ataque).",
                    "expira_em": timezone.now() + timezone.timedelta(hours=1),
                },
            )

        # Sanitiza a mensagem do erro (Remove CPFs, Emails, etc) antes de salvar
        mensagem_limpa = sanitizar_pii(str(exception))
        traceback_limpo = sanitizar_pii(traceback.format_exc())
        tipo_excecao = type(exception).__name__

        # Lógica de Deduplicação
        hash_input = f"{tipo_excecao}|{mensagem_limpa}|{request.path}"
        hash_erro = hashlib.sha256(hash_input.encode()).hexdigest()

        erro_existente = LogErro.objects.filter(hash_erro=hash_erro, resolvido=False).first()

        if erro_existente:
            erro_existente.contador += 1
            erro_existente.usuario = user # Atualiza com o último usuário que gerou o erro
            erro_existente.ip_endereco = ip
            erro_existente.save()
        else:
            LogErro.objects.create(
                usuario=user,
                tipo_excecao=tipo_excecao,
                mensagem=mensagem_limpa,
                traceback=traceback_limpo,
                path=request.path,
                metodo=request.method,
                ip_endereco=ip,
                hash_erro=hash_erro,
                contador=1
            )
        return None


class BlacklistMiddleware(MiddlewareMixin):
    """Bloqueia o acesso de IPs que estão na BlacklistIP."""

    def process_request(self, request):
        ip = get_client_ip(request)

        # Ignora localhost (Desenvolvimento)
        if ip in ["127.0.0.1", "::1"]:
            return None
        bloqueio = BlacklistIP.objects.filter(ip_endereco=ip).first()

        if bloqueio:
            if not bloqueio.expira_em or bloqueio.expira_em > timezone.now():
                return HttpResponseForbidden(
                    f"Acesso negado para o IP {ip}. Motivo: {bloqueio.motivo}."
                )
        return None


class Force2FAMiddleware(MiddlewareMixin):
    """
    Força o uso de 2FA para usuários da área de TI.
    Se o usuário tem permissão de TI e não está verificado via OTP, redireciona para setup.
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            return None

        # Verifica se o 2FA obrigatório está ativo via Feature Flag
        from apps.ti.models import FeatureFlag
        flag_2fa = FeatureFlag.objects.filter(nome="FORCE_2FA", ativo=True).exists()
        if not flag_2fa:
            return None

        # Ignora caminhos de setup de 2FA para evitar loop
        path = request.path
        if any(p in path for p in ["/account/two_factor/", "/account/otp/"]):
            return None

        from apps.ti.utils.permissoes import usuario_tem_painel_ti
        
        # Se for usuário de TI e NÃO estiver verificado (is_verified vem do django-otp)
        if usuario_tem_painel_ti(request.user):
            # Verifica se o método is_verified existe (injetado pelo OTPMiddleware)
            is_verified = False
            if hasattr(request.user, 'is_verified'):
                is_verified = request.user.is_verified()
            
            if not is_verified:
                # Redireciona para a configuração de 2FA
                return redirect("two_factor:setup")
        
        return None
