# 🗓️ SIGE — Backlog de Desenvolvimento (v7.3.2+)

Este documento detalha os objetivos estratégicos para as próximas fases, focando em performance, cobertura total de testes e expansão financeira.

---

## ⚡ 1. Performance & Otimização de Banco de Dados
*Objetivo: Latência mínima e consultas otimizadas.*
- [ ] **Auditoria de Queries (N+1):** Identificar e corrigir gargalos nas views acadêmicas e financeiras usando `select_related` e `prefetch_related`.
- [ ] **Otimização de Índices:** Revisar chaves estrangeiras e campos de busca para garantir indexação correta no MySQL.
- [ ] **Cache de Alto Nível:** Implementar cache granular de fragmentos de template para áreas de alta carga.

## 🛡️ 2. Estabilidade Absoluta (Meta: 100% de Cobertura)
*Objetivo: Garantir que nenhuma alteração quebre o core do sistema.*
- [x] **Testes de Camada de Usuários:** Cobertura inicial de 70% atingida.
- [ ] **Testes de Camada de Serviço:** Cobrir 100% da lógica de negócio nos apps `academico` e `financeiro`.
- [ ] **Testes de Integração de API:** Validar fluxos completos de autenticação e troca de dados.
- [ ] **Mocks de Infraestrutura:** Simular falhas de Redis, S3 e SMTP para validar a resiliência do sistema.

## 📱 3. Fundação Mobile & Frontend Moderno
*Objetivo: Preparar o SIGE para o ecossistema multi-plataforma.*
- [x] **Arquitetura API REST:** Implementação completa do Django Rest Framework (DRF).
- [x] **Autenticação JWT:** Configurar tokens seguros para acesso via App Mobile.
- [ ] **Refatoração Frontend:** Início da modernização da UI com foco em componentes reutilizáveis e performance (Vite/React Integration).

## 💰 4. Ciclo Financeiro v2
*Objetivo: Automação total do faturamento escolar.*
- [ ] **Integração Real de Pagamentos:** Conectar gateways (Asaas/Efí) para processamento de Pix e Boletos.
- [ ] **Webhooks de Conciliação:** Baixa automática de faturas em tempo real.
- [ ] **Módulo de NF-e:** Geração automática de notas fiscais de serviço.

## 🔐 5. Segurança & TI (Concluído na v7.3.2)
*Objetivo: Governança de dados de nível bancário.*
- [x] **Refinamento da Área de TI:** Adicionado monitoramento de GPU, telemetria IA e localização total.
- [x] **Mission Control God-Tier:** Implementação total de todos os 8 grupos de gestão (Operações, Segurança, Infra, Compliance, Dados, Config, Suporte, Estratégico).
- [x] **Hub de 18+ Módulos:** Templates finalizados para DNS, SSL, DB Admin, LGPD, DR, IA, FinOps, Workers, etc.
- [x] **Hardening de Segurança:** Implementação de MFA Mandatório via Feature Flags e Auditoria LGPD integrada ao IAM.
- [x] **Cofre de Snapshots Quantum:** Sistema de backup imutável com geolocalização.

---

## 📅 Cronograma Semanal (Próximas Tasks)

### Semana Atual (Foco: API REST & Mission Control)
- [x] Mapeamento de endpoints para o app `academico`.
- [x] Configuração do SimpleJWT para autenticação mobile.
- [x] Finalização de todos os módulos da Área de TI (18+ templates).
- [x] Integração de dados dinâmicos no Diagnóstico TI.

---
*SIGE v7.3.2 — Rumo à excelência técnica total.*
