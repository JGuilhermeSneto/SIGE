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


