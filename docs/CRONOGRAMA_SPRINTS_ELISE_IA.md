# 📅 Cronograma Geral de Sprints: Assistente ELISE IA — Apoio à Gestão Escolar
**Período:** 16 de Setembro de 2026 a 25 de Novembro de 2026 (10 Semanas)  
**Objetivo Central:** Construção, validação e documentação acadêmica do protótipo **ELISE IA — Sistema de Apoio à Decisão (DSS)** focado em Enturmação, Infraestrutura e Sustentabilidade Financeira de Turmas com Human-in-the-Loop, alimentando progressivamente o documento do TCC (tcc_elise_completo.docx).

---

## 🛡️ Diretrizes Inegociáveis do Projeto
1. **Foco Estrito na Gestão Escolar Ativa**:
   - Organização e balanceamento pedagógico de turmas (idade, gênero, necessidades especiais, lotação).
   - Otimização de infraestrutura física, salas, laboratórios e conflitos de horários na grade.
   - Sustentabilidade financeira de turmas (custo docente x receita de mensalidades) e diagnóstico de inadimplência.
2. **Zero Menção a Evasão Escolar**: qualquer menção ou modelo sobre evasão escolar está estritamente vetado (escopo exclusivo de pesquisa de terceiros).
3. **Human-in-the-Loop Obrigatório**: a IA gera diagnósticos, simulações e justificativas (LGPD/Direito à Explicação), mas **nunca grava alterações no banco de dados sem a aprovação e clique explícito do gestor**.
4. **Rito Diário de Fechamento**:
   - Commit e Push diário no repositório GitHub com padrão semântico (`feat:`, `test:`, `docs:`, `fix:`).
   - Registro diário de evolução no arquivo `docs/DIARIO_EVOLUCAO_IA.md`.
   - Transferência progressiva dos resultados e evidências técnicas para o documento do TCC.

---

## 🧭 Visão Macro das 10 Semanas (16/09 a 25/11)

```
[Semana 1: 16/09 - 20/09] ➔ Fundação da Arquitetura ELISE IA, Modelos e Interface (Drawer/FAB)
[Semana 2: 21/09 - 27/09] ➔ Motor 1: Algoritmo de Enturmação e Balanceamento de Alunos
[Semana 3: 28/09 - 04/10] ➔ Validação Human-in-the-Loop da Enturmação & Redação TCC (Caps. 3 e 5.1)
[Semana 4: 05/10 - 11/10] ➔ Motor 2: Alocação de Infraestrutura e Detecção de Conflitos de Grade
[Semana 5: 12/10 - 18/10] ➔ Otimização de Salas/Turnos & Redação TCC (Caps. 5.2 e 5.3)
[Semana 6: 19/10 - 25/10] ➔ Motor 3: Sustentabilidade Financeira de Turmas & Ponto de Equilíbrio
[Semana 7: 26/10 - 01/11] ➔ Diagnóstico de Inadimplência, Planos de Renegociação & Redação TCC (Cap. 5.4)
[Semana 8: 02/11 - 08/11] ➔ Unificação no Assistente Conversacional (Chat da ELISE IA) & Governança LGPD
[Semana 9: 09/11 - 15/11] ➔ Testes com Gestores, Coleta de Métricas & Redação TCC (Capítulo 6)
[Semana 10: 16/11 - 25/11]➔ Estabilização Final, Fechamento Integral do TCC, Apresentação & Release
```

---

## 📋 Detalhamento das Sprints Semanais e Metas Diárias

