import os
import sys

# Adiciona o diretório raiz do SIGE ao PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.ia.services.contexto import montar_contexto
from apps.ia.services.llm_service import perguntar

pergunta = (
    "Como gestor escolar, preciso de um panorama executivo: quantas turmas temos "
    "cadastradas, qual é a situação atual do acervo da biblioteca e quantos professores "
    "estão ativos na nossa instituição?"
)
contexto = montar_contexto(tipo='GERAL')

print("=" * 60)
print("DADOS DO ELISE (CONTEXTO RAG DETERMINÍSTICO INJETADO):")
print("=" * 60)
print(contexto)

print("\n" + "=" * 60)
print("INICIANDO INFERÊNCIA NO LLAMA 3.1 8B...")
print("=" * 60)
resultado = perguntar(pergunta=pergunta, contexto=contexto)

print("\n" + "=" * 60)
print("RESULTADO DO TESTE DE APOIO À DECISÃO (ELISE IA):")
print("=" * 60)
print(f"Sucesso: {resultado['sucesso']}")
print(f"Latência de Inferência: {resultado['latencia_segundos']} s")
print(f"Modelo: {resultado['modelo']}")
print(f"Aviso Ético/Legal: {resultado['aviso']}")
print("\nRESPOSTA GERADA PELO ASSISTENTE:\n")
print(resultado['resposta'])
