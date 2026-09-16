# 📋 Plano de Teste de Software — SIGE (Sistema Integrado de Gestão Educacional)
> **Projeto:** SIGE v7.3.2-APEX  
> **Status:** Documento Consolidado de Engenharia de Qualidade

---

## 1. Identificação do Documento
- **Título**: Plano de Teste do SIGE Mission Control
- **Versão**: 7.3.2 (Apex)
- **Data**: 14/05/2026
- **Equipe Responsável**: Pedro Henrique, Israel Cipriano, João Batista e Jose Guilherme
- **Aprovado por**: Jose Guilherme 

---

## 2. Introdução
O plano de teste tem como objetivo garantir que o ecossistema SIGE atenda aos requisitos funcionais (gestão acadêmica e financeira) e não funcionais (segurança SOC, alta disponibilidade IoT e performance mobile), minimizando riscos de regressão e garantindo a integridade dos dados sob conformidade com a LGPD. O foco principal é a validação da convergência entre o hardware (sensores) e o software (dashboard e app mobile).

---

## 3. Escopo dos Testes
| Item | Descrição |
|---|---|
| **Módulos Testados** | Acadêmico, Financeiro, IoT, Segurança (SOC), Mobile API, TI/Backups e Saúde. |
| **Funcionalidades Críticas** | Cálculo de Médias, Registro de Frequência RFID, Bloqueio de IP por Brute Force e Autenticação JWT Mobile. |
| **Exclusões** | Testes de carga em redes externas (devido a limitações de ambiente controlado) e integração com gateways de terceiros em modo produção (uso de Sandbox). |

---

## 4. Objetivos dos Testes
- Identificar e reportar defeitos de sincronização entre o hardware ESP32 e o backend Django.
- Validar a robustez das políticas de segurança e a eficácia da Auto-Blacklist.
- Garantir que a cobertura de testes unitários em módulos core (Financeiro/Acadêmico) seja superior a 75%.
- Assegurar a integridade dos backups imutáveis (WORM).

---

## 5. Tipos de Testes Aplicados
| Tipo de Teste | Objetivo |
|---|---|
| **Testes Unitários** | Validar lógicas isoladas de modelos e services (ex: algoritmo de notas). |
| **Testes de Integração** | Verificar a comunicação entre apps (ex: Financeiro alertando inadimplência ao Acadêmico). |
| **Testes de Casos de Uso** | Simular fluxos reais de usuários: Aluno, Professor e Responsável. |
| **Testes de Estresse (IoT)** | Validar a capacidade de processamento de milhares de mensagens MQTT simultâneas. |

---

## 6. Estratégia de Teste
- **Ferramentas utilizadas**: Pytest (Core), Factory Boy (Mocking), Faker (Massa de Dados), Mosquitto (Broker Test), Postman (API Mobile) e Locust (Carga).
- **Dados de Teste**: Geração dinâmica de 10.000 usuários fictícios e simulação de entradas/saídas sincronizadas via script Python para estresse do barramento de dados.
- **Critérios de Aceitação**: 100% dos testes críticos passando; Cobertura global de código > 62%; Zero vulnerabilidades de nível "High" reportadas pelo Bandit.

---

## 8. Casos de Teste (Aulas & Core)
| ID | Caso de Teste | Passos | Resultado Esperado |
|---|---|---|---|
| **CT001** | Login com credenciais válidas | 1. Abrir o sistema SIGE.<br>2. Inserir matrícula e senha.<br>3. Clicar em “Entrar”. | O usuário deve ser autenticado e redirecionado para o dashboard Apex. |
| **CT002** | Bloqueio de IP por Brute Force | 1. Inserir senha errada 5 vezes seguidas.<br>2. Tentar o 6º acesso. | O sistema deve bloquear o IP e exibi-lo na Blacklist do painel de TI. |
| **CT003** | Frequência via IoT (RFID) | 1. Simular publicação MQTT com UID de cartão válido.<br>2. Verificar diário de classe. | A presença do aluno deve ser registrada automaticamente com o timestamp correto. |
| **CT004** | Geração de Carteirinha Digital | 1. Acessar Perfil Aluno no App Mobile.<br>2. Visualizar QR Code. | O sistema deve gerar um QR Code JWT dinâmico com expiração de 30s. |

---

## 9. Riscos e Mitigações
- **Instabilidade no Broker MQTT** → Mitigação: Implementação de failover automático e buffers locais no firmware do ESP32.
- **Indisponibilidade do Banco de Dados** → Mitigação: Uso de arquitetura Master/Replica e snapshots WORM diários.
- **Falta de cobertura de testes** → Mitigação: Revisão de código (Code Review) mandatória com check de coverage no CI/CD.

---

## 10. Cronograma de Testes (Maio 2026)
| Atividade | Responsável | Início | Conclusão |
|---|---|---|---|
| Planejamento Inicial | Jose Guilherme | 10/05/2026 | 12/05/2026 |
| Execução de Testes Unitários | Equipe Dev | 13/05/2026 | 18/05/2026 |
| **Auditoria de Segurança (SOC)** | Israel Cipriano | 19/05/2026 | 21/05/2026 |
| **Teste de Estresse IoT/MQTT** | Pedro Henrique | 22/05/2026 | 24/05/2026 |
| Validação Mobile API | João Batista | 25/05/2026 | 27/05/2026 |
| Relatório Final Q2 | Jose Guilherme | 28/05/2026 | 30/05/2026 |

---

## 🚀 11. Futuras Tasks & Testes Automatizados
Para garantir a evolução contínua do SIGE Apex, as seguintes frentes de automação estão agendadas para o próximo ciclo:

1. **E2E com Playwright**: Automação completa do fluxo de matrícula do aluno e lançamento de notas pelo professor (Simulação real de navegador).
2. **Stress Testing com Locust**: Simulação de 5.000 dispositivos IoT enviando dados simultâneos para validar a resiliência do Redis e Workers Celery.
3. **Mutation Testing**: Aplicação de testes de mutação no módulo `apps.academico` para garantir que os testes unitários são verdadeiramente eficazes.
4. **Contract Testing**: Implementação de testes de contrato entre o Backend (DRF) e o App Mobile para evitar quebras de interface em updates.
5. **Automação de Penetration Test**: Integração de ferramentas de scan dinâmico (DAST) no pipeline de CI/CD para detectar vulnerabilidades de runtime.

---

## 12. Relatórios e Comunicação
- O status dos testes será compartilhado via **Flower** (monitoramento de tasks) e **Slack/E-mail**.
- Defeitos serão reportados e rastreados no **Trello/GitHub Issues**.
- Reuniões semanais de alinhamento com a equipe de desenvolvimento para revisão do backlog de bugs.

---
**SIGE v7.3.2-APEX: Estabilidade e Excelência em Gestão Educacional.**
