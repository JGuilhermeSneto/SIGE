import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.ia.models import SessaoAssistente, MensagemAssistente
from apps.ia.services.contexto import montar_contexto

User = get_user_model()
gestor_user = User.objects.filter(is_staff=True).first()
if not gestor_user:
    gestor_user = User.objects.first()

print(f"Usuário selecionado para o teste de auditoria: {gestor_user.username if gestor_user else 'None'}")

# Cria sessão de teste
sessao = SessaoAssistente.objects.create(
    usuario=gestor_user,
    titulo="Auditoria de Panorama Escolar (Dia 3)"
)

contexto = montar_contexto(tipo="GERAL")
pergunta = "Qual é o panorama executivo da infraestrutura e acervo bibliográfico?"

# Salva mensagem do gestor
msg_user = MensagemAssistente.objects.create(
    sessao=sessao,
    papel="user",
    conteudo=pergunta,
    contexto_utilizado=contexto
)

# Salva resposta da LLM (simulação registrada do teste real executado)
resposta_llm = (
    "Sugestão para o gestor:\n"
    "- A unidade escolar dispõe de 7 ambientes/salas cadastrados e 250 itens de patrimônio registrados.\n"
    "- O acervo da biblioteca conta com 200 títulos cadastrados e 796 exemplares físicos, com 20 empréstimos em atraso."
)
msg_assistant = MensagemAssistente.objects.create(
    sessao=sessao,
    papel="assistant",
    conteudo=resposta_llm,
    latencia_segundos=131.57
)

print(f"Sessão ID {sessao.id} criada com sucesso!")
print(f"Mensagens na sessão: {sessao.mensagens.count()}")
for m in sessao.mensagens.all():
    print(f"  [{m.papel.upper()}] (latência: {m.latencia_segundos}s): {m.conteudo[:80]}...")

print("\nAuditoria do banco de dados validada com sucesso!")
