# 🤖 ELISE IA — Documentação Técnica, Instalação e Execução

Este documento reúne todas as especificações técnicas, links oficiais de download, comandos de terminal e o passo a passo completo para instalar, configurar e executar o módulo de Inteligência Artificial **ELISE IA** integrado ao sistema de gestão escolar **ELISE/SIGE**.

---

## 📌 1. Visão Geral do Módulo

O **ELISE IA** é um módulo de **Apoio à Tomada de Decisão (Decision Support System - DSS)** voltado para gestores de escolas particulares de pequeno e médio porte.

### 🛡️ Princípios Inegociáveis (LGPD e Governança)
* **Human-in-the-Loop**: A IA gera diagnósticos e recomendações, mas **nunca grava alterações no banco de dados sem a validação e o clique explícito do gestor**.
* **Direito à Explicação (Art. 20 da LGPD)**: Toda resposta e proposta gerada vem acompanhada de uma justificativa legível em linguagem natural embasada em indicadores objetivos.
* **Privacidade e Execução 100% Local**: Os dados escolares não saem do ambiente da instituição; não há envio para APIs externas de terceiros em nuvem.
* **Arquitetura Determinística**: Números, capacidades de salas, balanços e cálculos financeiros são processados diretamente pelo Django ORM. A LLM atua na síntese, contextualização e explicação em linguagem natural.
* **Escopo Delimitado**: Foco na gestão escolar ativa (Enturmação, Infraestrutura/Salas e Sustentabilidade Financeira). **Zero menção a evasão escolar**.

---

## 💻 2. Especificações de Hardware e Software

As especificações abaixo seguem as medições e requisitos estabelecidos no documento oficial do TCC (*Seção 4, Quadros 1, 2 e 3*).

### 2.1 Especificações da LLM (Modelo)
| Característica | Especificação Técnica |
|---|---|
| **Modelo** | Llama 3.1 8B (variante ajustada para instruções) |
| **Desenvolvedor** | Meta |
| **Identificador no Ollama** | `llama3.1:8b` |
| **Parâmetros** | ~8,03 bilhões |
| **Quantização** | Q4_K_M (~4,9 GB de tamanho em disco) |
| **Janela de Contexto** | Até 128 mil tokens (configurada em 4096 tokens no ELISE) |
| **Idiomas Oficiais** | Português (Brasil), Inglês, Espanhol, Alemão, Francês, Italiano, etc. |
| **Temperatura Adotada** | `0.2` (respostas mais determinísticas e analíticas) |

### 2.2 Requisitos de Hardware e Ambiente
| Recurso | Requisito Mínimo Recomendado | Configuração de Teste (TCC) |
|---|---|---|
| **Memória RAM** | 8 GB livres (ao menos 12 GB no total do sistema) | 12 GB RAM (~11,8 GB utilizáveis) |
| **Processador** | CPU quad-core 2.5 GHz ou superior | CPU de ~3.0 GHz (inferência em CPU) |
| **Armazenamento** | 10 GB de espaço livre em disco | HDD / SSD com espaço livre para o modelo |
| **GPU (Opcional)** | Não obrigatória (acelera a inferência via CUDA/Vulkan se houver) | Execução validada em CPU |
| **Sistema Operacional**| Windows 10/11 (64-bit), Linux ou macOS | Windows 10/11 |
| **Python** | Python 3.11 a 3.14 (compatível com Django 6.0) | Python 3.14 |

---

## 📥 3. Links Oficiais para Download

