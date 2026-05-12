from django.utils import timezone
from django.shortcuts import render
from .models import JanelaManutencao


class ManutencaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir acesso a arquivos estáticos e mídia sempre
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Checar se há manutenção ativa
        agora = timezone.now()
        manutencao = JanelaManutencao.objects.filter(
            inicio__lte=agora,
            fim__gte=agora,
            concluida=False,
            bloquear_acesso=True
        ).first()

        if manutencao:
            # Se for usuário de TI (superuser ou staff), deixa passar
            if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
                return self.get_response(request)
            
            # Caso contrário, exibe a página de manutenção
            return render(request, "ti/manutencao.html", {"manutencao": manutencao}, status=503)

        return self.get_response(request)
