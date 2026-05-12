# 🛠️ Área de TI — Operações e Manutenção
> **Versão:** 1.0 — Maio 2026
> **Responsável:** Equipe de TI (Coordenação/Senior)

---

## 📋 Visão Geral

A Área de TI do SIGE oferece ferramentas avançadas para monitoramento, manutenção e operações administrativas do sistema. Esta documentação cobre as funcionalidades disponíveis no painel TI e suas melhores práticas de uso.

## 🎯 Funcionalidades Principais

### 1. Painel de Visão Geral
- **Status Cards Dinâmicos**: KPIs em tempo real (bugs novos, erros recentes, IPs bloqueados, acessos auditados)
- **Cache Otimizado**: Dados cacheados por 5 minutos para performance
- **Refresh Manual**: Botão de atualização para dados em tempo real
- **Timestamp de Atualização**: Indicação clara da última atualização dos dados

### 2. Dashboard de Segurança (Shield)
- **Auditoria Completa**: Logs de acessos a áreas sensíveis
- **Telemetria de Erros**: Captura e análise de exceções do sistema
- **Monitoramento de Intrusões**: IPs bloqueados e tentativas suspeitas
- **Paginação Inteligente**: Navegação eficiente em grandes volumes de dados
- **Filtros Avançados**: Pesquisa e ordenação por data, usuário e tipo

### 3. Operações Administrativas
- **Limpeza de Logs**: Remoção automática de logs antigos (>30 dias, >90 dias)
- **Health Checks**: Verificações de saúde do banco, cache e sistema
- **Gerenciamento de Cache**: Limpeza manual do cache do sistema
- **Limpeza de Sessões**: Remoção de sessões de usuário expiradas
- **Export de Configurações**: Visualização das configurações atuais

## 🔧 Operações Disponíveis

### Limpeza de Logs
```bash
# Via Interface Web (Recomendado)
1. Acesse Área de TI → Operações
2. Clique em "Limpar logs > 30 dias" ou "Limpar logs > 90 dias"
3. Confirme a operação
```

**Impacto:**
- Reduz tamanho do banco de dados
- Melhora performance de queries
- Mantém conformidade com LGPD (logs antigos removidos)

### Health Check do Sistema
```bash
# Verificações Automáticas:
✅ Banco de dados: Conectividade e resposta
✅ Cache: Funcionamento do Redis/LocMem
✅ Usuários: Contagem de registros ativos
```

**Uso:** Execute diariamente para monitoramento proativo.

### Gerenciamento de Cache
```bash
# Operação: Limpeza Total do Cache
- Remove todas as chaves cacheadas
- Força recálculo de dados no próximo acesso
- Útil após mudanças críticas no sistema
```

## 📊 Monitoramento e KPIs

### Cards de Status (Painel TI)
| Card | Descrição | Frequência |
|------|-----------|------------|
| Bugs Novos | Relatórios não triados | Atualização em tempo real |
| Erros Recentes | Exceções dos últimos 7 dias | Cache 5min |
| IPs Bloqueados | Endereços ativos na blacklist | Cache 5min |
| Acessos Auditados | Logs de auditoria recentes | Cache 5min |

### Dashboard de Segurança
| Seção | Conteúdo | Paginação |
|-------|----------|-----------|
| Auditoria | Logs de acesso LGPD | 25 por página |
| Erros | Telemetria de exceções | 20 por página |
| Bugs | Relatórios de problemas | 15 por página |
| Blacklist | IPs bloqueados | 20 por página |

## 🔒 Permissões e Acesso

### Níveis de Acesso
- **TI — Operador**: Acesso ao painel e dashboard de segurança (somente leitura)
- **TI — Coordenação**: Acesso completo incluindo operações administrativas
- **Superusuário**: Acesso irrestrito a todas as funcionalidades

### Guards de Segurança
- Autenticação obrigatória em todas as views
- Verificação de permissões em tempo real
- Logs de auditoria para todos os acessos

## 🚀 Melhores Práticas

### Manutenção Preventiva
1. **Diária**: Executar health check pela manhã
2. **Semanal**: Verificar e limpar logs antigos
3. **Mensal**: Revisar configurações e atualizar documentação

### Monitoramento Contínuo
1. Acompanhe os cards de status diariamente
2. Configure alertas para picos anômalos
3. Mantenha o dashboard de segurança sempre visível

### Operações Críticas
1. Sempre faça backup antes de operações destrutivas
2. Teste operações em ambiente de desenvolvimento primeiro
3. Documente todas as intervenções manuais

## 📈 Performance e Otimização

### Cache Strategy
- **Painel TI**: 5 minutos de cache para balancear atualização e performance
- **Dashboard Segurança**: Dados frescos com paginação para escalabilidade
- **Operações**: Resultados em tempo real sem cache

### Query Optimization
- `select_related()` em todas as queries de auditoria
- Paginação Django para controle de memória
- Índices otimizados no banco de dados

## 🐛 Troubleshooting

### Problemas Comuns
| Problema | Sintoma | Solução |
|----------|---------|---------|
| Cache Stale | Dados desatualizados | Usar botão refresh ou aguardar 5min |
| Paginação Lenta | Carregamento demorado | Verificar índices do banco |
| Health Check Falha | Erro no banco/cache | Verificar configurações de conexão |

### Logs de Debug
- Todos os erros são capturados no `LogErro`
- Operações administrativas são auditadas
- Use o dashboard de segurança para investigação

## 📚 Referências

- [SECURITY.md](SECURITY.md) — Camadas de proteção do sistema
- [LOGGING.md](LOGGING.md) — Sistema de observabilidade
- [INFRASTRUCTURE.md](INFRASTRUCTURE.md) — Configuração da infraestrutura

---

**Última atualização:** 12 de Maio de 2026
**Versão:** 1.0</content>
<parameter name="filePath">c:\Users\gu268\Projetos\Django-projetos\SIGE\docs\TI_OPERATIONS.md