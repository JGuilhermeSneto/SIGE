def get_client_ip(request):
    """
    Utilitário para extrair o IP do cliente de forma robusta, 
    lidando com proxies e balanceadores de carga.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
