# Configurações do SIGE

## Visão geral

O diretório `config/` contém as configurações centrais do Django usadas pelo projeto.

## Funcionalidades principais

- Definição de `INSTALLED_APPS` e middlewares.
- Configuração de banco de dados e variáveis de ambiente.
- Rotas globais via `ROOT_URLCONF`.
- Integração com `rest_framework`, `corsheaders` e JWT.

## Estrutura de pastas

- `settings.py` — configurações de ambiente e dependências.
- `urls.py` — roteamento principal do sistema.
- `wsgi.py` / `asgi.py` — pontos de entrada para servidores.
- `__init__.py` — pacote Python.

## Uso principal

Use este app para centralizar configurações e manter o projeto consistente entre ambientes.

## Observações

Mantenha segredos em `.env` e não no repositório.

> Atualizado em 2026-04-22.
