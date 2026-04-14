#!/usr/bin/env python
"""
Ponto de entrada da linha de comando do Django (SIGE).

O que é: script padrão que o Django gera para rodar comandos como
``migrate``, ``runserver``, ``createsuperuser``, etc.

Como funciona: define qual módulo de settings usar e delega os argumentos
da linha de comando para ``execute_from_command_line``.
"""

import os
import sys


def main() -> None:
    """Carrega ``config.settings`` e executa o comando Django passado no terminal."""
    # Variável de ambiente que o Django lê para localizar todas as configurações.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
