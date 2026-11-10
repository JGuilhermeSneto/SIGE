"""
Teste Experimental C3 Financeiro (Tabela 13 do TCC): Sustentabilidade e Break-Even.
Valida o Motor 3 (Financeiro) com o modelo Llama 3.1 8B via Ollama.
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
    "Qual é a análise de sustentabilidade financeira das turmas de 2026, "
    "quais turmas estão operando abaixo do ponto de equilíbrio (break-even) "
    "e o que você recomenda para mitigar o déficit operacional?"
)

print("=" * 70)
print("TESTE EXPERIMENTAL FINANCEIRO: MOTOR 3 - SUSTENTABILIDADE E BREAK-EVEN")
print("=" * 70)
print(f"Pergunta: {PERGUNTA}\n")

contexto = montar_contexto(tipo="FINANCEIRO")
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

