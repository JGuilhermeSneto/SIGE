from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from ..models.blacklist import BlacklistIP
from ..utils.ip_whitelist import ip_esta_na_whitelist


def honeypot_trap(request):
    """
    View de Armadilha (Honeypot):
    Captura o IP do atacante e o bane imediatamente por 48 horas.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    if not ip_esta_na_whitelist(ip):
        BlacklistIP.objects.update_or_create(
            ip_endereco=ip,
            defaults={
                "motivo": f"Tentativa de acesso a URL restrita (Honeypot) em {request.path}",
                "expira_em": timezone.now() + timedelta(hours=48),
            },
        )

    return HttpResponseForbidden("<h1>Acesso Negado</h1><p>Seu endereço IP foi permanentemente registrado e bloqueado por tentativas de acesso não autorizadas.</p>")
