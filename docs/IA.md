# 🤖 ELISE IA — Sistema de Apoio à Tomada de Decisão (DSS)

## 📌 Visão Geral & Escopo do Projeto

O **ELISE IA** é um módulo de Inteligência Artificial voltado ao apoio à tomada de decisão na gestão escolar, integrado nativamente ao ecossistema **ELISE/SIGE**. 

Projetado especificamente para suprir as dores operacionais e estratégicas de **escolas particulares de pequeno e médio porte**, o módulo transforma o grande volume de dados acadêmicos, financeiros e logísticos já centralizados pela plataforma em diagnósticos preditivos e planos de ação práticos.

---

## 🛡️ Diretrizes Conceituais e Éticas (LGPD)

O assistente foi desenhado sob quatro pilares inegociáveis:

1. **Atuação como Sistema de Apoio à Decisão (DSS)**:
   - A IA funciona como uma conselheira e simuladora de cenários, nunca tomando decisões arbitrárias.
2. **Princípio *Human-in-the-Loop***:
   - Nenhuma mutação de dados é realizada de forma autônoma.
   - Toda recomendação gera um registro formal `PropostaDecisao` no banco de dados, que exige aprovação manual e clique explícito do gestor escolar para ter seus efeitos aplicados.
3. **Direito à Explicação (Art. 20 da LGPD)**:
   - Toda resposta e proposta gerada vem acompanhada de uma justificativa clara em linguagem natural, citando os números objetivos e indicadores determinísticos do sistema em que se baseou.
4. **Execução 100% Local & Privacidade Absoluta**:
   - A inferência é executada na infraestrutura local da escola via **Ollama**, sem envio de dados ou dependência de APIs de terceiros em nuvem, garantindo a conformidade com a LGPD e custo zero de requisições.
5. **Zero Menção a Evasão Escolar**:
   - O escopo prático do módulo foca exclusivamente na gestão escolar ativa (enturmação, infraestrutura e sustentabilidade de turmas).

---

## 🏛️ Três Motores Principais de Apoio à Decisão

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ELISE IA - DECISION SUPPORT                     │
├─────────────────────┬──────────────────────┬───────────────────────────┤
│  1. Enturmação e    │  2. Infraestrutura e │  3. Sustentabilidade      │
│     Balanceamento   │     Ocupação de Salas│     Financeira de Turmas  │
├─────────────────────┼──────────────────────┼───────────────────────────┤
│ • Paridade de gênero│ • Alocação por lotação│ • Ponto de equilíbrio     │
│ • Equilíbrio etário │ • Choque de horários │   (breakeven de alunos)   │
│ • Distribuição ética│ • Detecção de salas  │ • Custo docente x receita │
│   de necessidades   │   ociosas/lotadas    │ • Régua de cobrança e     │
│   especiais (PNE)   │ • Gestão de labs     │   renegociação preventiva │
└─────────────────────┴──────────────────────┴───────────────────────────┘
```

---

## ⚙️ Arquitetura Técnica

### 1. Modelo de Linguagem (LLM)
* **Modelo**: Meta Llama 3.1 8B (`llama3.1:8b`).
* **Quantização**: Q4_K_M (~4,9 GB).
* **Ambiente de Execução**: Ollama Local (`http://localhost:11434`).
* **Parâmetros de Inferência**:
  * `temperature`: `0.2` (respostas determinísticas e consistentes).
  * `num_ctx`: `4096` tokens.
  * `timeout`: `120` segundos.

### 2. Camada Determinística (Cálculos no Django)
Para mitigar alucinações numéricas, a LLM **não realiza cálculos matemáticos**. O Django consulta o banco de dados via ORM, calcula os indicadores de forma determinística e os injeta estruturados no prompt da LLM (RAG Simplificado).

---

## 📂 Estrutura de Arquivos (`apps/ia`)

```
SIGE/apps/ia/
├── migrations/
│   └── 0001_initial.py         # Criação das tabelas no banco de dados
├── services/
│   ├── __init__.py             # Exportação das interfaces de serviço
│   ├── llm_service.py          # Integração direta com a API do Ollama (Llama 3.1)
│   └── contexto.py             # Montagem do resumo estruturado de dados do ELISE
├── admin.py                    # Gestão e auditoria de conversas e propostas
├── apps.py                     # Configuração da aplicação Django
├── models.py                   # SessaoAssistente, MensagemAssistente, PropostaDecisao
├── urls.py                     # Rotas REST (/ia/chat/, /ia/status/, /ia/propostas/)
└── views.py                    # Views protegidas com autenticação JWT
```

---

## 🔌 Endpoints da API REST

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/ia/status/` | Status rápido de prontidão do assistente. |
| `GET` | `/ia/status/detalhado/` | Diagnóstico de conexão do Ollama, modelo ativo e métricas. |
| `POST` | `/ia/chat/` | Envio de pergunta do gestor e recebimento da resposta assistida. |
| `POST` | `/ia/propostas/<id>/acao/` | Aprovação (`APROVAR`) ou Rejeição (`REJEITAR`) de proposta. |

---

## 🛠️ Comandos de Gestão do Ollama

Para gerenciar o motor de inferência local no terminal:

```powershell
# 1. Iniciar o servidor Ollama (se não estiver em background)
ollama serve

# 2. Listar modelos baixados
ollama list

# 3. Verificar status do modelo e uso de memória
ollama ps

# 4. Descarregar o modelo da memória RAM
ollama stop llama3.1:8b
```

---

## 📚 Referência Acadêmica
Este módulo faz parte do Trabalho de Conclusão de Curso (TCC) de Guilherme Elise:
* **Documento Base**: `TCC_Guilherme_Elise.docx`
* **Cronograma Detalhado**: [docs/CRONOGRAMA_SPRINTS_ELISE_IA.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/CRONOGRAMA_SPRINTS_ELISE_IA.md)
* **Diário de Evolução Diária**: [docs/DIARIO_EVOLUCAO_IA.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/DIARIO_EVOLUCAO_IA.md)
