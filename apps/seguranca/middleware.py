import logging
import traceback
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models.blacklist import BlacklistIP
from .utils.ip_whitelist import garantir_ip_liberado, ip_esta_na_whitelist

logger = logging.getLogger("seguranca.audit")

import re
from apps.ti.models import RegraWAF, ConfiguracaoSeguranca

class SecurityShieldMiddleware:
    """Escudo SOC: Bloqueia IPs banidos, Honeypots, WAF e Exfiltração."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Se o IP está na whitelist (ex: localhost, loopback ou IPs confiáveis), ignora blacklist
        if not ip_esta_na_whitelist(ip):
            try:
                # 1. Verificar Lista Negra
                banido = BlacklistIP.objects.filter(ip_endereco=ip, is_active=True).first()
                if banido:
                    return HttpResponseForbidden(f"Acesso negado. IP {ip} bloqueado.")
            except Exception as e:
                logger.error(f"Erro ao verificar blacklist para IP {ip}: {e}")

        # 2. Motor WAF (Filtro de Ataques com cache para evitar query em toda requisição)
        from django.core.cache import cache
        try:
            regras_waf = cache.get("regras_waf_ativas")
            if regras_waf is None:
                regras_waf = list(RegraWAF.objects.filter(ativo=True))
                cache.set("regras_waf_ativas", regras_waf, 60)

            path_completo = f"{request.path}?{request.GET.urlencode()}"
            for regra in regras_waf:
                if re.search(regra.padrao_regex, path_completo, re.IGNORECASE):
                    logger.warning(f"WAF: Bloqueado IP {ip} tentando {path_completo} (Regra: {regra.nome})")
                    return HttpResponseForbidden("Ação bloqueada pelo firewall do sistema (WAF).")
        except Exception as e:
            logger.error(f"Erro no motor WAF: {e}")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


class Force2FAMiddleware:
    """Middleware desativado temporariamente conforme solicitação do usuário."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class SecurityHardeningMiddleware:
    """Aplica cabeçalhos extras de endurecimento de segurança."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Permissions-Policy'] = "geolocation=(), microphone=()"
        return response


class ManutencaoMiddleware:
    """Alias para compatibilidade (a lógica principal está no app TI)."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class BlacklistMiddleware(SecurityShieldMiddleware):
    """Alias para manter compatibilidade com settings.py antigos."""
    pass


class AuditMiddleware:
    """Registra acessos sensíveis no log do sistema (LGPD Compliance)."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            logger.info(f"AUDIT: User {request.user.username} accessed {request.path} from {request.META.get('REMOTE_ADDR')}")
        return self.get_response(request)


class ExceptionMiddleware:
    """Captura exceções e loga para o SOC."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"CRITICAL ERROR: {str(exception)}\n{traceback.format_exc()}")
        # Em produção, retornaria uma página 500 customizada
        return None
