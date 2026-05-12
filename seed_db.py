print("DEBUG: Script seed_db.py carregado com sucesso.")
import os
import django
import random
import time
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction, connection

# Importação de models
from apps.usuarios.models.perfis import Gestor, Professor, Aluno, Responsavel
from apps.biblioteca.models.biblioteca import Livro, Emprestimo
from apps.saude.models.ficha_medica import FichaMedica, RegistroVacina
from apps.financeiro.models import Fatura, CategoriaFinanceira, CentroCusto, Lancamento, Pagamento
from apps.academico.models.academico import Turma, Disciplina, PlanejamentoAula, MaterialDidatico, GradeHorario
from apps.academico.models.desempenho import Frequencia, Nota
from apps.comunicacao.models.comunicado import Comunicado
from apps.infraestrutura.models.patrimonio import UnidadeEscolar, CategoriaBem, ItemPatrimonio

User = get_user_model()

# Dicionários de nomes para realismo
NOMES_M = ["Joao", "Jose", "Carlos", "Paulo", "Lucas", "Marcos", "Gabriel", "Diego", "Felipe", "Thiago"]
NOMES_F = ["Maria", "Ana", "Juliana", "Beatriz", "Fernanda", "Patricia", "Camila", "Leticia", "Vanessa", "Yasmin"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Ferreira", "Rocha", "Costa", "Pereira", "Ribeiro"]

def gerar_nome(genero=None):
    primeiro = random.choice(NOMES_M) if genero == 'M' else random.choice(NOMES_F) if genero == 'F' else random.choice(NOMES_M + NOMES_F)
    return f"{primeiro} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"

def limpar_banco():
    db_info = connection.settings_dict
    print(f"DEBUG: Conectado ao banco: {db_info.get('NAME')} em {db_info.get('HOST') or 'Localhost'}")
    print("Limpando banco de dados...")
    models = [
        Pagamento, Lancamento, Fatura, RegistroVacina, FichaMedica, 
        Emprestimo, Livro, Frequencia, Nota, PlanejamentoAula, 
        MaterialDidatico, GradeHorario, Disciplina, Aluno, 
        Responsavel, Professor, Gestor, Turma, Comunicado
    ]
    for m in models:
        count = m.objects.count()
        print(f"  - Deletando {count} registros de {m._meta.model_name}...")
        m.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    print("Banco limpo.\n")

def seed():
    print("Iniciando Populacao SIGE Premium...")
    start_time = time.time()

    # 1. Infra e Finanças
    escola = UnidadeEscolar.objects.create(nome="SIGE Management Institute", eh_sede=True)
    cat_mensal = CategoriaFinanceira.objects.create(nome="Mensalidade", tipo="RECEITA")
    cc_adm = CentroCusto.objects.create(nome="Administrativo")

    # 2. Professores e Responsáveis
    professores = []
    for i in range(5):
        u, _ = User.objects.get_or_create(username=f"prof_{i}")
        u.set_password("1")
        u.save()
        p = Professor.objects.create(user=u, nome_completo=f"Prof. {gerar_nome()}", cpf=f"00{i:03d}.000.000-00"[:14])
        professores.append(p)

    responsaveis = []
    for i in range(10):
        u, _ = User.objects.get_or_create(username=f"resp_{i}")
        u.set_password("1")
        u.save()
        r = Responsavel.objects.create(
            user=u, 
            nome_completo=gerar_nome(), 
            cpf=f"11{i:03d}.111.111-11"[:14],
            controle_parental_ativo=True if i < 7 else False
        )
        responsaveis.append(r)

    # 3. Turmas, Alunos e Acadêmico
    anos = [2026]
    turmas_base = ["1º Ano A", "2º Ano B", "3º Ano C"]
    materias = ["Matemática", "Português", "História", "Física"]
    
    aluno_idx = 1
    for ano in anos:
        for t_nome in turmas_base:
            turma = Turma.objects.create(nome=t_nome, ano=ano, turno='manha')
            
            # Disciplinas
            discs = []
            for m_nome in materias:
                d = Disciplina.objects.create(nome=m_nome, turma=turma, professor=random.choice(professores))
                discs.append(d)

            # Alunos
            for i in range(1, 11):
                nome_aluno = gerar_nome()
                u_aluno, _ = User.objects.get_or_create(username=f"temp_{aluno_idx}")
                u_aluno.set_password("1")
                u_aluno.save()
                
                # O Aluno.save() gerará a matrícula YYYYTTTUUUU
                aluno = Aluno.objects.create(
                    user=u_aluno, 
                    nome_completo=nome_aluno, 
                    turma=turma, 
                    cpf=f"22{aluno_idx}.222.222-22"
                )
                
                # Vinculo Parental
                pai = random.choice(responsaveis)
                pai.alunos.add(aluno)

                # Notas e Frequência
                for d in discs:
                    Nota.objects.create(
                        aluno=aluno, disciplina=d, 
                        nota1=Decimal(random.randint(5, 10)),
                        nota2=Decimal(random.randint(6, 10))
                    )
                    for dia in range(5):
                        Frequencia.objects.create(
                            aluno=aluno, disciplina=d, 
                            data=date(2026, 3, dia+1), 
                            presente=random.choice([True, True, True, False])
                        )
                
                aluno_idx += 1

    # 4. Comunicados
    Comunicado.objects.create(
        titulo="Bem-vindo ao Novo SIGE",
        conteudo="Aproveite as novas funcionalidades de Controle Parental e Login via Matrícula.",
        publico_alvo="GLOBAL", importancia="ALTA"
    )

    print(f"Finalizado em {round(time.time() - start_time, 2)}s")
    print(f"Resumo: {Aluno.objects.count()} Alunos, {Responsavel.objects.count()} Responsaveis.")

if __name__ == "__main__":
    limpar_banco()
    seed()