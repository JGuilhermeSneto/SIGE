"""
Interface WSGI do SIGE — usada por servidores de produção (Gunicorn, uWSGI, etc.).

O que é: expõe o callable ``application`` que o servidor HTTP chama para
cada requisição síncrona.

Como funciona: aponta ``DJANGO_SETTINGS_MODULE`` para ``config.settings`` e
delega ao ``get_wsgi_application()`` do Django.

Documentação: https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
