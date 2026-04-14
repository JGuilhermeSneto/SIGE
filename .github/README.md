# SIGE · Automation & CI/CD

Este diretório contém as configurações para automação do ciclo de desenvolvimento, integração contínua e segurança.

## Conteúdo

- **`workflows/`**: Contém arquivos `.yml` que definem as ações do **GitHub Actions**.
  - No `push` para a branch `main`, são executados: Linting (Flake8), Formatação (Black) e Testes Unitários.
- **`dependabot.yml`**: Configuração do Dependabot para monitorar e sugerir atualizações de segurança para as bibliotecas listadas no `requirements.txt`.

## Manutenção

Sempre que uma nova regra de qualidade de código ou uma nova suíte de testes (ex: testes de UI com Selenium) for adicionada, os arquivos em `workflows/` devem ser atualizados para garantir que o pipeline de CI reflita essas novas exigências.

## Novas áreas sensíveis a CI (Abr/2026)

- Fluxos de calendário escolar (evento/aula suspensa/feriado/prova).
- Fluxos de gabarito (liberação manual e automática por prazo).
- Notificações de aluno (nota, chamada, correção e gabarito).

Recomendação: ampliar gradualmente testes automatizados para esses cenários em PRs futuros.
