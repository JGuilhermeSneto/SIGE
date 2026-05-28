import logging
from celery import shared_task
from django.conf import settings
from .models import DeviceToken

logger = logging.getLogger(__name__)

@shared_task
def send_push_notification(user_id, title, body, data=None):
    """
    Mock de envio de notificação Push.
    Em produção, integraria com firebase-admin (FCM) ou pyapns2.
    """
    devices = DeviceToken.objects.filter(user_id=user_id, is_active=True)
    if not devices.exists():
        logger.info(f"Nenhum device token ativo encontrado para o user {user_id}")
        return False

    success_count = 0
    for device in devices:
        logger.info(f"Enviando Push para {device.platform} (Token: {device.token[:10]}...): {title}")
        # Aqui viria a lógica do SDK FCM/APNs
        # FCM_SERVER_KEY = settings.FCM_SERVER_KEY
        success_count += 1

    return success_count
