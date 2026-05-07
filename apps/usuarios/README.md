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
- **User-Profile Robust Linkage**: Lógica de cadastro inteligente que permite vincular múltiplos perfis ao mesmo CPF sem duplicar usuários, garantindo a integridade referencial.
- **Context Processors**: Injeção de notificações em tempo real e dados de perfil em todos os templates globais.
- **Administrative Notifications**: Fluxo automático de alertas para gestores na criação de novos usuários (Alunos/Professores).
- **Pytest**: Suíte de testes automatizados com 90%+ de cobertura neste módulo.

> Atualizado em Maio de 2026 — Shield v1.2 e Notificações Administrativas integrados.

## 📌 Quick Wins – Ajustes a implementar hoje (Usuários)

- **Cobertura de testes**: ampliar testes em `services/perfil_service.py` e `views/*` para alcançar >75%.
- **Pre‑commit**: garantir formatação e lint em todo o módulo.
- **Segredos**: certificar que `.env` não seja versionado pelo módulo.
- **Cache de perfis**: usar `cache` ao buscar foto e nome exibido em templates.
- **Headers de segurança**: validar CSP nas páginas de login/registro.
- **Docker‑compose dev**: incluir `postgres` e `redis` para desenvolvimento local do módulo.