### 🟢 SEMANA 1 (16/09 a 20/09) — Fundação da Arquitetura e Interface Base
**Meta da Semana:** Estruturar o app `apps/ia`, criar os modelos de propostas/decisões e colocar a interface do assistente (drawer lateral de chat) funcionando no `base.html`.
- **Qua 16/09**: Estabilização do ambiente (resolução de conexões MySQL), congelamento e backup da versão anterior (`v1.2.0-sige-legacy`), criação do cronograma geral e do diário de bordo.
- **Qui 17/09**: Criação dos modelos em `apps/ia/models.py` (`SessaoAssistente`, `MensagemAssistente`, `PropostaDecisao`). Execução de migrações no banco.
- **Sex 18/09**: Implementação da gaveta lateral moderna (Drawer) no `base.html` conectada ao botão flutuante com feedback visual e atalhos rápidos.
- **Sáb 19/09**: Criação dos primeiros endpoints em `apps/ia/views.py` (`chat_api` e status do assistente). Testes de integração.
- **Dom 20/09**: Fechamento do Sprint 1: Commit/push semanal, registro de evolução e rascunho da estrutura de telas para a Seção 5.6 do TCC.

---

### 🟢 SEMANA 2 (21/09 a 27/09) — Motor 1: Enturmação e Balanceamento de Alunos
**Meta da Semana:** Desenvolver o algoritmo de distribuição e balanceamento de alunos entre turmas.
- **Seg 21/09**: Levantamento das variáveis de enturmação no banco: idade, gênero, turma atual, capacidade máxima da sala e `possui_necessidade_especial`.
- **Ter 22/09**: Implementação do `apps/ia/services/enturmacao_service.py` com lógica de distribuição homogênea e respeito a limites de capacidade.
- **Qua 23/09**: Implementação da regra ética: distribuição equilibrada de alunos com necessidades especiais para garantir atendimento pedagógico adequado.
- **Qui 24/09**: Criação do gerador de justificativas em linguagem natural legível para o gestor (*Direito à Explicação* / LGPD).
- **Sex 25/09**: Testes unitários do algoritmo de enturmação (`apps/ia/tests/test_enturmacao.py`).
- **Sáb 26/09**: Simulação com turmas reais do banco de testes e validação de casos extremos (turma cheia, alunos com perfis divergentes).
- **Dom 27/09**: Fechamento da Semana: Commit/push, registro no diário de bordo sobre o comportamento do algoritmo.

---

### 🟢 SEMANA 3 (28/09 a 04/10) — Validação Human-in-the-Loop da Enturmação & Redação do TCC
**Meta da Semana:** Interface de aprovação manual para o gestor e redação técnica do TCC.
- **Seg 28/09**: Criação dos cartões de proposta (*Cards de Decisão*) na interface com exibição do cenário Atual vs. Proposto.
- **Ter 29/09**: Implementação do endpoint de execução manual segura (`aprovar_proposta_api`), garantindo transações atômicas e log de auditoria do gestor.
- **Qua 30/09**: Botões de rejeição e personalização de proposta na interface pelo gestor.
- **Qui 01/10**: Redação para o TCC: Preenchimento da Seção 3.1 e 3.2 (Arquitetura do ELISE e Módulos).
- **Sex 02/10**: Redação para o TCC: Preenchimento da Seção 5.1 (Origem e preparação dos dados acadêmicos).
- **Sáb 03/10**: Revisão do código e validação de segurança nas permissões de gestor.
- **Dom 04/10**: Fechamento da Semana: Commit/push, atualização do diário de bordo com as primeiras métricas de tempo de resposta.

---

### 🟢 SEMANA 4 (05/10 a 11/10) — Motor 2: Infraestrutura, Ocupação de Salas e Grade Horária
**Meta da Semana:** Desenvolver o diagnóstico de infraestrutura escolar e detecção de conflitos de horários.
- **Seg 05/10**: Mapeamento dos modelos de salas físicas, turnos e `GradeHorario`.
- **Ter 06/10**: Implementação de `apps/ia/services/infraestrutura_service.py` para detecção de conflitos de grade (mesmo professor ou mesma sala em horários coincidentes).
- **Qua 07/10**: Algoritmo de alocação de salas por capacidade (evitar salas superdimensionadas com poucos alunos e salas lotadas).
- **Qui 08/10**: Geração de alertas preventivos de sobrecarga de laboratórios e espaços especializados.
- **Sex 09/10**: Card de proposta de remanejamento de salas/horários para validação humana.
- **Sáb 10/10**: Testes unitários do motor de infraestrutura (`apps/ia/tests/test_infraestrutura.py`).
- **Dom 11/10**: Fechamento da Semana: Commit/push, registro no diário de bordo sobre eficácia da detecção de conflitos.

