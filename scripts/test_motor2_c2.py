"""
Teste Experimental C2 (Tabela 13 do TCC): Comparação e Diagnóstico de Infraestrutura.
Valida o Motor 2 (Infraestrutura) com o modelo Llama 3.1 8B via Ollama.
"""

import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.ia.services import perguntar, montar_contexto

PERGUNTA = (
    "Como gestor escolar, quais são as condições de conservação física das salas de aula "
    "e quais ações imediatas de infraestrutura e alocação de mobiliário você recomenda para "
    "os ambientes Sala 101 e Sala 102?"
)

print("=" * 70)
print("TESTE EXPERIMENTAL C2: MOTOR 2 - INFRAESTRUTURA E CONSERVAÇÃO")
print("=" * 70)
print(f"Pergunta: {PERGUNTA}\n")

contexto = montar_contexto(tipo="INFRAESTRUTURA")
print("--- CONTEXTO DETERMINÍSTICO INJETADO ---")
print(contexto)
print("-" * 70)

t0 = time.time()
resultado = perguntar(pergunta=PERGUNTA, contexto=contexto)
t_total = time.time() - t0

print("\n--- RESPOSTA DA LLM (LLAMA 3.1 8B) ---")
print(resultado["resposta"])
print("-" * 70)
print(f"Sucesso: {resultado.get('sucesso')}")
print(f"Latência reportada pelo serviço: {resultado.get('latencia_segundos')}s")
print(f"Tempo total cronometrado: {t_total:.2f}s")
print(f"Modelo: {resultado.get('modelo')}")
print("=" * 70)

