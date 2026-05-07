# 🗓️ SIGE — Cronograma de Tasks (Maio 2026)

Este documento detalha o planejamento estratégico e as entregas previstas para o mês de maio, focando em robustez, escalabilidade e modernização tecnológica.

---

## 🛠️ Semana 2 (11/05 – 17/05): Transição de Core & Identidade

O foco desta semana é a mudança fundamental na autenticação e o início da migração para o frontend moderno.

### 🔐 Autenticação & Cadastro
- [ ] **Mudar de e-mail para Matrícula**:
    - Implementar padrão `YYYYTTTUUUU` (Ano, ID Turma, ID Usuário).
    - Refatorar `AbstractUser` e `AuthenticationBackend`.
    - Atualizar endpoints de login no mobile e IoT.
- [ ] **Melhora no script de população do banco de dados**:
    - Gerar dados coerentes com o novo padrão de matrícula.
    - Simular fluxos de notas e frequências em larga escala.

### 🖼️ Mídia & Performance (Render Stability)
- [ ] **Integração com Cloudinary/S3**:
    - Configurar storage externo para fotos reais.
    - Implementar upload e edição de fotos de perfil sem sobrecarregar o disco do Render.
    - Servir mídias via CDN para evitar quedas no servidor de aplicação.

### ⚛️ Frontend & Integração Inicial
- [ ] **Início da migração React + Vite**:
    - Setup do projeto React no repositório.
    - Mover os primeiros templates Django (Login/Dashboard) para telas reais em React.
    - Configurar APIs do frontend com JWT e Refresh Tokens.
    - Hospedagem do frontend em provedores gratuitos (Netlify/Vercel).

---

## 🏗️ Semana 3 (18/05 – 24/05): Expansão de Funcionalidades & Integração

Foco em portais especializados e integração total entre os subsistemas.

### 👨‍👩‍👧‍👦 Portal do Responsável
- [ ] **Desenvolvimento do Portal**:
    - Telas de acompanhamento acadêmico e financeiro.
    - Notificações de frequência e avisos via API.

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

- [ ] **Ajuste PEP8 & Tipagem**: Garantir 100% de conformidade com PEP8 e uso de MyPy para tipagem estática.
- [ ] **Limpeza de Lint**: Resolver todos os warnings e erros de Pylint/Flake8.
- [ ] **Cobertura de Testes**: Subir a cobertura global para **80%+**.
- [ ] **Melhoria de Código em Geral**: Refatoração de funções complexas e remoção de código duplicado.

---
*Assinado: SIGE Engineering Team — Maio 2026*
