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

