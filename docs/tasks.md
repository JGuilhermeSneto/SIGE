# 🗓️ SIGE — Backlog de Desenvolvimento (v7.3.0+)

Este documento detalha os objetivos estratégicos para as próximas fases, focando em performance, cobertura total de testes e expansão financeira.

---

## ⚡ 1. Performance & Otimização de Banco de Dados
*Objetivo: Latência mínima e consultas otimizadas.*
- [ ] **Auditoria de Queries (N+1):** Identificar e corrigir gargalos nas views acadêmicas e financeiras usando `select_related` e `prefetch_related`.
- [ ] **Otimização de Índices:** Revisar chaves estrangeiras e campos de busca para garantir indexação correta no MySQL.
- [ ] **Cache de Alto Nível:** Implementar cache granular de fragmentos de template para áreas de alta carga.

## 🛡️ 2. Estabilidade Absoluta (Meta: 100% de Cobertura)
*Objetivo: Garantir que nenhuma alteração quebre o core do sistema.*
- [ ] **Testes de Camada de Serviço:** Cobrir 100% da lógica de negócio nos apps `academico`, `financeiro` e `usuarios`.
- [ ] **Testes de Integração de API:** Validar fluxos completos de autenticação e troca de dados.
- [ ] **Mocks de Infraestrutura:** Simular falhas de Redis, S3 e SMTP para validar a resiliência do sistema.

## 📱 3. Fundação Mobile & Frontend Moderno
*Objetivo: Preparar o SIGE para o ecossistema multi-plataforma.*
- [ ] **Arquitetura API REST:** Implementação completa do Django Rest Framework (DRF).
- [ ] **Autenticação JWT:** Configurar tokens seguros para acesso via App Mobile.
- [ ] **Refatoração Frontend:** Início da modernização da UI com foco em componentes reutilizáveis e performance (Vite/React Integration).

## 💰 4. Ciclo Financeiro v2
*Objetivo: Automação total do faturamento escolar.*
- [ ] **Integração Real de Pagamentos:** Conectar gateways (Asaas/Efí) para processamento de Pix e Boletos.
- [ ] **Webhooks de Conciliação:** Baixa automática de faturas em tempo real.
- [ ] **Módulo de NF-e:** Geração automática de notas fiscais de serviço.

## 🔐 5. Segurança & TI (Melhoria Contínua)
*Objetivo: Governança de dados de nível bancário.*
- [ ] **Refinamento da Área de TI:** Adicionar monitoramento de locks de banco e tráfego de rede.
- [ ] **Hardening de Segurança:** Revisão constante de middlewares, proteção contra CSRF/XSS e auditoria LGPD.
- [ ] **Manutenção Preditiva:** Alertas automáticos baseados em telemetria de hardware.

---

## 📅 Cronograma Semanal (Próximas Tasks)

### Semana Atual (Foco: Otimização & Testes)
- [ ] Mapeamento de queries lentas no Hub de Infraestrutura.
- [ ] Expansão de testes para o app `usuarios` (Meta: 70% parcial).
- [ ] Ajustes finos no visual do dashboard principal (v7.3).

### Próxima Semana (Foco: API & Financeiro)
- [ ] Protótipo da API de Notas e Frequência.
- [ ] Modelagem da integração com Gateway de Pagamento.

---
*SIGE v7.3.0 — Rumo à excelência técnica total.*
