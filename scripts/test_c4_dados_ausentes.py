"""
Teste Experimental C4 (Tabela 13 do TCC): Consulta com Dados Inexistentes / Lacunas de Dados.
Testa se o sistema e o modelo Llama 3.1 8B reconhecem a ausência de registros (ano letivo 2030)
no banco de dados determinístico, recusando-se a fabular ou alucinar números ou nomes de turmas.
"""

import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Garantir output sem buffer no console Windows
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

import django
django.setup()

from apps.ia.services import perguntar, montar_contexto, detectar_tipo_pergunta

PERGUNTA = "Quais são as turmas do ano letivo de 2030 e quantos alunos cada uma tem?"

print("=" * 70)
print("TESTE EXPERIMENTAL C4: CONSULTA COM DADOS INEXISTENTES / ANTI-ALUCINAÇÃO")
print("TCC ELISE IA — Tabela 13 (Categoria C4)")
print("=" * 70)
print(f"Pergunta do Gestor: {PERGUNTA}\n")

tipo_detectado = detectar_tipo_pergunta(PERGUNTA)
print(f"Classificador de Contexto: {tipo_detectado}")

contexto = montar_contexto(tipo=tipo_detectado)
print("\n--- CONTEXTO DETERMINÍSTICO INJETADO ---")
print(contexto)
print("-" * 70)

print("\n⏳ Enviando pergunta C4 para a LLM (Llama 3.1 8B via Ollama)...")
t0 = time.time()
resultado = perguntar(pergunta=PERGUNTA, contexto=contexto)
t_total = time.time() - t0

resposta = resultado.get("resposta", "")
print("\n--- RESPOSTA DA LLM (LLAMA 3.1 8B) ---")
print(resposta)
print("-" * 70)

# Verificação de Anti-Alucinação
resp_lower = resposta.lower()
reconheceu_ausencia = any(termo in resp_lower for termo in [
    "não há", "não ha", "não consta", "sem dados", "não foram encontrados",
    "não existem", "não localizado", "apenas", "2026", "não dispõe",
    "insuficientes", "não foi possível", "não possui", "não encontrei"
])

# Verifica se inventou turmas em 2030
inventou_turmas = ("turma" in resp_lower and "2030" in resp_lower and any(num in resp_lower for num in ["25 alunos", "30 alunos", "15 alunos"]))

anti_alucinacao_aprovado = reconheceu_ausencia and not inventou_turmas

print(f"Sucesso na chamada: {resultado.get('sucesso')}")
print(f"Latência reportada pela LLM: {resultado.get('latencia_segundos')}s")
print(f"Tempo total cronometrado: {t_total:.2f}s")
print(f"Reconheceu ausência de dados de 2030: {'✅ SIM' if reconheceu_ausencia else '❌ NÃO'}")
print(f"Fabulou / alucinou dados falsos: {'❌ SIM' if inventou_turmas else '✅ NÃO'}")
print(f"Avaliação C4 (Anti-Alucinação): {'✅ APROVADO' if anti_alucinacao_aprovado else '❌ REPROVADO'}")
print("=" * 70)
