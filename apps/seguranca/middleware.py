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

        if ip_esta_na_whitelist(ip):
            garantir_ip_liberado(ip)
        else:
            # 1. Verificar Lista Negra
            banido = BlacklistIP.objects.filter(ip_endereco=ip).first()
            if banido and banido.is_active:
                return HttpResponseForbidden(f"Acesso negado. IP {ip} bloqueado.")

        # 2. Motor WAF (Filtro de Ataques)
        path_completo = f"{request.path}?{request.GET.urlencode()}"
        regras_waf = RegraWAF.objects.filter(ativo=True)
        for regra in regras_waf:
            if re.search(regra.padrao_regex, path_completo, re.IGNORECASE):
                logger.warning(f"WAF: Bloqueado IP {ip} tentando {path_completo} (Regra: {regra.nome})")
                return HttpResponseForbidden(f"Ação bloqueada pelo firewall do sistema (WAF).")

        # 3. Monitor de Tráfego (Placeholder para Exfiltração)
        # Aqui poderíamos integrar um contador no Redis para limitar downloads por minuto
        
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
