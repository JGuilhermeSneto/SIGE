import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('sige.audit')

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware para registrar acessos a views sensíveis para conformidade com a LGPD.
    Registra quem acessou o quê e quando.
    """
    
    # Lista de nomes de URL ou caminhos que devem ser auditados
    SENSITIVE_PATHS = [
        '/saude/',
        '/financeiro/',
        '/documentos/boletim/',
        '/documentos/declaracao/',
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            path = request.path
            # Verifica se o caminho atual é sensível
            if any(sensitive in path for sensitive in self.SENSITIVE_PATHS):
                user = request.user.username
                ip = self.get_client_ip(request)
                logger.info(f"AUDIT: Usuário [{user}] acessou área sensível: {path} (IP: {ip})")
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
