"""
Interface ASGI do SIGE — entrada para servidores assíncronos (Uvicorn, Daphne, etc.).

O que é: expõe ``application`` no protocolo ASGI (HTTP/WebSockets assíncronos).

Como funciona: igual ao WSGI em relação ao ``DJANGO_SETTINGS_MODULE``, mas
via ``get_asgi_application()`` — preparado para Django async / canais no futuro.

Documentação: https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
