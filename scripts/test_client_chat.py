import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

print("Testando POST /ia/chat/ com Django Client...", flush=True)

User = get_user_model()
user = User.objects.filter(is_superuser=True).first() or User.objects.first()

client = Client()
if user:
    client.force_login(user)

# Teste com classificação automática de intenção
payload = {
    "pergunta": "Qual a taxa de ocupação da Sala 101 e ela precisa de reparos?",
    "tipo": "AUTO"
}

print(f"Enviando pergunta: '{payload['pergunta']}'...", flush=True)
response = client.post(
    "/ia/chat/",
    data=json.dumps(payload),
    content_type="application/json",
    HTTP_HOST="localhost"
)

print(f"Status Code do Chat: {response.status_code}", flush=True)
if response.status_code == 200:
    data = response.json()
    print("Sucesso:", data.get("sucesso"), flush=True)
    print("Tipo de Contexto Aplicado:", data.get("tipo_contexto_aplicado"), flush=True)
    print("Latência (s):", data.get("latencia_segundos"), flush=True)
    print("Resposta (primeiros 150 chars):", data.get("resposta")[:150] + "...", flush=True)
    print("TESTE DE CHAT WEB CONCLUÍDO COM SUCESSO!", flush=True)
else:
    print("Falha:", response.content[:300], flush=True)

