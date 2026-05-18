import ipaddress

from django.conf import settings


def _ips_configurados():
    return getattr(settings, "SEGURANCA_IP_WHITELIST", [])


def normalizar_ip(ip):
    if not ip:
        return None
    return str(ip).strip()


def ip_esta_na_whitelist(ip):
    """IPs que nunca podem ser bloqueados (blacklist, honeypot ou axes)."""
    ip = normalizar_ip(ip)
    if not ip:
        return False

    if ip in _ips_configurados() or ip in ("localhost",):
        return True

    try:
        addr = ipaddress.ip_address(ip)
        if settings.DEBUG and addr.is_loopback:
            return True
    except ValueError:
        pass

    return False


def garantir_ip_liberado(ip):
    """Remove qualquer bloqueio existente para IPs liberados."""
    ip = normalizar_ip(ip)
    if not ip or not ip_esta_na_whitelist(ip):
        return

    from apps.seguranca.models import BlacklistIP

    BlacklistIP.objects.filter(ip_endereco=ip).delete()

    try:
        from axes.models import AccessAttempt

        AccessAttempt.objects.filter(ip_address=ip).delete()
    except Exception:
        pass
