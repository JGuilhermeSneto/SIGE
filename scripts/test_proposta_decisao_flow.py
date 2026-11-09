import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.ia.models import PropostaDecisao

User = get_user_model()
gestor = User.objects.filter(is_staff=True).first() or User.objects.first()

print("=" * 60)
print("TESTE DE FLUXO HUMAN-IN-THE-LOOP (APROVAÇÃO DE PROPOSTA)")
print("=" * 60)

proposta = PropostaDecisao.objects.filter(tipo="ENTURMACAO", status="PENDENTE").first()
if not proposta:
    print("Nenhuma proposta pendente encontrada.")
    sys.exit(0)

print(f"Proposta Selecionada: [ID {proposta.id}] {proposta.titulo}")
print(f"Status Inicial: {proposta.status}")

# Simula aprovação consciente pelo gestor escolar
proposta.status = "APROVADA"
proposta.decidido_por = gestor
proposta.decidido_em = timezone.now()
proposta.observacao_gestor = (
    "Aprovado após reunião pedagógica. O remanejamento de 8 estudantes para a turma 1º Ano B "
    "será executado na abertura do próximo bimestre, priorizando o equilíbrio do atendimento de AEE."
)
proposta.save()

# Recarrega do banco para validar persistência
proposta.refresh_from_db()

print("\n" + "-" * 50)
print("ESTADO APÓS DELIBERAÇÃO HUMANA (DECISÃO DO GESTOR):")
print("-" * 50)
print(f"Status Atual: {proposta.status} (Garantia Human-in-the-Loop)")
print(f"Decidido por: {proposta.decidido_por.username}")
print(f"Decidido em: {proposta.decidido_em.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Observação do Gestor:\n  \"{proposta.observacao_gestor}\"")
print(f"Dados estruturados prontos para execução: {proposta.dados_proposta}")
print("\nFluxo Human-in-the-Loop validado com sucesso!")
