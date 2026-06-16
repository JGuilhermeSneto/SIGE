import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.usuarios.models.perfis import Aluno
from apps.academico.models.academico import Turma

User = get_user_model()

# Config
turma_id = 77  # ajuste se necessário
password = 'SenhaSIGE2026'  # mínimo 10 caracteres
students = [
    ('Junior Silva',),
    ('Israel Souza',),
    ('Guilherme Santos',),
    ('Pedro Alves',),
]

try:
    turma = Turma.objects.get(id=turma_id)
except Exception as e:
    print(f'Turma id={turma_id} não encontrada: {e}')
    exit(1)

created = []
for entry in students:
    nome = entry[0]
    # avoid duplicate by nome
    existing = Aluno.objects.filter(nome_completo__iexact=nome)
    if existing.exists():
        a = existing.first()
        print(f'Aluno já existe: {nome} -> matricula={a.matricula} (user={a.user.username})')
        continue

    # create a temporary user
    temp_username = 'temp_' + nome.split()[0].lower() + str(os.urandom(3).hex())
    user = User.objects.create(username=temp_username, email='', first_name=nome.split()[0], last_name=' '.join(nome.split()[1:]))
    user.set_password(password)
    user.save()

    aluno = Aluno(user=user, nome_completo=nome, turma=turma)
    aluno.save()  # this will generate matricula and sync username

    created.append({'nome': nome, 'matricula': aluno.matricula, 'username': user.username, 'password': password})
    print(f'Criado: {nome} -> matricula={aluno.matricula} username={user.username}')

print('\nResumo:')
for c in created:
    print(c)