| Recurso | Link Oficial de Download |
|---|---|
| **Ollama para Windows (Instalador .exe)** | [https://ollama.com/download/windows](https://ollama.com/download/windows) |
| **Download Direto do Instalador Windows** | [https://ollama.com/download/OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe) |
| **Ollama para Linux (Script cURL)** | [https://ollama.com/download/linux](https://ollama.com/download/linux) |
| **Ollama para macOS (.zip)** | [https://ollama.com/download/mac](https://ollama.com/download/mac) |
| **Repositório do Modelo Llama 3.1** | [https://ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) |
| **Repositório Oficial do Ollama (GitHub)**| [https://github.com/ollama/ollama](https://github.com/ollama/ollama) |

---

## 🚀 4. Passo a Passo de Instalação e Configuração

### Passo 1: Instalação do Ollama no Windows
1. Baixe o instalador oficial através do link: [OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe).
2. Execute o instalador `OllamaSetup.exe` (ou via terminal com `.\OllamaSetup.exe /silent`).
3. Verifique se o executável foi adicionado ao PATH do Windows abrindo um novo terminal PowerShell:
   ```powershell
   ollama --version
   ```
   *(Deverá exibir a versão instalada, ex: `ollama version is 0.40.15`)*.

### Passo 2: Baixar o Modelo Llama 3.1 8B
No terminal PowerShell, execute o comando de download (~4,9 GB):
```powershell
ollama pull llama3.1:8b
```
*(O Ollama fará o download das camadas e validará o hash SHA-256 automaticamente).*

### Passo 3: Configurar o Ambiente Virtual Python do SIGE
Abra o terminal na raiz do projeto (`c:\Users\gu268\Projetos\Django-projetos`):
```powershell
# 1. Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar a biblioteca cliente do Ollama
pip install ollama
```

### Passo 4: Executar as Migrações do App de IA no Django
Navegue até o diretório `SIGE` com o `venv` ativado:
```powershell
cd SIGE
python manage.py migrate ia
```
*(Isso criará as tabelas `ia_sessaoassistente`, `ia_mensagemassistente` e `ia_propostadecisao` no banco de dados).*

---

## 🖥️ 5. Comandos de Gerenciamento da LLM

| Objetivo | Comando no Terminal |
|---|---|
| **Iniciar o servidor Ollama** | `ollama serve` |
| **Listar modelos instalados localmente** | `ollama list` |
| **Verificar uso de memória e CPU/GPU** | `ollama ps` |
| **Testar o modelo interativamente no terminal** | `ollama run llama3.1:8b` |
| **Descarregar o modelo da memória RAM** | `ollama stop llama3.1:8b` |
| **Excluir o modelo do disco (se necessário)** | `ollama rm llama3.1:8b` |

---

## 🐍 6. Como Executar o Sistema Completo

Para rodar o ecossistema completo com a IA operacional:

### 1º Terminal: Iniciar o Ollama (Motor de Inferência)
```powershell
ollama serve
```
> *O serviço estará escutando no endereço `http://127.0.0.1:11434`.*

### 2º Terminal: Iniciar o Servidor Django (SIGE)
```powershell
cd c:\Users\gu268\Projetos\Django-projetos
.\venv\Scripts\Activate.ps1
cd SIGE
python manage.py runserver 8000
```
> *O backend estará acessível em `http://127.0.0.1:8000/`.*

---

## 🧪 7. Testes de Validação e Verificação da API

### Teste 1: Testar a API nativa do Ollama via cURL
No prompt de comando ou PowerShell:
```powershell
curl http://localhost:11434/api/chat -d '{"model":"llama3.1:8b","messages":[{"role":"user","content":"Explique o que é o sistema ELISE em uma frase."}],"stream":false}'
```

### Teste 2: Testar a comunicação via Python
Execute no terminal com o ambiente virtual ativado:
```powershell
python -c "from ollama import chat; r = chat(model='llama3.1:8b', messages=[{'role': 'user', 'content': 'Olá, confirme se está pronto.'}]); print(r.message.content)"
```

### Teste 3: Checar o status da IA no Django
Acesse via navegador ou cURL:
```http
GET http://127.0.0.1:8000/ia/status/
```
**Resposta esperada (JSON):**
```json
{
  "status": "ready",
  "assistant": "ELISE IA",
  "version": "1.0.0",
  "llm": {
    "disponivel": true,
    "host": "http://localhost:11434",
    "modelo_configurado": "llama3.1:8b",
    "modelo_presente": true,
    "modelos_instalados": ["llama3.1:8b"]
  }
}
```

### Teste 4: Enviar pergunta ao Assistente (`POST /ia/chat/`)
Requisição com autenticação JWT (ou sessão de gestor logado):
```json
// POST http://127.0.0.1:8000/ia/chat/
// Headers: Authorization: Bearer <seu_token_jwt>
{
  "pergunta": "Qual é a situação de ocupação das salas e matrículas ativas hoje?",
  "tipo": "GERAL"
}
```

---

## ⚙️ 8. Variáveis de Configuração (`SIGE/config/settings.py`)

As seguintes variáveis controlam o comportamento da IA e podem ser customizadas no arquivo `.env`:

```env
# Configurações do Assistente ELISE IA
ELISE_LLM_MODEL=llama3.1:8b
ELISE_LLM_HOST=http://localhost:11434
ELISE_LLM_TEMPERATURE=0.2
ELISE_LLM_CONTEXT_WINDOW=4096
ELISE_LLM_TIMEOUT=120
```

---

## ⚠️ 9. Resolução de Problemas (Troubleshooting)

### Problema 1: `Warning: could not connect to a running Ollama instance`
* **Causa:** O servidor do Ollama não está em execução.
* **Solução:** Abra um terminal e execute `ollama serve`, ou certifique-se de que o ícone do Ollama está ativo na bandeja do sistema (perto do relógio do Windows).

### Problema 2: `modelo_presente: false` no endpoint `/ia/status/`
* **Causa:** O modelo `llama3.1:8b` ainda não foi baixado pelo Ollama.
* **Solução:** Execute `ollama pull llama3.1:8b` no terminal e aguarde a mensagem `success`.

### Problema 3: Erro de Timeout (120 segundos excedidos)
* **Causa:** Em computadores sem GPU dedicada executando sobre disco HDD, a inferência inicial do Llama 3.1 8B pode demorar mais que o normal.
* **Solução:** Aumente o valor de `ELISE_LLM_TIMEOUT=180` no `.env` ou diminua a janela de contexto para `ELISE_LLM_CONTEXT_WINDOW=2048`.

### Problema 4: Falha de memória RAM insuficiente
* **Causa:** Menos de 6 GB de memória RAM livre para o modelo e o sistema operacional simultaneamente.
* **Solução:** Feche navegadores pesados ou aplicativos desnecessários durante os testes e confirme o consumo com `ollama ps`.

---

## 📚 Documentos Correlatos
* **Documento do TCC**: [TCC_Guilherme_Elise.docx](file:///c:/Users/gu268/Projetos/Django-projetos/TCC_Guilherme_Elise.docx)
* **Cronograma das 10 Semanas**: [CRONOGRAMA_SPRINTS_ELISE_IA.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/CRONOGRAMA_SPRINTS_ELISE_IA.md)
* **Diário de Evolução Diária**: [DIARIO_EVOLUCAO_IA.md](file:///c:/Users/gu268/Projetos/Django-projetos/SIGE/docs/DIARIO_EVOLUCAO_IA.md)
