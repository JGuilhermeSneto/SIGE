# 🖥️ App: TI (v8.0 Apex)

Módulo central de operações, observabilidade e governança técnica do ecossistema SIGE, com localização total (PT-BR) e design de alta fidelidade.

![Testes](https://img.shields.io/badge/Testes-3%2F3%20passed-brightgreen?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~65%25-yellowgreen?style=flat-square)

## 🚀 Novidades da Versão 8.0 Apex
- **Monitoramento em Tempo Real:** Atualização automática via polling de CPU, RAM, disco e rede com `psutil`.
- **Quantum Snapshots v2:** Módulo de backups com radar de integridade, geolocalização de replicação e políticas de imutabilidade.
- **Cognitive Systems Monitoring:** Painel de IA com monitoramento de VRAM, temperatura de GPU e eventos de agentes neurais (SIGE-GPT / Guardian AI).
- **CI/CD Orchestration:** Visualização em tempo real da topologia de pipeline e logs de build integrados.
- **FinOps Hub:** Monitoramento de custos cloud em tempo real com forecast e detecção de oportunidades de economia.
- **Localização 100% (PT-BR):** Todas as interfaces técnicas (APM, Logs, IAM, CI/CD, IA, FinOps) traduzidas para o contexto brasileiro.

## 📋 Responsabilidades
- Monitoramento de recursos de hardware (CPU/RAM/GPU) e saúde de serviços.
- Gestão de segredos e identidades (Vault & IAM).
- Orquestração de pipelines de deploy e conformidade de backups.
- Governança de custos cloud e auditoria de segurança (SOC).

## 🔗 Estrutura de URLs (Namespace: `ti`)
| Rota | Descrição | Nível de Acesso |
|---|---|---|
| `/ti/` | Dashboard Geral (v8.0) | TI Operador |
| `/ti/soc/` | Security Operations Center | TI Operador |
| `/ti/backups/` | Gestão de Snapshots Quantum | TI Coordenação |
| `/ti/infraestrutura/` | Hub de Serviços e Manutenção | TI Coordenação |
| `/ti/modulo/<slug>/` | Módulos Dinâmicos (APM, Logs, IA, etc) | TI Operador |

## 🛠️ Tecnologias Integradas
- **Monitoramento:** `psutil` + Lógica de telemetria IA para hardware.
- **Segurança:** RBAC avançado, 2FA Mandatório (Feature Flag) e Vault AES-256.
- **Frontend:** Glassmorphism Design System com Chart.js e Canvas Animations.
- **Localização:** Custom i18n layer para interfaces técnicas de alto nível.

---
> Para detalhes técnicos de monitoramento e manutenção, consulte o [**Guia de Infraestrutura (v8.0)**](../../docs/INFRAESTRUTURA.md).
