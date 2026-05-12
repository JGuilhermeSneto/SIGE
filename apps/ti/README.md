# 🖥️ App: TI (v7.2.4)

Módulo central de operações, observabilidade e governança técnica do ecossistema SIGE.

## 🚀 Novidades da Versão 7.2.4
- **Security Operations Center (SOC):** Interface de defesa proativa com monitoramento de incidentes e bloqueio de IPs.
- **Hub de Infraestrutura:** Monitor de latência e console de manutenção unificados em `/ti/infraestrutura/`.
- **API LGPD:** Endpoint para extração de logs de auditoria para conformidade.
- **Telemetria Avançada:** Integração com Chart.js para monitoramento histórico de carga de sistema.

## 📋 Responsabilidades
- Monitoramento de recursos de hardware (CPU/RAM/Disco) via `psutil`.
- Gestão de incidentes técnicos via `BugReport`.
- Execução de scripts de manutenção e limpeza de infraestrutura.
- Governança de acesso e auditoria de segurança.

## 🔗 Estrutura de URLs (Namespace: `ti`)
| Rota | Descrição | Nível de Acesso |
|---|---|---|
| `/ti/` | Dashboard Geral (v7.2) | TI Operador |
| `/ti/soc/` | Security Operations Center | TI Operador |
| `/ti/backups/` | Gestão de Snapshots | TI Coordenação |
| `/ti/infraestrutura/` | Hub de Serviços e Manutenção | TI Coordenação |

## 🛠️ Tecnologias Integradas
- **Diagnóstico:** Lógica personalizada em `utils/diagnostico.py`.
- **Monitoramento:** `psutil` para hardware e `connection.vendor` para DB stats.
- **Segurança:** Blacklist dinâmica de IPs integrada ao middleware de segurança.
- **Frontend:** SIGE Design System com Chart.js para telemetria visual.

---
> Para detalhes técnicos de monitoramento e manutenção, consulte o [**Guia de Infraestrutura (v7.2.4)**](../../docs/INFRAESTRUTURA.md).
> Para detalhes sobre a arquitetura de segurança, consulte a documentação do app `seguranca`.
