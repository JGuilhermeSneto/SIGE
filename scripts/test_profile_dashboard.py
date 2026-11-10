import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.ia.services import (
    verificar_disponibilidade_llm,
    diagnosticar_enturmacao,
    diagnosticar_infraestrutura,
    diagnosticar_financeiro,
)
from apps.ia.models import PropostaDecisao

print("1. Testando verificar_disponibilidade_llm...", flush=True)
t0 = time.time()
llm = verificar_disponibilidade_llm()
print(f"   LLM: {llm} ({time.time()-t0:.2f}s)", flush=True)

print("2. Testando diagnosticar_enturmacao...", flush=True)
t0 = time.time()
m1 = diagnosticar_enturmacao(ano=2026)
print(f"   M1 turmas avaliadas: {m1['total_turmas_avaliadas']} ({time.time()-t0:.2f}s)", flush=True)

print("3. Testando diagnosticar_infraestrutura...", flush=True)
t0 = time.time()
m2 = diagnosticar_infraestrutura()
print(f"   M2 ambientes: {m2['total_ambientes']} ({time.time()-t0:.2f}s)", flush=True)

print("4. Testando diagnosticar_financeiro...", flush=True)
t0 = time.time()
m3 = diagnosticar_financeiro(ano=2026)
print(f"   M3 faturado: {m3['total_faturado_acumulado']} ({time.time()-t0:.2f}s)", flush=True)

print("5. Testando PropostaDecisao query...", flush=True)
t0 = time.time()
p = list(PropostaDecisao.objects.all().order_by("-criado_em"))
print(f"   Propostas: {len(p)} ({time.time()-t0:.2f}s)", flush=True)

print("6. Testando render template isolado...", flush=True)
from django.template.loader import render_to_string
t0 = time.time()
html = render_to_string("ia/dashboard.html", {
    "llm_status": llm,
    "diag_m1": m1,
    "diag_m2": m2,
    "diag_m3": m3,
    "propostas": p,
    "total_pendentes": 5,
    "total_aprovadas": 1,
    "total_rejeitadas": 0,
})
print(f"   Template renderizado com sucesso: {len(html)} caracteres em {time.time()-t0:.2f}s!", flush=True)
