import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.usuarios.models import Aluno
from django.contrib.auth.models import User

# Verifica alunos de teste existentes
matriculas = ['202677588', '202677589', '202677590', '202677591']
print("=== STATUS ATUAL ===")
for m in matriculas:
    existe = Aluno.objects.filter(matricula=m).exists()
    print(f"  Matricula {m}: {'EXISTE' if existe else 'NAO EXISTE'}")

# Pega dados do aluno 202677590 como referencia
try:
    ref = Aluno.objects.select_related('user').get(matricula='202677590')
    turma_id = ref.turma_id
    inst_id = ref.instituicao_id
    print(f"\nReferencia (202677590):")
    print(f"  turma_id={turma_id}")
    print(f"  instituicao_id={inst_id}")
    print(f"  senha ok? {ref.user.check_password('SenhaSIGE2026')}")

    SENHA = 'SenhaSIGE2026'
    alunos_teste = [
        ('202677588', 'Junior', 'Teste', 'junior.teste@sige.local'),
        ('202677589', 'Israel', 'Teste', 'israel.teste@sige.local'),
        ('202677591', 'Pedro',  'Teste', 'pedro.teste@sige.local'),
    ]

    print("\n=== CRIANDO ALUNOS FALTANTES ===")
    for matricula, first, last, email in alunos_teste:
        if Aluno.objects.filter(matricula=matricula).exists():
            print(f"  {first} {last} ({matricula}) ja existe.")
            aluno = Aluno.objects.get(matricula=matricula)
            aluno.user.set_password(SENHA)
            aluno.user.save()
            print(f"    -> Senha redefinida para: {SENHA}")
            continue

        # Cria o User
        if User.objects.filter(username=matricula).exists():
            u = User.objects.get(username=matricula)
        else:
            u = User.objects.create_user(
                username=matricula,
                email=email,
                password=SENHA,
                first_name=first,
                last_name=last,
            )
        u.is_active = True
        u.save()

        # Cria o Aluno
        Aluno.objects.create(
            user=u,
            matricula=matricula,
            turma_id=turma_id,
            instituicao_id=inst_id,
        )
        print(f"  CRIADO: {first} {last} | username={matricula} | senha={SENHA}")

    # Atualiza nome do 202677590 (Guilherme Teste)
    ref.user.first_name = 'Guilherme'
    ref.user.last_name = 'Teste'
    ref.user.email = 'guilherme.teste@sige.local'
    ref.user.save()
    ref.user.set_password(SENHA)
    ref.user.save()
    print(f"\n  ATUALIZADO: Guilherme Teste (202677590) - senha redefinida")

    print("\n=== VERIFICACAO FINAL ===")
    for m in matriculas:
        a = Aluno.objects.select_related('user').get(matricula=m)
        u = a.user
        ok = u.check_password(SENHA)
        print(f"  {u.first_name} {u.last_name} | matricula={m} | username={u.username} | active={u.is_active} | senha_ok={ok}")

except Aluno.DoesNotExist:
    print("ERRO: Aluno de referencia 202677590 nao encontrado.")
    sys.exit(1)
