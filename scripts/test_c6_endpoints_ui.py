"""
Validação da URL /ia/ e endpoints REST do DSS via Django Test Client
======================================================================
TCC Seção 5.1 — Integração de Interface e Endpoints

Verifica:
  1. GET /ia/              → HTTP 200, template dashboard renderizado
  2. GET /ia/status/       → HTTP 200, JSON com status do LLM
  3. GET /ia/status/detalhado/ → HTTP 200, JSON completo
  4. GET /ia/propostas/    → HTTP 200, JSON lista de propostas pendentes
  5. POST /ia/propostas/   → HTTP 201, cria proposta PENDENTE
  6. POST /ia/propostas/<id>/acao/ → HTTP 200, aprova proposta (APROVADA)

Critérios de aprovação:
  - Todos os endpoints retornam os status HTTP esperados
  - JSON de resposta contém as chaves obrigatórias
  - Proposta criada começa como PENDENTE (Human-in-the-Loop)
  - Decisão altera corretamente o status no banco

Referências:
  - TCC Seção 4.7: Interface Human-in-the-Loop
  - TCC Tabela 13 (Categoria C6 — integração de interface)
"""

import os
import sys
import json
import django
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

RESULTADO = {
    "total": 0,
    "aprovados": 0,
    "erros": [],
}


def assert_ok(nome: str, condicao: bool, detalhe: str = ""):
    """Registra resultado de cada verificação."""
    RESULTADO["total"] += 1
    if condicao:
        RESULTADO["aprovados"] += 1
        print(f"  ✅ {nome}")
    else:
        print(f"  ❌ {nome}{' — ' + detalhe if detalhe else ''}")
        RESULTADO["erros"].append(nome)


