"""
Rotas WebSocket da Área de TI.
"""
from django.urls import path
from .consumers import TINotificacoesConsumer

websocket_urlpatterns = [
    path("ws/ti/", TINotificacoesConsumer.as_asgi()),
]
