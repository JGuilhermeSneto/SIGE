"""
Sinais da app TI - Captura eventos e envia notificações em tempo real via WebSocket.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from axes.models import AccessLog
from datetime import datetime


@receiver(post_save, sender=AccessLog)
def notificar_novo_login(sender, instance, created, **kwargs):
    """
    Dispara notificação em tempo real quando um novo login bem-sucedido é registrado.
    Enviado via WebSocket para o painel de TI.
    """
    if not created:
        return

    channel_layer = get_channel_layer()

    # Formatar data e hora
    data_hora = instance.attempt_time.strftime("%d/%m/%Y %H:%M:%S")
    
    # Truncar user_agent para apenas os primeiros 70 caracteres
    user_agent = instance.user_agent[:70] if instance.user_agent else "N/A"

    async_to_sync(channel_layer.group_send)(
        "ti_notificacoes",
        {
            "type": "novo_login",  # Isso chama o método `async def novo_login` no consumer
            "usuario": instance.username or "Desconhecido",
            "ip": instance.ip_address,
            "dispositivo": user_agent,
            "data_hora": data_hora,
            "timestamp": int(instance.attempt_time.timestamp()),
        },
    )
