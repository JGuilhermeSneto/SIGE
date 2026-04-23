from celery import shared_task
from django.contrib.auth import get_user_model
from .models.desempenho import Notificacao

@shared_task
def enviar_notificacao_assincrona(user_id, titulo, mensagem, tipo='AVISO', url_destino=None):
    """
    Tarefa assíncrona para criar notificações sem travar o request do usuário.
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        Notificacao.objects.create(
            usuario=user,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            url_destino=url_destino
        )
        return f"Notificação enviada para {user.username}"
    except User.DoesNotExist:
        return "Usuário não encontrado"
