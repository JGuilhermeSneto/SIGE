import logging
from django.utils.deprecation import MiddlewareMixin
from apps.seguranca.models import LogAuditoria

logger = logging.getLogger('sige.audit')

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware para registrar acessos a views sensíveis para conformidade com a LGPD.
    Registra quem acessou o quê e quando, salvando no banco de dados.
    """
    
    SENSITIVE_PATHS = [
        '/saude/',
        '/financeiro/',
        '/infraestrutura/',
        '/admin/',
        '/seguranca/',
        '/usuarios/perfil/',
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            path = request.path
            
            # Verifica se o caminho atual é sensível
            if any(sensitive in path for sensitive in self.SENSITIVE_PATHS):
                user = request.user
                ip = self.get_client_ip(request)
                method = request.method
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Salva no banco de dados para visibilidade no Dashboard
                LogAuditoria.objects.create(
                    usuario=user,
                    path=path,
                    metodo=method,
                    ip_endereco=ip,
                    user_agent=user_agent,
                    descricao=f"Acesso à área sensível: {path}"
                )

                # Mantém o log em arquivo como backup
                logger.info(f"AUDIT: Usuário [{user.username}] acessou área sensível: {path} (IP: {ip})")
        
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ExceptionMiddleware(MiddlewareMixin):
    """Captura exceções não tratadas e salva no banco de dados para auditoria de erros."""
    
    def process_exception(self, request, exception):
        import traceback
        from apps.seguranca.models import LogErro
        
        user = request.user if request.user.is_authenticated else None
        ip = AuditMiddleware().get_client_ip(request)
        
        LogErro.objects.create(
            usuario=user,
            tipo_excecao=type(exception).__name__,
            mensagem=str(exception),
            traceback=traceback.format_exc(),
            path=request.path,
            metodo=request.method,
            ip_endereco=ip
        )
        return None
