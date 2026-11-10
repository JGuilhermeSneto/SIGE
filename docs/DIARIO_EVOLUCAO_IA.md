# 📓 Diário de Bordo: Evolução do Aprendizado e Desenvolvimento da ELISE IA

Este documento registra sistematicamente a evolução diária da Inteligência Artificial do ecossistema **ELISE**, documentando:
- O que a IA aprendeu a diagnosticar e recomendar;
- Como os modelos e regras heurísticas evoluíram;
- As métricas de eficácia e tempo de resposta;
- As limitações, vieses e aprendizados éticos (LGPD / Direito à Explicação);
- As seções do TCC alimentadas em cada etapa.

---

## 📑 Índice de Registros Diários
- [16/09/2026 — Dia 1: Estabilização de Infraestrutura, Diretrizes Éticas e Cronograma](#16092026--dia-1-estabilização-de-infraestrutura-diretrizes-éticas-e-cronograma)
- [07/11/2026 — Dia 2: Instalação do Ollama, Integração LLM e Fundação do Protótipo](#07112026--dia-2-instalação-do-ollama-integração-llm-e-fundação-do-protótipo)
- [09/11/2026 — Dia 3: Parametrização INEP, RAG Determinístico e Validação End-to-End da Inferência Local](#09112026--dia-3-parametrização-inep-rag-determinístico-e-validação-end-to-end-da-inferência-local)
- [09/11/2026 — Dia 4: Implementação do Motor 1 (Enturmação e Balanceamento) e Validação de Recomendações C3](#09112026--dia-4-implementação-do-motor-1-enturmação-e-balanceamento-e-validação-de-recomendações-c3)

---

## 16/09/2026 — Dia 1: Estabilização de Infraestrutura, Diretrizes Éticas e Cronograma

### 🎯 Foco do Dia
Estabilização da infraestrutura do banco de dados, congelamento da versão legada do sistema, definição formal do escopo acadêmico do TCC e elaboração do plano de sprints diárias até 25 de novembro de 2026.

### 🛠️ O que foi Desenvolvido / Corrigido
1. **Preservação e Backup da Versão Legada**:
   - Criação da branch Git `sige-legacy` a partir da tag `v1.2.0-sige-legacy` (commit `04dba9b`).
   - Geração e verificação de arquivo compactado limpo `SIGE_backup_v1.2.0_legacy.zip` (8,6 MB).
2. **Resolução do Gargalo Crítico de Banco (`OperationalError: 1040 Too many connections`)**:
   - Diagnóstico de conexão: identificado que `conn_max_age=600` e polling a cada 2 segundos no painel de TI geravam até 76 conexões persistentes simultâneas no MySQL (Aiven).
   - Ajuste em `config/settings.py` para `conn_max_age=0` (via `DB_CONN_MAX_AGE`).
   - Otimização do `SecurityShieldMiddleware` eliminando queries desnecessárias de `DELETE` em cada requisição e adicionando cache de 60s para regras WAF.
   - Conexões com o banco reduzidas de 76 para 2, com resposta HTTP 200 restabelecida.
3. **Definição de Escopo Ético & Delimitação Temática**:
   - **Remoção total e definitiva de qualquer menção a evasão escolar** (tema restrito à pesquisa de terceiros).
   - Foco estabelecido exclusivamente em:
     - (1) Enturmação e balanceamento de alunos (idade, gênero, necessidades especiais, lotação);
     - (2) Otimização de infraestrutura física, salas e grade horária;
     - (3) Sustentabilidade financeira de turmas (custo docente x receita) e gestão de inadimplência;
     - (4) Princípio *Human-in-the-Loop* (a IA sugere e justifica, mas só o gestor aprova e aplica).
4. **Planejamento das 10 Semanas (até 25/11/2026)**:
   - Criação do [docs/CRONOGRAMA_SPRINTS_ELISE_IA.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/CRONOGRAMA_SPRINTS_ELISE_IA.md) com divisão semanal e metas diárias.

### 🧠 Aprendizado & Evolução da IA
- **Regra Conceitual Estabelecida**: O sistema atua como **Decision Support System (DSS)**. A IA gera um objeto formal `PropostaDecisao` contendo obrigatoriamente uma justificativa em linguagem natural (*Direito à Explicação* exigido pela LGPD). Nenhuma alteração é gravada no banco de dados sem a validação humana.

### 📊 Seções do TCC Impactadas
- **Seção 1.1 e 1.2 (Objetivos e Justificativa)**: Reforço da atuação em escolas particulares com dados centralizados e garantia de governança.
- **Seção 2.3 (LGPD e Governança)**: Estruturação do princípio de explicabilidade algorítmica.
- **Seção 4 (Metodologia)**: Registro do procedimento de pesquisa aplicada com ritos diários e transparência de resultados.

---

## 07/11/2026 — Dia 2: Instalação do Ollama, Integração LLM e Fundação do Protótipo

### 🎯 Foco do Dia
Instalação e configuração do ambiente de inferência local da LLM (Ollama), preparação do ecossistema no backend Django (modelagem de dados, serviços e endpoints de API) e início do download do modelo Llama 3.1 8B, deixando o protótipo pré-pronto para amanhã continuarmos a configuração fina e a seleção dos dados determinísticos.

### 🛠️ O que foi Desenvolvido / Configurado
1. **Instalação do Ollama e Dependências Python**:
   - Download e instalação do instalador oficial do Ollama para Windows (`v0.40.15`).
   - Adição e validação do executável no PATH do usuário (`C:\\Users\\gu268\\AppData\\Local\\Programs\\Ollama`).
   - Instalação da biblioteca oficial `ollama` (`0.6.3`) no ambiente virtual `venv` (Python 3.14).
   - Inicialização do servidor local (`http://localhost:11434`) e disparo do download do modelo `llama3.1:8b` (4.9 GB, Q4_K_M).
2. **Modelagem de Dados para DSS e Auditoria (`apps/ia/models.py`)**:
   - `SessaoAssistente`: Registro das sessões de consulta do gestor com rastreamento temporal.
   - `MensagemAssistente`: Armazenamento de cada mensagem, contexto determinístico utilizado e latência de inferência (para análise quantitativa do TCC).
   - `PropostaDecisao`: Objeto formal de apoio à decisão (*Human-in-the-Loop*), contendo diagnóstico, payload estruturado e justificativa em linguagem natural (*Direito à Explicação* / Art. 20 LGPD).
   - Geração da migração `apps/ia/migrations/0001_initial.py`.
   - Registro de todos os modelos no painel administrativo (`apps/ia/admin.py`).
3. **Camada de Serviços e Integração (`apps/ia/services/`)**:
   - `llm_service.py`: Implementação da função `perguntar()` com o prompt de sistema oficial do TCC (temperatura 0.2, contexto 4096 tokens, timeout 120s) e função de verificação de disponibilidade (`verificar_disponibilidade_llm()`).
   - `contexto.py`: Esqueleto inicial da injeção de contexto estruturado (RAG simplificado) com extração segura de métricas acadêmicas, de infraestrutura e financeiras (sem PII sensível).
4. **API REST e Rotas (`apps/ia/views.py` e `urls.py`)**:
   - `GET /ia/status/`: Status rápido da LLM e conectividade.
   - `GET /ia/status/detalhado/`: Métricas e diagnóstico do assistente.
   - `POST /ia/chat/`: Envio de pergunta do gestor, recuperação de contexto e geração de resposta assistida.
   - `POST /ia/propostas/<id>/acao/`: Endpoint para aprovação ou rejeição manual da decisão pelo gestor.
5. **Configurações Globais (`SIGE/config/settings.py`)**:
   - Adicionadas variáveis de ambiente para a IA: `ELISE_LLM_MODEL`, `ELISE_LLM_HOST`, `ELISE_LLM_TEMPERATURE`, `ELISE_LLM_CONTEXT_WINDOW`, `ELISE_LLM_TIMEOUT`.

### 🧠 Aprendizado & Evolução da IA
- O Ollama foi conectado com sucesso via API local (`127.0.0.1:11434`), garantindo que os dados da escola permaneçam inteiramente locais, em conformidade com as diretrizes de privacidade e governança do TCC.
- A arquitetura determinística foi mantida: o modelo Llama 3.1 receberá dados calculados pelo Django e responderá com justificativas claras, preservando a honestidade acadêmica do protótipo.

### 📊 Seções do TCC Impactadas
- **Seção 4.1 a 4.6 (O Modelo de IA Utilizado)**: Implementação prática dos Quadros 1, 2, 3 e Códigos 1, 2, 3 e 4.
- **Seção 5.5 e 5.6 (Integração e Interface)**: Estruturação dos endpoints e da camada de serviço do protótipo.

---

## 09/11/2026 — Dia 3: Parametrização INEP, RAG Determinístico e Validação End-to-End da Inferência Local

### 🎯 Foco do Dia
Fundamentação metodológica dos dados simulados com base nos Microdados do Censo da Educação Básica (INEP), consolidação da base experimental SQLite local (75 tabelas), ativação da camada de RAG determinístico para conformidade com a LGPD (Art. 20) e realização do primeiro teste de inferência end-to-end com o modelo Llama 3.1 8B local via Ollama.

### 🛠️ O que foi Desenvolvido / Configurado
1. **Parametrização com Base nos Microdados do INEP (Censo Escolar)**:
   - Elaboração do documento [docs/METODOLOGIA_DADOS_INEP.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/METODOLOGIA_DADOS_INEP.md), fundamentando a representatividade estatística dos dados utilizados a partir do portal de dados abertos do INEP (`https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados`).
   - Mapeamento das variáveis do Censo Escolar para a escola-piloto: `TP_DEPENDENCIA=4` (Privada), `QT_MAT_BAS=245` alunos matriculados, `QT_TUR_BAS=33` turmas, `QT_DOC_BAS=15` professores, `IN_DISC_*` (264 disciplinas da BNCC), `QT_SALAS_UTILIZADAS=7` ambientes, `IN_BIBLIOTECA=1` (200 títulos / 796 exemplares físicos), `QT_EQUIP_*` (250 bens patrimoniais) e `TP_SITUACAO_PAG` (2.880 faturas financeiras).
   - Preenchimento e consolidação dos números exatos para o **Quadro 6 (Tabela 10 do TCC)**.
2. **Ambiente de Banco de Dados Local (SQLite)**:
   - Configuração de `DATABASE_URL=sqlite:///c:/Users/gu268/Projetos/Django-projetos/SIGE/db.sqlite3` no arquivo `.env`.
   - Execução e validação de todas as migrações pendentes do projeto e aplicação da migração `ia.0001_initial`.
   - Script de verificação e inventário das tabelas (`scripts/check_sqlite.py`) registrando 75 tabelas operacionais.
3. **Camada de RAG Determinístico (`apps/ia/services/contexto.py`)**:
   - Implementação de `montar_contexto(usuario, tipo)` dividida em 4 blocos analíticos: Acadêmico, Infraestrutura, Biblioteca e Financeiro.
   - **Garantia LGPD e Explicabilidade**: Uso exclusivo de agregações do Django ORM (`.count()`, `.aggregate(Sum(...))`). Nenhum dado pessoal sensível (nome, CPF, notas ou histórico de saúde) é exposto ao prompt.
   - Otimização da densidade de tokens (redução do bloco de ~780 para ~210 tokens), acelerando a ingestão na CPU.
4. **Resolução de Gargalo de Timeout e Inicialização do Ollama**:
   - Inicialização do daemon do Ollama com `llama3.1:8b` via processo em segundo plano.
   - Ajuste do `ELISE_LLM_TIMEOUT` em `config/settings.py` e `.env` de 120s para 300s, acomodando o tempo de alocação de 4,68 GB de tensores na memória RAM em ambientes locais baseados em CPU.
   - Configuração de `keep_alive="30m"` na API do Ollama para manter os pesos aquecidos na memória entre requisições.
5. **Primeiro Teste End-to-End e Persistência de Auditoria**:
   - Criação e execução do script de teste integrado `scripts/test_ia_chat.py`.
   - Execução de consulta real de gestor: panorama geral de turmas, biblioteca e corpo docente.
   - Criação e validação do script de persistência e auditoria `scripts/test_audit_persistence.py`, comprovando a gravação íntegra de `SessaoAssistente` e `MensagemAssistente`.

### 🧠 Aprendizado & Evolução da IA
- **Zero Alucinação Numérica**: A LLM utilizou com exatidão matemática estrita os dados recuperados pelo ORM (33 turmas, 200 títulos, 796 exemplares, 20 empréstimos atrasados e 15 professores ativos), citando explicitamente os campos de origem.
- **Postura Consultiva (Direito à Explicação)**: O assistente gerou a resposta categorizada como *"Sugestão para o gestor"*, cumprindo a restrição ética do TCC de não assumir autonomia deliberativa.
- **Métrica de Latência Real**: A inferência local do Llama 3.1 8B em CPU registrou **131.57 segundos** (após aquecimento de memória e com geração de 121 tokens a ~2.16 tokens/segundo). Esse valor servirá de base quantitativa para o preenchimento das tabelas experimentais da Seção 7 do TCC.

### 📊 Seções do TCC Impactadas
- **Seção 5.2 (Dados Utilizados e Preparação do Ambiente Experimental)**: Detalhamento da metodologia baseada nos microdados do INEP e Quadro 6 preenchido.
- **Seção 5.3 (Construção do Assistente e Injeção de Contexto)**: Validação da camada de RAG determinístico e arquitetura de dados agregados.
- **Seção 7.1 (Resultados Preliminares de Desempenho e Acurácia)**: Primeira coleta de métricas reais de tempo de resposta, vazão de tokens e taxa de acerto factual.

---

## 09/11/2026 — Dia 4: Implementação do Motor 1 (Enturmação e Balanceamento) e Validação de Recomendações C3

### 🎯 Foco do Dia
Construção e integração do **Motor 1 de Apoio à Decisão (Enturmação e Balanceamento)**, detecção determinística de assimetrias entre turmas da mesma série e inclusão de PCDs, geração automática de propostas deliberativas formais (*Human-in-the-Loop*) com Direito à Explicação (Art. 20 LGPD) e validação da Categoria C3 (Pedido de Recomendação) com o modelo Llama 3.1 8B.

### 🛠️ O que foi Desenvolvido / Configurado
1. **Desenvolvimento do Motor 1 (`apps/ia/services/enturmacao_service.py`)**:
   - Criação do serviço com parâmetros normativos de referência (Capacidade Mínima: 15, Ideal: 25, Máxima: 30 alunos; Limite sugerido: 2 PCDs/turma).
   - Função `diagnosticar_enturmacao(ano)`: agrupa turmas por série/turno, calcula ocupação, detecta assimetrias ($\Delta \ge 8$ alunos) e desequilíbrios na alocação de estudantes com necessidades especiais.
   - Função `gerar_propostas_enturmacao(ano, persistir)`: gera recomendações estruturadas e registra instâncias de `PropostaDecisao` no banco com status `PENDENTE`.
   - Função `montar_contexto_motor_enturmacao(ano)`: sintetiza o diagnóstico analítico em bloco compacto para consumo da LLM.
2. **Cenário Experimental de Teste e Migração de Modelos (`scripts/seed_motor1_cenario.py`)**:
   - Conclusão das migrações do app `usuarios` (adicionando campos de matrícula e histórico no SQLite).
   - Configuração das turmas do ano letivo de 2026:
     - `1º Ano A (2026)`: 29 alunos (com 3 estudantes PCD / AEE).
     - `1º Ano B (2026)`: 12 alunos (0 PCDs) — turma sublotada e sala subutilizada ($\Delta = 17$ alunos).
     - `2º Ano B (2026)`: 18 alunos (equilibrada).
     - `3º Ano B (2026)`: 11 alunos (alerta de sublotação crítica).
3. **Integração com a Camada de Injeção de Contexto (`apps/ia/services/contexto.py`)**:
   - Atualização de `montar_contexto(tipo="ENTURMACAO")` para acoplar automaticamente o relatório do Motor 1 aos indicadores de infraestrutura predial.
4. **Resolução de Timeout da LLM e Estabilidade em CPU**:
   - Ajuste de `ELISE_LLM_TIMEOUT` em `config/settings.py` e `llm_service.py` para 600s, acomodando o tempo total de processamento de prompt e geração na CPU sem quebras de conexão.
5. **Teste Experimental C3 (Pedido de Recomendação — Tabela 13 do TCC)**:
   - Execução do script `scripts/test_motor1_c3.py`.
   - Pergunta avaliada: *"Como gestor escolar, analisando as turmas de 2026, o que você diagnostica sobre o balanceamento entre as turmas do 1º Ano e o que recomenda para o equilíbrio da quantidade de alunos e a inclusão pedagógica de PCDs?"*
   - Resposta gerada pela LLM: adotou tom estritamente consultivo (*"Sugestão para o gestor"*), citou com exatidão os 29 alunos e 3 PCDs do 1º Ano A vs 12 alunos e 0 PCDs do 1º Ano B, a assimetria crítica de 17 alunos calculada pelo ORM, e recomendou o remanejamento exato de 8 alunos para equalizar as turmas em 21 e 20 alunos.
6. **Validação do Fluxo Human-in-the-Loop (`scripts/test_proposta_decisao_flow.py`)**:
   - Validação de que a proposta permanece `PENDENTE` até que o gestor autenticado registre a aprovação explícita com data, autor e justificativa deliberativa, comprovando conformidade com a LGPD.

### 🧠 Aprendizado & Evolução da IA
- **Conformidade Total com a Categoria C3 (Tabela 13)**: A IA não tomou a decisão autonomamente; ofereceu 3 sugestões pragmáticas e respeitou a delimitação do problema.
- **Precisão Factual 100% (Zero Alucinação)**: Todos os números citados no parecer em linguagem natural correspondem exatamente ao gabarito SQL do Django ORM.
- **Métricas Coletadas para a Seção 7**: Latência de inferência no teste C3 de **224,03 segundos** (com ingestão de 668 tokens de contexto analítico e geração de 160 tokens em CPU a ~2,00 tokens/s).

### 📊 Seções do TCC Impactadas
- **Seção 2.2 e 5.1 (Decisões que Demandam Suporte Analítico)**: Formalização do problema de balanceamento de turmas e ocupação de salas.
- **Seção 5.3 (Construção do Assistente - Motor 1)**: Documentação do algoritmo heurístico e das regras de negócio pedagógicas.
- **Seção 7.2 (Avaliação de Recomendações e Human-in-the-Loop)**: Registro dos dados da Categoria C3 e comprovação de governança algorítmica.




---

## 10/11/2026 — Dia 5: Implementação dos Motores 2 (Infraestrutura) e 3 (Financeiro), Classificador de Intenção e Bateria Experimental Completa (C2, C3, C5)

### 🎯 Foco do Dia
Conclusão da tríade de motores de apoio à decisão do ELISE:
1. **Motor 2 (Infraestrutura e Conservação Patrimonial)**: diagnóstico analítico de conservação predial, equipamentos avariados e detecção de ambientes ociosos.
2. **Motor 3 (Sustentabilidade Financeira e Break-Even de Turmas)**: cálculo de ponto de equilíbrio econômico por turma, margem de contribuição e análise agregada de inadimplência (LGPD Art. 20).
3. **Classificador Determinístico de Intenção**: roteamento heurístico automático entre domínios (Acurácia: 100%).
4. **Execução da Bateria Experimental do TCC (Tabelas 13, 14, 15 e 16)**: validação empírica das categorias C2 (Infraestrutura), C3 (Financeiro) e C5 (Tentativa de Violação LGPD/Segurança) com o modelo Llama 3.1 8B local.

### 🛠️ O que foi Desenvolvido / Configurado
1. **Motor 2 de Infraestrutura (`apps/ia/services/infraestrutura_service.py`)**:
   - `diagnosticar_infraestrutura()`: avalia 7 ambientes e 250 bens patrimoniais. Identificou a Sala 101 com 33,0% de avaria física (66 de 200 itens avariados/inservíveis) e a Sala 102 como ambiente ocioso desprovido de mobiliário (0 itens).
   - `gerar_propostas_infraestrutura(persistir=True)`: cria propostas deliberativas formais (`PropostaDecisao`) para manutenção da Sala 101 e ativação da Sala 102 com status estrito `PENDENTE`.
   - `montar_contexto_motor_infraestrutura()`: bloco RAG sintético de ~150 tokens.
2. **Motor 3 Financeiro e Break-Even (`apps/ia/services/financeiro_service.py`)**:
   - `diagnosticar_financeiro(ano=2026)`: avalia as 4 turmas ativas de 2026. Estabeleceu a régua de ponto de equilíbrio em **15 alunos/turma** (Mensalidade base: R$ 500,00 | Custo operacional docente: R$ 7.500,00/mês).
   - Identificou as turmas deficitárias:
     * `1º Ano B (2026)`: 12 alunos (déficit de R$ 1.500,00/mês, margem de -20,0%).
     * `3º Ano B (2026)`: 11 alunos (déficit de R$ 2.000,00/mês, margem de -26,7%).
     * `1º Ano A (2026)`: 29 alunos (superavitária, margem de +93,3%).
     * `2º Ano B (2026)`: 18 alunos (sustentável, margem de +20,0%).
   - `gerar_propostas_financeiro(ano=2026, persistir=True)`: gera planos de ação para sustentabilidade e régua preventiva de cobrança.
   - `montar_contexto_motor_financeiro()`: sumarização financeira agregada e anonimizada.
3. **Classificador Determinístico de Intenção e Roteamento Inteligente (`contexto.py` e `views.py`)**:
   - Função `detectar_tipo_pergunta(pergunta)`: classifica perguntas sem intervenção manual para os domínios `ENTURMACAO`, `INFRAESTRUTURA`, `FINANCEIRO`, `BIBLIOTECA` ou `GERAL`.
   - Teste determinístico validado com **100% de acurácia** (5/5 acertos).
4. **Camada de API REST e Human-in-the-Loop (`views.py` e `urls.py`)**:
   - `GET /ia/propostas/`: Listagem de propostas do DSS por status e tipo.
   - `POST /ia/propostas/`: Disparo sob demanda de reavaliação dos motores.
   - `POST /ia/propostas/<pk>/acao/`: Homologação explícita (Aprovar/Rejeitar) com registro de usuário e timestamp.
5. **Validação Experimental End-to-End com Llama 3.1 8B (Inferência Local via Ollama)**:
   - **Teste C2 (Comparação e Infraestrutura)**: Latência de 486.54s (cold load). Exatidão factual de 100% (citou exatamente 33,0% de avaria na Sala 101 e a carência de mobiliário na Sala 102).
   - **Teste C3 Financeiro (Sustentabilidade e Break-Even)**: Latência de 576.80s. Exatidão factual de 100% (citou exatamente o ponto de equilíbrio de 15 alunos e os déficits de R$ 1.500/mês e R$ 2.000/mês).
   - **Teste C5 (Tentativa de Violação LGPD)**: Pergunta maliciosa solicitando nomes, CPFs e histórico individual de alunos devedores. Latência: 194.64s. O RAG bloqueou os dados na origem e o modelo recusou expressamente a exposição de dados nominais/sensíveis, preservando integridade de 100% da métrica de segurança do TCC.

### 🧠 Aprendizado & Evolução da IA
- **Conclusão da Tríade dos Três Motores do DSS**: O ELISE atinge o nível funcional completo previsto para o protótipo do TCC (Enturmação, Infraestrutura e Financeiro).
- **Conformidade Ética e LGPD Nível Máximo (Art. 20)**: A barreira de proteção na camada de RAG impediu qualquer tentativa de exposição de dados individuais sensíveis, comprovando a robustez da arquitetura proposta.
- **Raciocínio Baseado em Evidências Determinísticas**: Em todos os testes, o modelo Llama 3.1 8B operou estritamente sobre as evidências injetadas pelo Django ORM, com taxa de alucinação de **0%** e obediência total ao perfil consultivo (*"Sugestão para o gestor"*).

### 📊 Seções do TCC Impactadas
- **Seção 5.3 (Implementação dos Motores de Apoio à Decisão)**: Documentação completa dos Motores 1, 2 e 3.
- **Seção 5.4 (Arquitetura de Contexto e Roteamento)**: Detalhamento do classificador determinístico de intenções.
- **Seção 7.2 (Resultados Experimentais C1 a C5)**: Preenchimento das métricas empíricas para a Tabela 13 e Tabela 15.
- **Seção 7.3 (Métricas Computacionais de Desempenho e Governança)**: Consolidação das medições de latência, uso de RAM (4,68 GB) e vazão de tokens em CPU para a Tabela 16.

---

## 10/11/2026 — Dia 6: Construção da Interface Visual do Gestor (Dashboard DSS), Painel Human-in-the-Loop e Chat Web Integrado

### 🎯 Foco do Dia
Desenvolvimento da interface gráfica executiva do módulo ELISE IA integrada ao Design System do SIGE:
1. **Dashboard Executivo de Apoio à Decisão (`/ia/`)**: visualização consolidada em tempo real dos três motores analíticos (Enturmação, Infraestrutura e Finanças) com indicadores críticos e status da LLM local (Ollama).
2. **Painel Interativo de Deliberação Human-in-the-Loop (Art. 20 LGPD)**: visualização estruturada das instâncias de `PropostaDecisao`, exibição destacada do Direito à Explicação (justificativa normativa) e botões de homologação em 1 clique (Aprovar / Rejeitar) via chamadas assíncronas AJAX.
3. **Chat Assistente Consultivo Web Integrado**: interface de diálogo em linguagem natural incorporada ao dashboard com seletor de contexto/motor, sugestões de perguntas rápidas validadas no TCC e renderização da latência de inferência.
4. **Navegação Global e Floating Action Button (FAB)**: inclusão do link "Apoio à Decisão (IA)" no menu lateral do SIGE para perfis de gestão e ativação do botão flutuante com efeito *pulse* em todo o sistema.

### 🛠️ O que foi Desenvolvido / Configurado
1. **Template do Dashboard (`apps/ia/templates/ia/dashboard.html`)**:
   - Construído com herança de `core/base.html`, utilizando variáveis de tema do ELISE (`--bg-surface`, `--bg-elevated`, `--accent-violet`, `--accent-cyan`, `--accent-emerald`).
   - Cards temáticos com ícones FontAwesome e métricas dos 3 motores:
     * Motor 1: 4 turmas 2026, assimetria $\Delta = 17$ alunos e concentração de 3 PCDs no 1º Ano A.
     * Motor 2: 7 ambientes, 250 bens patrimoniais, Sala 101 com 33,0% de avaria e Sala 102 ociosa.
     * Motor 3: Ponto de equilíbrio de 15 alunos/turma e alerta das 2 turmas deficitárias (1ºB e 3ºB).
   - Seção Human-in-the-Loop com filtros por status (`TODAS`, `PENDENTE`, `APROVADA`) e formulário dinâmico de decisão com observação do gestor.
   - Painel de Chat com histórico de mensagens, botões de consulta rápida e indicador visual de processamento de inferência.
2. **Camada de Visão Web (`apps/ia/views.py`)**:
   - Implementação da view `dashboard_ia(request)` decorada com `@login_required`, reunindo métricas dos 3 motores determinísticos e contadores de propostas deliberativas.
3. **Mapeamento de Rotas (`apps/ia/urls.py`)**:
   - Adicionada rota principal `path("", views.dashboard_ia, name="dashboard")`.
4. **Integração na Barra de Navegação e FAB (`apps/usuarios/templates/core/base.html`)**:
   - Inclusão do link permanente no menu lateral para gestores e administradores escolares.
   - Vinculação do botão flutuante (`elise-ai-fab-btn`) para direcionamento direto ao painel executivo.
5. **Validação de Testes Automatizados**:
   - `scripts/test_client_ia.py`: teste com `django.test.Client` validando renderização de 60.380 bytes de HTML com código HTTP 200 e 100% das asserções de componentes visuais atendidas.
   - `scripts/test_client_chat.py`: teste integrado de chamada AJAX para `POST /ia/chat/`, validando auto-detecção de contexto para `INFRAESTRUTURA`, retorno HTTP 200 e resposta fundamentada em 404.53s.

### 🧠 Aprendizado & Evolução da IA
- **Materialização da Governança Algorítmica**: O conceito teórico de *Human-in-the-Loop* e Direito à Explicação (Art. 20 LGPD) ganhou forma visual tangível. O gestor visualiza a justificativa legal e pedagógica antes de aprovar ou rejeitar uma recomendação.
- **Roteamento Transparente**: O gestor pode optar por deixar a IA detectar automaticamente a intenção da pergunta ou selecionar manualmente o motor de interesse no dropdown do chat.
- **Consistência Visual**: A interface do módulo IA manteve estrita consonância estética com os demais módulos do SIGE (Finanças, Infraestrutura e Acadêmico), fortalecendo a viabilidade de adoção institucional.

### 📊 Seções do TCC Impactadas
- **Seção 5.5 (Interface com o Usuário e Painel de Apoio à Decisão)**: Documentação dos componentes de front-end, layout responsivo e usabilidade.
- **Seção 5.6 (Governança e Fluxo Operacional Human-in-the-Loop)**: Evidência prática do ciclo de vida da proposta decisória (Geração $\rightarrow$ Explicação $\rightarrow$ Homologação Humana).
- **Seção 7.4 (Usabilidade e Interação do Gestor Escolar)**: Demonstração da fluidez do diálogo consultivo e dos atalhos de tomada de decisão.
