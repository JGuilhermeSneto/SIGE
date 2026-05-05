# 🛡️ Módulo de Segurança & Governança (Shield)

O app `apps.seguranca` é a central de comando para a integridade do sistema, auditoria de dados e conformidade com a **LGPD**.

## 📐 Estrutura de Governança
- **Shield Dashboard**: Interface executiva para monitoramento de segurança.
- **Audit Log**: Registro imutável de todas as ações sensíveis (Escrita, Leitura de dados sensíveis).
- **MFA (Multi-Factor Authentication)**: Gestão de tokens e fluxos de autenticação em duas etapas.

## 🚀 Engenharia de Segurança
- **Telemetria de Erros**: Monitoramento em tempo real de exceções e comportamentos anômalos.
- **Proteção Brute-Force**: Integração com `django-axes` para bloqueio dinâmico de IPs suspeitos.
- **Criptografia**: Gestão de chaves para campos sensíveis nos outros módulos.

## 🔗 Integração Multi-Tenant
- Garante o isolamento estrito de logs de auditoria por instituição, impedindo vazamento de trilhas de acesso.

> Atualizado em Maio de 2026 — Central de Segurança Shield v1.0 consolidada.
