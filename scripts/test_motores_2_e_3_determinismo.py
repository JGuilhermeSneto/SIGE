"""
Script de validação determinística dos Motores 2 (Infraestrutura) e 3 (Financeiro).
Testa diagnósticos, geração de propostas Human-in-the-Loop e contexto RAG.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.ia.services import (
    diagnosticar_infraestrutura,
    gerar_propostas_infraestrutura,
    montar_contexto_motor_infraestrutura,
    diagnosticar_financeiro,
    gerar_propostas_financeiro,
    montar_contexto_motor_financeiro,
    detectar_tipo_pergunta,
    montar_contexto,
)
from apps.ia.models import PropostaDecisao

print("=" * 70)
print("1. TESTANDO MOTOR 2: INFRAESTRUTURA E CONSERVAÇÃO PATRIMONIAL")
print("=" * 70)

diag_infra = diagnosticar_infraestrutura()
print(f"Total de ambientes: {diag_infra['total_ambientes']}")
print(f"Total patrimônio: {diag_infra['total_patrimonio']}")
print(f"Itens operacionais: {diag_infra['itens_operacionais']} | Avariados: {diag_infra['itens_avariados']}")
print(f"Índice global de avaria: {diag_infra['indice_avaria_global_pct']}%")
print(f"Ambientes críticos por avaria: {[a['nome'] for a in diag_infra['ambientes_criticos_avaria']]}")
print(f"Ambientes ociosos/sem mobília: {[a['nome'] for a in diag_infra['ambientes_ociosos']]}")
print("Alertas gerados:", len(diag_infra["alertas"]))

props_infra = gerar_propostas_infraestrutura(persistir=True)
print(f"Propostas de infraestrutura persistidas: {len(props_infra)}")
for p in props_infra:
    print(f"  • [{p.status}] {p.titulo} (ID {p.id})")

print("\n--- CONTEXTO RAG MOTOR 2 ---")
ctx_infra = montar_contexto_motor_infraestrutura()
print(ctx_infra)

print("\n" + "=" * 70)
print("2. TESTANDO MOTOR 3: SUSTENTABILIDADE FINANCEIRA E BREAK-EVEN")
print("=" * 70)

diag_fin = diagnosticar_financeiro(ano=2026)
print(f"Ano: {diag_fin['ano_referencia']}")
print(f"Total turmas analisadas: {diag_fin['total_turmas']}")
print(f"Total alunos ativos: {diag_fin['total_alunos_ativos']}")
print(f"Receita projetada mensal: R$ {diag_fin['receita_mensal_projetada']:,.2f}")
print(f"Custo projetado mensal: R$ {diag_fin['custo_mensal_projetado']:,.2f}")
print(f"Saldo operacional mensal: R$ {diag_fin['saldo_mensal_operacional']:,.2f}")
print(f"Taxa inadimplência global: {diag_fin['taxa_inadimplencia_global_pct']}%")
print("Turmas deficitárias:", [t["turma_nome"] for t in diag_fin["turmas_deficitarias"]])

props_fin = gerar_propostas_financeiro(ano=2026, persistir=True)
print(f"Propostas financeiras persistidas: {len(props_fin)}")
for p in props_fin:
    print(f"  • [{p.status}] {p.titulo} (ID {p.id})")

print("\n--- CONTEXTO RAG MOTOR 3 ---")
ctx_fin = montar_contexto_motor_financeiro(ano=2026)
print(ctx_fin)

print("\n" + "=" * 70)
print("3. TESTANDO CLASSIFICADOR DETERMINÍSTICO DE INTENÇÃO")
print("=" * 70)
perguntas_teste = [
    ("Como está o equilíbrio de vagas e alunos PCD nas turmas do 1º ano?", "ENTURMACAO"),
    ("Quais salas possuem avarias no mobiliário e precisam de manutenção?", "INFRAESTRUTURA"),
    ("Qual a receita estimada e o risco de déficit das turmas de 2026?", "FINANCEIRO"),
    ("Quantos livros temos no acervo da biblioteca?", "BIBLIOTECA"),
    ("Me dê um resumo geral da escola.", "GERAL"),
]

acertos = 0
for perg, esperado in perguntas_teste:
    classif = detectar_tipo_pergunta(perg)
    correto = (classif == esperado)
    if correto:
        acertos += 1
    print(f"Pergunta: '{perg}'")
    print(f"  -> Classificado: {classif} | Esperado: {esperado} | OK: {correto}")

print(f"\nAcurácia do Classificador: {acertos}/{len(perguntas_teste)} ({acertos/len(perguntas_teste)*100:.0f}%)")

print("\nTotal de PropostasDecisao no banco:", PropostaDecisao.objects.count())
print("Propostas pendentes:", PropostaDecisao.objects.filter(status="PENDENTE").count())
print("=" * 70)
print("TESTE DETERMINÍSTICO CONCLUÍDO COM SUCESSO!")
print("=" * 70)

