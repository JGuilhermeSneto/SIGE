# 🗓️ SIGE — Cronograma de Tasks (Maio 2026)

Este documento detalha o planejamento estratégico e as entregas previstas para o mês de maio, focando em robustez, escalabilidade e modernização tecnológica.

---

## 🛠️ Semana 2 (11/05 – 17/05): Transição de Core & Identidade

O foco desta semana é a mudança fundamental na autenticação e o início da migração para o frontend moderno.

### 🔐 Autenticação & Cadastro
- [x] **Identidade Visual Premium**:
    - [x] Unificação visual da tela de login por matrícula.
    - [x] Paridade visual total da tela de 2FA (Premium Style).
- [x] **Melhora no script de população do banco de dados**:
    - [x] Gerar dados coerentes com o novo padrão de matrícula (YYYYTTTUUUU).
    - [x] Simular fluxos de notas e frequências em larga escala.
    - [x] Criação massiva de perfis de Responsáveis e vínculo parental.

### 🖼️ Mídia & Performance (Concluído)
- [x] **Integração com Cloudinary/S3**:
    - [x] Configurar storage externo para fotos reais (Pronto para chaves).
    - [x] Implementar upload e edição de fotos de perfil sem sobrecarregar o disco do Render.
    - [x] Servir mídias via CDN para evitar quedas no servidor de aplicação (Placeholders e CDN ativos).
- [x] **Robustez do Banco de Dados**:
    - [x] Correção de limites de campos para MySQL (EncryptedFields fix).
    - [x] Otimização de performance O(1) (Fim do N+1 nas views de Aluno e Responsável).
    - [x] Migrações de esquema aplicadas com sucesso na Aiven Cloud.

### 👨‍👩‍👧‍👦 Portal do Responsável (Concluído)
- [x] **Sincronização de Templates**: Dashboards com mesma estética do aluno.
- [x] **Gráfico Comparativo**: Visualização Chart.js de desempenho dos dependentes.
- [x] **Controle Parental**: Sistema de Switch e monitoramento funcional.
- [ ] **Avisos Específicos**: Push notifications para responsáveis (Via Mobile).

### ⚛️ Frontend & Integração Inicial
- [ ] **Início da migração React + Vite**:

---

## 🏗️ Semana 3 (18/05 – 24/05): Expansão de Funcionalidades & Integração

Foco em portais especializados e integração total entre os subsistemas.

### 📱 Mobile & IoT
- [ ] **APIs para Mobile**:
    - Endpoints otimizados para consulta de notas, faltas e horários.
- [ ] **IoT do Projeto**:
    - Estabilizar comunicação via MQTT para controle de acesso via matrícula.

### 📱 Mobile & IoT
- [ ] **APIs para Mobile**:
    - Endpoints otimizados para consulta de notas, faltas e horários.
- [ ] **IoT do Projeto**:
    - Estabilizar comunicação via MQTT para controle de acesso via matrícula.

### 👮 Segurança & Permissões
- [ ] **Melhoria do Sistema de Segurança**:
    - Implementar **Modo Manutenção** funcional com bypass para admins.
    - **Cargos e Permissões (RBAC)**: Refinar níveis de acesso com telas próprias para cada perfil.
    - Revisar Hardening de segurança e proteção contra brute-force.

---

## 🚀 Semana 4 (25/05 – 31/05): Otimização, Robustez & Profissionalismo

Semana dedicada a levar o projeto ao nível industrial/profissional.

### ⚡ Otimização de Performance
- [ ] **Otimizar Site do SIGE**:
    - Minificação de assets e compressão Gzip/Brotli.
    - Implementar Lazy Loading massivo.
- [ ] **Melhoria de Consultas (MySQL & Redis)**:
    - Otimizar queries SQL (Select Related / Prefetch).
    - Refinar uso de cache no Redis para diminuir latência.
    - **Escalabilidade**: Configurar autoscaling e monitoramento de queries no Render.

### 🏛️ Arquitetura & Novas Tecnologias
- [ ] **Robustez Profissional**:
    - **Revisar Arquitetura**: Padronizar Service Layer em 100% dos apps.
    - **Kafka/Message Brokers**: Avaliar e iniciar protótipo com Kafka para processamento de eventos de alta carga (Logs/Notificações).
    - **Outras Tecnologias**: Estudar uso de GraphQL para reduzir overfetching no Mobile.

### 🌐 Infraestrutura & Domínio
- [ ] **Domínio Próprio**: Configurar nome de domínio oficial para o sistema.
- [ ] **Melhora no CI/CD**: Pipeline completa com lint, testes, build e deploy automatizado tanto para Back quanto para Front.

---

## 🧪 Tasks Contínuas (Qualidade & Manutenção)

Estas tarefas devem ser executadas de forma transversal durante todo o mês.

- [x] **Ajuste PEP8 & Tipagem**: Infraestrutura configurada e aplicada ao core.
- [x] **Limpeza de Lint**: Redução de 92% dos erros (de 1458 para 112).
- [x] **Cobertura de Testes**: Subir a cobertura global para **80%+**.
- [x] **Melhoria de Código em Geral**: Refatoração de modelos centrais e correção de limites de campos criptografados para MySQL concluída.

---
*Assinado: SIGE Engineering Team — Maio 2026*
