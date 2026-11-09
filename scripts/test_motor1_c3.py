import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.ia.services.contexto import montar_contexto
from apps.ia.services.llm_service import perguntar
from apps.ia.services.enturmacao_service import gerar_propostas_enturmacao, diagnosticar_enturmacao

print("=" * 65)
print("TESTE EXPERIMENTAL TCC — CATEGORIA C3: PEDIDO DE RECOMENDAÇÃO (MOTOR 1)")
print("=" * 65)

# 1. Executa diagnóstico e propostas
propostas = gerar_propostas_enturmacao(ano=2026, persistir=True)
print(f"[Motor 1] {len(propostas)} proposta(s) formal(is) de decisão registrada(s) no banco.")

# 2. Monta o contexto analítico de Enturmação
contexto = montar_contexto(tipo="ENTURMACAO")
print("\n" + "-" * 50)
print("CONTEXTO INJETADO (DADOS DO MOTOR 1):")
print("-" * 50)
print(contexto)

# 3. Executa a inferência com a pergunta de recomendação (Categoria C3 da Tabela 13)
pergunta = (
    "Como gestor escolar, analisando as turmas de 2026, o que você diagnostica "
    "sobre o balanceamento entre as turmas do 1º Ano e o que recomenda para o "
    "equilíbrio da quantidade de alunos e a inclusão pedagógica de PCDs?"
)

print("\n" + "=" * 65)
print("ENVIANDO PERGUNTA C3 PARA A LLM (LLAMA 3.1 8B)...")
print("=" * 65)
print("Pergunta:", pergunta)

resultado = perguntar(pergunta=pergunta, contexto=contexto)

print("\n" + "=" * 65)
print("RESULTADO DA INFERÊNCIA CONSULTIVA (MOTOR 1 — C3):")
print("=" * 65)
print(f"Sucesso: {resultado['sucesso']}")
print(f"Latência de Inferência: {resultado['latencia_segundos']} s")
print(f"Modelo: {resultado['modelo']}")
print(f"Aviso Ético: {resultado['aviso']}")
print("\nRESPOSTA DO ASSISTENTE:\n")
print(resultado['resposta'])
