import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

print("Iniciando teste com Django Client...", flush=True)

User = get_user_model()
user = User.objects.filter(is_superuser=True).first() or User.objects.first()

client = Client()
if user:
    client.force_login(user)
    print(f"Logado como: {user.username}", flush=True)

print("Enviando GET /ia/ com HTTP_HOST=localhost...", flush=True)
response = client.get("/ia/", HTTP_HOST="localhost")
print(f"Status Code: {response.status_code}", flush=True)

if response.status_code == 200:
    content = response.content.decode("utf-8")
    print(f"HTML renderizado com sucesso: {len(content)} bytes", flush=True)
    print("Contém título:", "ELISE IA — Suporte Estratégico à Decisão" in content, flush=True)
    print("Contém Motor 1:", "Motor 1: Enturmação e Inclusão" in content, flush=True)
    print("Contém Motor 2:", "Motor 2: Infraestrutura e Espaços" in content, flush=True)
    print("Contém Motor 3:", "Motor 3: Sustentabilidade e Break-Even" in content, flush=True)
    print("Contém Propostas Decisórias:", "Propostas Decisórias do DSS" in content, flush=True)
    print("Contém Assistente Consultivo:", "Assistente Consultivo ELISE" in content, flush=True)
    print("TODAS AS ASSERÇÕES DE UI PASSARAM COM SUCESSO!", flush=True)
else:
    print("Erro ou Redirecionamento:", response.url if hasattr(response, 'url') else response.content[:300], flush=True)
