import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.academico.models.academico import Turma, Disciplina
from apps.usuarios.models.perfis import Aluno, Professor

User = get_user_model()

# Busca turma 77 (1º Ano B 2026) como referência
turma_b = Turma.objects.get(id=77)
instituicao = turma_b.instituicao

# 1. Cria ou recupera a turma paralela: 1º Ano A (2026)
turma_a, created = Turma.objects.get_or_create(
    nome="1o Ano A (2026)",
    ano=2026,
    turno="manha",
    instituicao=instituicao,
)
print(f"Turma '1o Ano A (2026)' {'criada' if created else 'já existente'} (ID {turma_a.id})")

# 2. Assegura que o 1º Ano A tenha 29 alunos
alunos_a_atuais = turma_a.alunos.count()
faltam_a = 29 - alunos_a_atuais

if faltam_a > 0:
    print(f"Criando {faltam_a} alunos para compor o 1º Ano A (2026)...")
    for i in range(faltam_a):
        username = f"aluno_1a_{i+1:03d}"
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"first_name": f"Estudante 1A {i+1}", "email": f"{username}@escola.com"}
        )
        cpf_fake = f"111222{i+1:03d}00"
        Aluno.objects.get_or_create(
            user=user,
            defaults={
                "instituicao": instituicao,
                "nome_completo": f"Estudante 1º Ano A {i+1}",
                "cpf": cpf_fake,
                "data_nascimento": "2010-03-15",
                "turma": turma_a,
                "status_matricula": "ATIVO",
                "matricula": f"2026{turma_a.id:03d}{user.id:04d}",
            }
        )

# 3. Configura 3 alunos com necessidades especiais no 1º Ano A
alunos_a = list(turma_a.alunos.all()[:3])
for idx, al in enumerate(alunos_a):
    al.possui_necessidade_especial = True
    al.descricao_necessidade = f"Necessidade de Apoio Pedagógico e Acessibilidade (PCD/AEE {idx+1})"
    al.save(update_fields=["possui_necessidade_especial", "descricao_necessidade"])

# 4. Assegura disciplinas para a nova turma espelhando o 1º Ano B
prof_padrao = Professor.objects.first()
if turma_a.disciplinas.count() == 0 and prof_padrao:
    for d_nome in ["Português", "Matemática", "História", "Geografia", "Ciências", "Inglês", "Arte", "Ed. Física"]:
        Disciplina.objects.get_or_create(
            nome=d_nome,
            turma=turma_a,
            defaults={"professor": prof_padrao}
        )

print("\n=== CENÁRIO EXPERIMENTAL 2026 CONFIGURADO ===")
print(f"1º Ano A (2026): {turma_a.alunos.count()} alunos (PCDs: {turma_a.alunos.filter(possui_necessidade_especial=True).count()})")
print(f"1º Ano B (2026): {turma_b.alunos.count()} alunos (PCDs: {turma_b.alunos.filter(possui_necessidade_especial=True).count()})")
t78 = Turma.objects.get(id=78)
t79 = Turma.objects.get(id=79)
print(f"2º Ano B (2026): {t78.alunos.count()} alunos")
print(f"3º Ano B (2026): {t79.alunos.count()} alunos (Sublotada)")