---

### 🟢 SEMANA 5 (12/10 a 18/10) — Otimização de Espaços & Redação TCC (Caps. 5.2 e 5.3)
**Meta da Semana:** Refinamento do motor de infraestrutura e redação dos requisitos de instalação.
- **Seg 12/10**: Ajuste fino do algoritmo de salas por turno (Manhã, Tarde, Noite).
- **Ter 13/10**: Integração das recomendações de salas ao chat do assistente (respostas contextuais a dúvidas do gestor).
- **Qua 14/10**: Redação para o TCC: Preenchimento da Seção 5.2 (Descrição técnica do modelo/regras de apoio à decisão).
- **Qui 15/10**: Redação para o TCC: Preenchimento da Seção 5.3 (Requisitos de hardware, software e passo a passo de instalação do ambiente).
- **Sex 16/10**: Validação de replicação do ambiente em máquina limpa seguindo o roteiro do TCC.
- **Sáb 17/10**: Criação de dados de demonstração (seed) de infraestrutura para testes.
- **Dom 18/10**: Fechamento da Semana: Commit/push, atualização do diário de bordo.

---

### 🟢 SEMANA 6 (19/10 a 25/10) — Motor 3: Sustentabilidade Financeira de Turmas
**Meta da Semana:** Implementar a análise de viabilidade econômica e ponto de equilíbrio de turmas.
- **Seg 19/10**: Mapeamento do modelo `Fatura`, mensalidades e custos docentes por turma.
- **Ter 20/10**: Implementação de `apps/ia/services/financeiro_analytics.py`: cálculo do ponto de equilíbrio (mínimo de alunos pagantes para a turma cobrir custos).
- **Qua 21/10**: Simulação de cenários: impacto financeiro de fusão ou desdobramento de turmas do mesmo ano.
- **Qui 22/10**: Painel visual de sustentabilidade de turmas no chat do assistente com indicadores de margem.
- **Sex 23/10**: Testes unitários do cálculo financeiro de turmas (`apps/ia/tests/test_financeiro_analytics.py`).
- **Sáb 24/10**: Auditoria de dados confidenciais financeiros à luz da LGPD (não expor dados bancários de responsáveis).
- **Dom 25/10**: Fechamento da Semana: Commit/push, registro da evolução no diário de bordo.

---

### 🟢 SEMANA 7 (26/10 a 01/11) — Diagnóstico de Inadimplência & Redação TCC (Cap. 5.4)
**Meta da Semana:** Motor de análise de inadimplência e redação sobre governança da IA.
- **Seg 26/10**: Diagnóstico de taxa de inadimplência histórica por série/turma.
- **Ter 27/10**: Sugestão de régua de comunicação e cronogramas de renegociação preventiva amigável.
- **Qua 28/10**: Card de proposta de planos de parcelamento sugeridos pela IA para aprovação humana do financeiro.
- **Qui 29/10**: Redação para o TCC: Preenchimento da Seção 5.4 (Configuração do agente, regras de sistema, guarda-corpos éticos e explicabilidade).
- **Sex 30/10**: Redação para o TCC: Preenchimento da Seção 5.5 (Integração à arquitetura Django do ELISE).
- **Sáb 31/10**: Testes integrados entre módulo financeiro e assistente.
- **Dom 01/11**: Fechamento da Semana: Commit/push, atualização do diário de bordo.

---

