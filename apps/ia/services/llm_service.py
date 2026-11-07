import time
import logging
from typing import Dict, Any, Optional
import ollama
from django.conf import settings

logger = logging.getLogger(__name__)

# Parâmetros padrão definidos no TCC (Seção 4.1 a 4.6)
MODELO = getattr(settings, "ELISE_LLM_MODEL", "llama3.1:8b")
HOST = getattr(settings, "ELISE_LLM_HOST", "http://localhost:11434")
TEMPERATURA = getattr(settings, "ELISE_LLM_TEMPERATURE", 0.2)
CONTEXT_WINDOW = getattr(settings, "ELISE_LLM_CONTEXT_WINDOW", 4096)
TIMEOUT = getattr(settings, "ELISE_LLM_TIMEOUT", 120)

# Prompt de sistema oficial documentado no TCC (Código 3 e Seção 4.6)
PROMPT_SISTEMA = (
    "Você é o assistente de apoio à decisão do ELISE, sistema de gestão "
    "de escolas particulares. Responda sempre em português do Brasil, de "
    "forma clara e objetiva. Use exclusivamente os dados fornecidos na "
    "seção DADOS DO ELISE; não invente números nem fatos. Se os dados "
    "forem insuficientes, diga isso explicitamente. Justifique suas "
    "conclusões citando os valores em que se baseou. Apresente suas "
    "respostas como sugestões para o gestor avaliar, nunca como decisões "
    "finais. Os dados estão anonimizados: não tente identificar pessoas. "
    "Lembre-se de que você faz parte de um protótipo experimental."
)


def get_client() -> ollama.Client:
    """Retorna uma instância configurada do cliente Ollama."""
    return ollama.Client(host=HOST, timeout=TIMEOUT)


def verificar_disponibilidade_llm() -> Dict[str, Any]:
    """
    Verifica se o servidor Ollama está acessível e se o modelo configurado
    está presente e disponível para inferência.
    """
    try:
        cliente = get_client()
        modelos = cliente.list()
        # modelos pode retornar lista de dicts ou objeto ModelList
        lista_nomes = []
        if hasattr(modelos, "models"):
            lista_nomes = [m.model for m in modelos.models]
        elif isinstance(modelos, dict) and "models" in modelos:
            lista_nomes = [m.get("name") or m.get("model") for m in modelos["models"]]
        
        modelo_presente = any(MODELO in nome for nome in lista_nomes)
        return {
            "disponivel": True,
            "host": HOST,
            "modelo_configurado": MODELO,
            "modelo_presente": modelo_presente,
            "modelos_instalados": lista_nomes,
        }
    except Exception as e:
        logger.warning(f"Ollama offline ou inacessível no host {HOST}: {e}")
        return {
            "disponivel": False,
            "host": HOST,
            "modelo_configurado": MODELO,
            "modelo_presente": False,
            "erro": str(e),
        }


def perguntar(pergunta: str, contexto: str = "") -> Dict[str, Any]:
    """
    Envia a pergunta do gestor e o contexto determinístico do ELISE
    para o modelo Llama 3.1 local via Ollama, medindo a latência.
    """
    cliente = get_client()
    inicio = time.time()
    
    conteudo_usuario = (
        f"DADOS DO ELISE:\n{contexto if contexto else 'Nenhum dado específico carregado no momento.'}\n\n"
        f"PERGUNTA DO GESTOR:\n{pergunta}"
    )

    try:
        resposta = cliente.chat(
            model=MODELO,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": conteudo_usuario},
            ],
            options={
                "temperature": TEMPERATURA,
                "num_ctx": CONTEXT_WINDOW,
            },
        )
        latencia = round(time.time() - inicio, 2)
        texto_resposta = resposta.message.content if hasattr(resposta, "message") else resposta["message"]["content"]
        
        return {
            "sucesso": True,
            "resposta": texto_resposta,
            "latencia_segundos": latencia,
            "modelo": MODELO,
            "aviso": "Protótipo experimental: valide as sugestões antes de tomar qualquer decisão.",
        }
    except Exception as e:
        latencia = round(time.time() - inicio, 2)
        logger.error(f"Erro ao consultar o Ollama/LLM: {e}")
        return {
            "sucesso": False,
            "resposta": (
                "O assistente de IA está temporariamente indisponível no ambiente local. "
                f"Verifique se o Ollama está em execução com o modelo '{MODELO}'."
            ),
            "erro": str(e),
            "latencia_segundos": latencia,
            "modelo": MODELO,
            "aviso": "Protótipo experimental (em modo de contingência).",
        }
