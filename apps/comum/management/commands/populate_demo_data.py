import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

from apps.usuarios.models.perfis import Aluno, Professor, Gestor
from apps.academico.models.academico import Turma, Disciplina, GradeHorario, AtividadeProfessor
from apps.academico.models.desempenho import Nota, Frequencia
from apps.infraestrutura.models.patrimonio import UnidadeEscolar, CategoriaBem, ItemPatrimonio, ItemEstoque, SaldoEstoque
from apps.comunicacao.models.comunicado import Comunicado
from apps.saude.models.ficha_medica import FichaMedica, RegistroVacina
from apps.biblioteca.models.biblioteca import Livro, Emprestimo

class Command(BaseCommand):
    help = 'Popula o banco de dados com informações realistas para demonstração.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Limpa o banco antes de popular')

    def handle(self, *args, **options):
        # 1. Limpeza Opcional
        if options['clear']:
            self.stdout.write("Limpando banco de dados...")
            # Deletar em ordem inversa de dependência
            Emprestimo.objects.all().delete()
            Livro.objects.all().delete()
            RegistroVacina.objects.all().delete()
            FichaMedica.objects.all().delete()
            Nota.objects.all().delete()
            Frequencia.objects.all().delete()
            AtividadeProfessor.objects.all().delete()
            Disciplina.objects.all().delete()
            Aluno.objects.all().delete()
            Professor.objects.all().delete()
            Gestor.objects.all().delete()
            Turma.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("Banco limpo!"))

        with transaction.atomic():
            self.stdout.write("Iniciando população de dados...")

            # --- INFRAESTRUTURA ---
            unidade, _ = UnidadeEscolar.objects.get_or_create(nome="Campus Central", eh_sede=True)
            cat_moveis, _ = CategoriaBem.objects.get_or_create(nome="Mobiliário", descricao="Mesas, cadeiras, armários")
            cat_ti, _ = CategoriaBem.objects.get_or_create(nome="Tecnologia", descricao="Computadores, periféricos")

            ItemPatrimonio.objects.get_or_create(tombamento="PAT-2024-001", nome="MacBook Pro M3 - Lab 1", categoria=cat_ti, unidade=unidade, estado_conservacao="NOVO")
            ItemPatrimonio.objects.get_or_create(tombamento="PAT-2024-002", nome="Projetor Epson 4K", categoria=cat_ti, unidade=unidade, estado_conservacao="BOM")
            ItemPatrimonio.objects.get_or_create(tombamento="PAT-2024-003", nome="Mesa Diretor - Madeira Maciça", categoria=cat_moveis, unidade=unidade, estado_conservacao="BOM")

            item_papel, _ = ItemEstoque.objects.get_or_create(nome="Resma Papel A4", unidade_medida="Pacote", estoque_minimo=10)
            SaldoEstoque.objects.get_or_create(item=item_papel, unidade=unidade, quantidade=50)

            # --- COMUNICAÇÃO ---
            Comunicado.objects.create(
                titulo="Boas-vindas ao Ano Letivo 2024", 
                conteudo="O Colégio SIGE Premium deseja a todos um excelente ano. Estamos ansiosos para vê-los!", 
                publico_alvo="GLOBAL",
                importancia="NORMAL"
            )
            Comunicado.objects.create(
                titulo="Reunião de Pais e Mestres", 
                conteudo="Convocação para reunião no auditório. Data: 20/04 às 19h.", 
                publico_alvo="GLOBAL",
                importancia="ALTA"
            )

            # --- BIBLIOTECA ---
            livros_data = [
                ("Dom Casmurro", "Machado de Assis", "9788520926512", 5),
                ("Sapiens", "Yuval Noah Harari", "9788525060419", 3),
                ("O Código Da Vinci", "Dan Brown", "9788575420956", 2),
                ("1984", "George Orwell", "9788535914849", 4),
            ]
            for t, a, i, q in livros_data:
                Livro.objects.get_or_create(titulo=t, autor=a, isbn=i, quantidade_total=q)

            # --- GESTORES ---
            gestores_info = [
                ("diretor", "Dr. Ricardo Oliveira", "ricardo.diretor", "111.111.111-11"),
                ("coordenador", "Dra. Ana Paula", "ana.coord", "222.222.222-22"),
            ]
            for cargo, nome, username, cpf in gestores_info:
                u, created = User.objects.get_or_create(username=username, email=f"{username}@sige.com")
                if created: u.set_password("sige123"); u.save()
                Gestor.objects.get_or_create(user=u, nome_completo=nome, cpf=cpf, cargo=cargo)

            # --- PROFESSORES ---
            profs_info = [
                ("Prof. Emerson Silva", "emerson.prof", "333.333.333-33"),
                ("Dra. Beatriz Santos", "beatriz.prof", "444.444.444-44"),
                ("Me. Carlos Souza", "carlos.prof", "555.555.555-55"),
            ]
            professores = []
            for nome, username, cpf in profs_info:
                u, created = User.objects.get_or_create(username=username, email=f"{username}@sige.com")
                if created: u.set_password("sige123"); u.save()
                p, _ = Professor.objects.get_or_create(user=u, nome_completo=nome, cpf=cpf)
                professores.append(p)

            # --- TURMAS E DISCIPLINAS ---
            turmas_data = [
                ("9º Ano A", "manha", 2026),
                ("1º Ensino Médio", "manha", 2026),
                ("2º Ensino Médio", "tarde", 2026),
                ("3º Ensino Médio", "tarde", 2026),
            ]
            disciplinas_nomes = ["Matemática", "Português", "História", "Ciências", "Educação Física"]
            
            for t_nome, t_turno, t_ano in turmas_data:
                turma, _ = Turma.objects.get_or_create(nome=t_nome, turno=t_turno, ano=t_ano)
                
                # Alunos da Turma
                for i in range(1, 11):
                    al_username = f"aluno.{turma.id}.{i}"
                    al_nome = f"Aluno {i} da {turma.nome}"
                    al_cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
                    u, created = User.objects.get_or_create(username=al_username, email=f"{al_username}@estudante.com")
                    if created: u.set_password("sige123"); u.save()
                    aluno, _ = Aluno.objects.get_or_create(user=u, nome_completo=al_nome, turma=turma, cpf=al_cpf)
                    
                    # Ficha de Saúde para metade dos alunos
                    if i % 2 == 0:
                        ficha, _ = FichaMedica.objects.get_or_create(aluno=aluno, tipo_sanguineo="O+", alergias="Lactose" if i % 4 == 0 else "")
                        RegistroVacina.objects.create(ficha=ficha, nome_vacina="Gripe", data_dose=timezone.now().date() - timedelta(days=60))

                # Disciplinas para a Turma
                for d_nome in disciplinas_nomes:
                    prof = random.choice(professores)
                    disc, _ = Disciplina.objects.get_or_create(nome=d_nome, turma=turma, professor=prof)
                    
                    # Notas para cada aluno na disciplina
                    for aluno in Aluno.objects.filter(turma=turma):
                        Nota.objects.get_or_create(
                            aluno=aluno, disciplina=disc,
                            nota1=Decimal(random.randint(6, 10)),
                            nota2=Decimal(random.randint(5, 9))
                        )
                        # Frequência (últimos 10 dias)
                        for d in range(10):
                            data_freq = timezone.now().date() - timedelta(days=d)
                            if data_freq.weekday() < 5: # Apenas dias de semana
                                Frequencia.objects.get_or_create(aluno=aluno, disciplina=disc, data=data_freq, presente=random.choice([True, True, True, False]))

            self.stdout.write(self.style.SUCCESS(f"População finalizada!"))
