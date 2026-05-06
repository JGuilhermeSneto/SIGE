# 🛡️ Módulo de Segurança & Governança (Shield v1.2)

O app `apps.seguranca` é a central de comando para a integridade do sistema, auditoria de dados e defesa ativa contra ameaças cibernéticas.

## 📐 Estrutura de Governança
- **Shield Dashboard (v1.2)**: Monitoramento avançado de segurança e gestão do Hardening.
- **Audit Log**: Registro imutável de todas as ações em dados sensíveis (Leitura/Escrita).
- **Hardening Middleware**:
    - **Admin Honeypot**: Detecta e bane bots em acessos não autorizados ao `/admin/`.
    - **Auto-Blacklist**: Inteligência para banimento dinâmico de IPs geradores de erros críticos.
- **Sanitização de PII (Scrubbing)**: Remoção automática de CPFs e E-mails de logs técnicos (LGPD compliance).
- **MFA (Multi-Factor Authentication)**: Autenticação em duas etapas nativa.

## 🚀 Engenharia de Segurança & TI
- **Workflow de Bugs**: Reporte com validação de **Magic Numbers** (assinatura binária) para evitar injeção de malware via upload.
- **Painel de Resolução**: Gestão do ciclo de vida de bugs com **notificações automáticas** para o usuário.
- **Modo Manutenção**: "Kill-switch" administrativo para isolamento técnico do sistema.
- **Proteção Brute-Force**: Bloqueio dinâmico via `django-axes`.
- **Criptografia AES-256**: Proteção de dados em repouso.

## 🔗 Integração Multi-Tenant
- Isolamento estrito de logs e auditoria por instituição.

> Atualizado em Maio de 2026 — Shield v1.2 (Hardening) — Defesa Ativa e Governança de Dados.
