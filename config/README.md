# SIGE · Project Configuration (Notas)

Este é o diretório raiz de configuração do Django. Embora o nome da pasta seja `notas/` (devido à inicialização original do projeto), este é o "coração" administrativo que conecta todos os módulos.

## Arquivos e Responsabilidades

- **`settings.py`**: Configurações centrais do projeto. Utiliza o `python-decouple` para separar segredos (como chaves de API e senhas de banco) em um arquivo `.env` fora do controle de versão.
- **`urls.py`**: O roteador mestre do sistema. Ele não define lógica, mas inclui os roteadores de cada aplicativo (principalmente o do `core`).
- **`wsgi.py` / `asgi.py`**: Interfaces de entrada para servidores web (Gunicorn, Uvicorn). O `asgi.py` está preparado para lidar com comunicações assíncronas se necessário no futuro.
- **`__init__.py`**: Marca este diretório como um pacote Python.

## Diretrizes de Manutenção

1. **Segurança**: Nunca coloque senhas ou chaves secretas diretamente no `settings.py`. Use o arquivo `.env`.
2. **Ambientes**: O `settings.py` está configurado para alternar entre SQLite (desenvolvimento) e MySQL (produção) automaticamente com base nas variáveis de ambiente.
3. **Segurança em produção**: mantenha `DEBUG=False`, configure `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, cookies seguros e CORS/CSRF trusted origins para o domínio público.
4. **Inclusão de Apps**: Sempre adicione novos aplicativos instalados na lista `INSTALLED_APPS` aqui.

## Atualizações recentes relevantes para configuração

- O projeto passou a usar notificações persistentes de aluno (modelo em `apps.academico.models.desempenho`), exigindo migration nova.
- O domínio de atividades recebeu campos de liberação de gabarito (migration dedicada).

### Checklist pós-pull

Sempre rode:

```bash
python manage.py migrate
```

Migrations recentes esperadas:

- `academico.0003_atividadeprofessor_gabarito_liberacao`
- `academico.0004_notificacaoaluno`
