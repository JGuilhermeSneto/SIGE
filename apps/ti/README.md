# 🖥️ App: TI (Área de Tecnologia da Informação)

Módulo de operações, monitoramento e gestão técnica do ecossistema SIGE.

## Responsabilidades
- Dashboard operacional com métricas em tempo real
- Gestão de chamados e bugs (triagem, análise, resolução)
- Ferramentas de manutenção (limpeza de logs, health check, cache)
- Acesso à documentação técnica e API Swagger
- Integração com o Dashboard de Segurança (Shield)

## URLs (Namespace: `ti`)
| Rota | View | Acesso |
|---|---|---|
| `/ti/` | `painel_ti` | TI Operador |
| `/ti/seguranca/` | `SecurityDashboardView` | TI Operador |
| `/ti/bugs/` | `gestao_bugs` | TI Operador |
| `/ti/documentacao/` | `documentacao_ti` | TI Operador |
| `/ti/api-docs/` | `documentacao_api` | TI Operador |
| `/ti/operacoes/` | `operacoes_ti` | TI Coordenação |

## Permissões
- **TI — Operador**: acesso ao painel, segurança, chamados e documentação.
- **TI — Coordenação**: acesso adicional às operações avançadas (manutenção, DB).
- **Superusuário**: acesso total.

## Template Base
Todos os templates herdam de `ti/base_ti.html`, que inclui a sub-navegação da área.

## Novas Integrações (Maio 2026)
| Recurso | Tecnologia | Arquivo |
|---|---|---|
| **Health Check real** | `django-health-check` | `/health/` |
| **Notificações em tempo real** | `Django Channels` + WebSocket | `consumers.py`, `routing.py` |
| **Monitor de filas** | `Flower` | porta `:5555` (externo) |

> Consulte [`docs/INTEGRACOES_TI.md`](../../docs/INTEGRACOES_TI.md) para detalhes completos.
