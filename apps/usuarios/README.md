# 👥 Módulo de Usuários & Identidade

Este módulo é o pilar de segurança e gestão de acessos (RBAC) do SIGE, gerenciando a identidade de alunos, professores, gestores e responsáveis.

## 🎭 Perfis e Dashboards
O sistema estende o `auth.User` para fornecer interfaces personalizadas:
- **Gestor**: Dashboard executivo com foco em BI e Observabilidade.
- **Professor**: Painel focado em produtividade pedagógica.
- **Aluno**: Interface imersiva (Clean UI) para foco nos estudos.
- **Responsável**: Portal de acompanhamento financeiro e acadêmico.

## 🛡️ Segurança Enterprise
- **2FA (TOTP)**: Autenticação em duas etapas via Google Authenticator.
- **Trilha de Auditoria**: Registro completo de acessos sensíveis em conformidade com a **LGPD**.
- **Password Strength**: Validação agressiva via `zxcvbn`.

## 🏗️ Engenharia
- **Service Layer**: Criação de perfis e vinculação de permissões centralizada em `services/`.
- **Context Processors**: Injeção de notificações e dados de perfil em todos os templates globais.
- **Pytest**: Suíte de testes automatizados com 90%+ de cobertura neste módulo.

> Atualizado em 27/04/2026 — Padrão Jarvis de Segurança Enterprise.
