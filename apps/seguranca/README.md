# 🛡️ App: Segurança (Shield)

Módulo central de segurança, auditoria e conformidade LGPD do SIGE.

## Responsabilidades
- Dashboard de segurança unificado (Shield)
- Registro de logs de auditoria (`LogAuditoria`)
- Captura e sanitização de erros de sistema (`LogErro`)
- Blacklist de IPs suspeitos (`BlacklistIP`)
- Gestão de reports de bugs enviados por usuários (`BugReport`)
- Configuração do modo manutenção

## Middlewares
| Middleware | Função |
|---|---|
| `SecurityHardeningMiddleware` | Honeypot para admin, detecção de bots |
| `BlacklistMiddleware` | Bloqueia IPs na lista negra |
| `AuditMiddleware` | Registra acessos a áreas sensíveis |
| `ExceptionMiddleware` | Captura exceções, sanitiza PII, auto-blacklist |
| `ManutencaoMiddleware` | Controle do modo manutenção global |

## Modelos Principais
- `LogAuditoria`, `LogErro`
- `BlacklistIP`, `ConfiguracaoSeguranca`
- `BugReport`

## Permissões
- **TI**: acessa todos os dashboards e pode atualizar status de bugs.
- **Gestor**: visualiza logs de auditoria do seu escopo.