### 🟢 SEMANA 8 (02/11 a 08/11) — Unificação do Assistente Conversacional & Auditoria LGPD
**Meta da Semana:** Integrar os 3 motores ao fluxo do chat e validar todas as diretrizes da LGPD.
- **Seg 02/11**: Unificação do processamento de linguagem natural no assistente (reconhecimento de intenção entre turmas, salas e finanças).
- **Ter 03/11**: Refinamento visual da gaveta de chat: badges de status, mensagens de boas-vindas com dados em tempo real da escola.
- **Qua 04/11**: Implementação de auditoria rigorosa de propostas (`apps/ia/models.py - PropostaDecisao`) para rastrear quem aprovou cada ação.
- **Qui 05/11**: Validação de segurança: conferência de que nenhum perfil não autorizado (ex: aluno ou responsável) consiga acessar as rotas da IA.
- **Sex 06/11**: Testes end-to-end com simulações completas de perguntas e aprovações.
- **Sáb 07/11**: Redação para o TCC: Preenchimento da Seção 5.6 (Interface de apresentação, capturas de tela e avisos de protótipo experimental).
- **Dom 08/11**: Fechamento da Semana: Commit/push, atualização do diário de bordo.

---

### 🟢 SEMANA 9 (09/11 a 15/11) — Testes de Eficácia, Coleta de Métricas & Redação TCC (Cap. 6)
**Meta da Semana:** Avaliação quantitativa e qualitativa do protótipo e escrita dos Resultados.
- **Seg 09/11**: Coleta de métricas técnicas do protótipo: tempo médio de resposta, índice de balanceamento de turmas (antes vs. depois) e conflitos de salas eliminados.
- **Ter 10/11**: Teste de usabilidade e simulação com roteiro de tarefas de gestão escolar.
- **Qua 11/11**: Tabulação dos resultados técnicos e gráficos comparativos para o TCC.
- **Qui 12/11**: Redação para o TCC: Preenchimento da Seção 6.1 (Resultados do modelo e métricas objetivas).
- **Sex 13/11**: Redação para o TCC: Preenchimento da Seção 6.2 e 6.3 (Avaliação de utilidade para a gestão, benefícios observados, limitações identificadas e honestidade científica).
- **Sáb 14/11**: Revisão das referências bibliográficas do TCC.
- **Dom 15/11**: Fechamento da Semana: Commit/push, fechamento dos relatórios de métricas no diário de bordo.

---

### 🟢 SEMANA 10 (16/11 a 25/11) — Estabilização Final, Fechamento Integral do TCC & Release
**Meta da Semana:** Congelamento final do código, revisão ortográfica/metodológica do TCC e entrega.
- **Seg 16/11**: Redação para o TCC: Preenchimento da Seção 7 (Considerações finais, síntese dos objetivos atendidos e trabalhos futuros).
- **Ter 17/11**: Revisão completa do texto do TCC com a orientadora, alinhamento de formatação ABNT e sumário.
- **Qua 18/11**: Geração do documento final do TCC (`tcc_elise_completo_final.docx` e `.pdf`).
- **Qui 19/11**: Bateria final de testes automatizados (`pytest`) e garantia de cobertura de testes no app `apps/ia`.
- **Sex 20/11**: Limpeza de código, revisão de docstrings e padronização com flake8.
- **Sáb 21/11**: Criação dos slides e roteiro de apresentação do TCC com demonstração prática do protótipo.
- **Seg 23/11**: Simulação e ensaio geral da defesa com o protótipo rodando localmente.
- **Ter 24/11**: Tag final de release no Git: `v2.0.0-elise-ia-final` e backup final `.zip`.
- **Qua 25/11**: **ENTREGA FINAL DO TCC & RELEASE COMPLETO DO PROJETO**. 🚀

---

## 📝 Protocolo Obrigatório do Rito Diário

Ao término de cada sessão diária de trabalho, o seguinte checklist deve ser cumprido:
1. `git status`: verificar todos os arquivos modificados.
2. `git add -A`: preparar alterações.
3. `git commit -m "feat(ia): <descricao semantica do avanco>"`: commit com mensagem clara.
4. `git push origin main`: envio para o repositório remoto no GitHub.
5. Atualização de `docs/DIARIO_EVOLUCAO_IA.md` registrando o que foi construído e o aprendizado obtido no dia.