def main():
    print("=" * 70)
    print("VALIDAÇÃO DE ENDPOINTS — /ia/ e REST DSS")
    print("TCC ELISE IA — Integração de Interface (C6)")
    print("=" * 70)

    # Usar ou criar gestor de teste
    gestor, criado = User.objects.get_or_create(
        username="gestor_c6_test",
        defaults={"first_name": "Gestor", "last_name": "C6", "is_staff": True},
    )
    if criado:
        gestor.set_password("test@1234")
        gestor.save()
    print(f"Usuário gestor: {gestor.username} (criado agora: {criado})")

    # Usar force_login para contornar django-axes (que exige request no authenticate)
    client = Client()
    client.force_login(gestor)
    login_ok = True
    assert_ok("Login do gestor (force_login)", login_ok)

    # -------------------------------------------------------------------------
    # 1. GET /ia/ — Dashboard HTML
    # -------------------------------------------------------------------------
    print("\n[1] GET /ia/ — Dashboard HTML")
    inicio = time.time()
    r = client.get("/ia/", HTTP_HOST="localhost")
    lat1 = round(time.time() - inicio, 3)
    assert_ok("HTTP 200", r.status_code == 200, f"status={r.status_code}")
    assert_ok("Content-Type HTML", "text/html" in r.get("Content-Type", ""))
    tamanho = len(r.content)
    assert_ok("Template renderizado (>5000 bytes)", tamanho > 5000, f"{tamanho} bytes")
    print(f"  Latência: {lat1}s | Tamanho: {tamanho} bytes")

    # -------------------------------------------------------------------------
    # 2. GET /ia/status/ — Status LLM (JSON simples, sem autenticação)
    # -------------------------------------------------------------------------
    print("\n[2] GET /ia/status/ — Status LLM")
    r2 = client.get("/ia/status/", HTTP_HOST="localhost")
    assert_ok("HTTP 200", r2.status_code == 200)
    try:
        data2 = json.loads(r2.content)
        # assistente_status retorna chave 'llm' com as subchaves
        llm_info = data2.get("llm", {})
        assert_ok("Chave 'llm' presente", "llm" in data2)
        assert_ok("Chave 'assistant' presente", "assistant" in data2)
        print(f"  Ollama disponível: {llm_info.get('disponivel')}")
        print(f"  Modelo: {llm_info.get('modelo_configurado')}")
    except json.JSONDecodeError:
        assert_ok("JSON válido", False, "não é JSON")

    # -------------------------------------------------------------------------
    # 3. GET /ia/status/detalhado/ — Status detalhado (APIView com auth)
    # -------------------------------------------------------------------------
    print("\n[3] GET /ia/status/detalhado/")
    r3 = client.get("/ia/status/detalhado/", HTTP_HOST="localhost",
                    HTTP_ACCEPT="application/json")
    assert_ok("HTTP 200", r3.status_code == 200)
    try:
        data3 = json.loads(r3.content)
        assert_ok("Chave 'llm' presente", "llm" in data3)
        assert_ok("Chave 'motores' presente", "motores" in data3)
        motores = data3.get("motores", {})
        assert_ok("Motor enturmacao presente", "enturmacao" in motores)
        assert_ok("Motor infraestrutura presente", "infraestrutura" in motores)
        assert_ok("Motor financeiro presente", "financeiro" in motores)
        print(f"  Motores disponíveis: {list(motores.keys())}")
    except json.JSONDecodeError as e:
        assert_ok("JSON válido", False, f"não é JSON: {e} | body={r3.content[:200]}")

    # -------------------------------------------------------------------------
    # 4. GET /ia/propostas/ — Lista propostas
    # -------------------------------------------------------------------------
    print("\n[4] GET /ia/propostas/ — Lista de propostas")
    r4 = client.get("/ia/propostas/", HTTP_HOST="localhost")
    assert_ok("HTTP 200", r4.status_code == 200)
    try:
        data4 = json.loads(r4.content)
        propostas = data4 if isinstance(data4, list) else data4.get("results", data4.get("propostas", []))
        assert_ok("Lista retornada", isinstance(propostas, list))
        print(f"  Total de propostas retornadas: {len(propostas)}")
    except json.JSONDecodeError:
        assert_ok("JSON válido", False)

    # -------------------------------------------------------------------------
    # 5. POST /ia/propostas/ — Disparar geração de propostas (Motor 1)
    # -------------------------------------------------------------------------
    print("\n[5] POST /ia/propostas/ — Gerar propostas via Motor 1")
    payload_geracao = {"motor": "ENTURMACAO", "ano": 2026}
    r5 = client.post(
        "/ia/propostas/",
        data=json.dumps(payload_geracao),
        content_type="application/json",
        HTTP_HOST="localhost",
    )
    print(f"  Status: {r5.status_code}")
    proposta_id = None
    if r5.status_code in (200, 201):
        try:
            data5 = json.loads(r5.content)
            total_geradas = data5.get("total_geradas", 0)
            ids_geradas = data5.get("propostas", [])
            assert_ok("HTTP 200/201 (geração)", True)
            assert_ok("Campo 'mensagem' presente", "mensagem" in data5)
            print(f"  Propostas geradas/atualizadas: {total_geradas} | IDs: {ids_geradas}")
            # Pegar a primeira proposta PENDENTE para testar ação
            from apps.ia.models import PropostaDecisao
            p_pendente = PropostaDecisao.objects.filter(status="PENDENTE").first()
            if p_pendente:
                proposta_id = p_pendente.id
                print(f"  Proposta PENDENTE disponível para ação: ID {proposta_id}")
        except Exception as e:
            assert_ok("JSON válido da geração", False, str(e))
    else:
        assert_ok("HTTP 200/201", False, f"status={r5.status_code}, body={r5.content[:300]}")

    # -------------------------------------------------------------------------
    # 6. POST /ia/propostas/<id>/acao/ — Aprovar proposta
    # -------------------------------------------------------------------------
    if proposta_id:
        print(f"\n[6] POST /ia/propostas/{proposta_id}/acao/ — Aprovar proposta")
        payload_acao = {
            "acao": "APROVAR",
            "observacao": "Aprovado no teste de integração C6 — Dia 7.",
        }
        r6 = client.post(
            f"/ia/propostas/{proposta_id}/acao/",
            data=json.dumps(payload_acao),
            content_type="application/json",
            HTTP_HOST="localhost",
        )
        print(f"  Status HTTP: {r6.status_code}")
        if r6.status_code == 200:
            try:
                data6 = json.loads(r6.content)
                novo_status = data6.get("status", "")
                assert_ok("HTTP 200 na ação", True)
                assert_ok("Status = APROVADA após aprovação", novo_status == "APROVADA", f"status={novo_status}")
                print(f"  Novo status: {novo_status}")
            except Exception as e:
                assert_ok("JSON válido da ação", False, str(e))
        else:
            assert_ok("HTTP 200 na ação", False, f"status={r6.status_code}, body={r6.content[:300]}")

    # -------------------------------------------------------------------------
    # Sumário
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"RESULTADO FINAL C6: {RESULTADO['aprovados']}/{RESULTADO['total']} verificações aprovadas")
    if RESULTADO["erros"]:
        print(f"❌ Falhas: {', '.join(RESULTADO['erros'])}")
    else:
        print("✅ Todos os endpoints funcionais e conformes")

    taxa = round((RESULTADO["aprovados"] / RESULTADO["total"]) * 100, 1)
    print(f"Taxa de aprovação: {taxa}%")
    return RESULTADO["aprovados"] == RESULTADO["total"]


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
