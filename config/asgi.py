"""
ASGI config do SIGE — suporte a HTTP e WebSockets via Django Channels.

Expõe o callable ASGI como `application`.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import apps.ti.routing as ti_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # Requisições HTTP normais (views, admin, API)
        "http": django_asgi_app,

        # Conexões WebSocket (painel TI em tempo real)
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    ti_routing.websocket_urlpatterns
                )
            )
        ),
    }
)
