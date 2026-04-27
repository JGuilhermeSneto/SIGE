import threading
from django.utils.deprecation import MiddlewareMixin
from ..models.tenant import Instituicao

_thread_locals = threading.local()

def get_current_tenant():
    """Retorna a instituição ativa na thread atual."""
    return getattr(_thread_locals, 'instituicao', None)

class TenantMiddleware(MiddlewareMixin):
    """
    Middleware responsável por identificar qual instituição está acessando o sistema.
    Por enquanto, ele busca a primeira instituição do banco ou cria uma 'Escola Padrão'.
    """
    def process_request(self, request):
        # 1. Tenta pegar a instituição pelo slug na URL ou pelo host (futuro)
        # Por enquanto, pegamos a primeira disponível para não quebrar o sistema.
        instituicao = Instituicao.objects.first()
        
        if not instituicao:
            # Seed automático se não houver nenhuma (facilita o dev)
            instituicao = Instituicao.objects.create(
                nome="SIGE - Escola Padrão",
                cnpj="00.000.000/0001-00",
                slug="escola-padrao"
            )
            
        request.instituicao = instituicao
        _thread_locals.instituicao = instituicao

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'instituicao'):
            del _thread_locals.instituicao
        return response
