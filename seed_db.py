"""
SIGE - Super Script de População de Banco de Dados (Simulador Massivo 10 Anos)
Padrão: IFRN (Instituto Federal do Rio Grande do Norte)

Executar com:
  python seed_db.py

AVISO: Este script recria o banco de dados do zero.
Usa bulk_create intensivamente para gerar mais de 10 anos de histórico de alunos,
finanças, almoxarifado, diários de classe, empréstimos e muito mais.
Pode demorar vários minutos para terminar.
"""

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
from django.db import transaction

# Importação de absolutamente todos os models do projeto
from apps.usuarios.models.perfis import Gestor, Professor, Aluno
from apps.biblioteca.models.biblioteca import Livro, Emprestimo
from apps.saude.models.ficha_medica import FichaMedica, RegistroVacina, AtestadoMedico
from apps.financeiro.models import Fatura, CategoriaFinanceira, CentroCusto, Lancamento, FolhaPagamento, Pagamento
from apps.academico.models.academico import Turma, Disciplina, PlanejamentoAula, AtividadeProfessor, MaterialDidatico, GradeHorario
from apps.academico.models.desempenho import Frequencia, Nota, NotaAtividade, Notificacao
from apps.calendario.models.calendario import EventoCalendario
from apps.comunicacao.models.comunicado import Comunicado
from apps.infraestrutura.models.patrimonio import (UnidadeEscolar, CategoriaBem, Ambiente, ItemPatrimonio, 
                                                  ManutencaoBem, ItemEstoque, SaldoEstoque, MovimentacaoEstoque)

User = get_user_model()

# ==============================================================================
# DICIONÁRIOS DE DADOS PARA GERAÇÃO
# ==============================================================================
PRIMEIROS_NOMES_M = ["Joao", "Jose", "Carlos", "Paulo", "Lucas", "Marcos", "Gabriel", "Diego", "Felipe", "Thiago", "Bruno", "Eduardo", "Rodrigo", "Gustavo", "Leonardo", "Alexandre", "Sergio", "Rafael", "Leandro", "Marcelo", "Daniel", "Igor", "Caio", "Victor", "Arthur", "Samuel", "Matheus", "Pedro", "Davi", "Enzo"]
PRIMEIROS_NOMES_F = ["Maria", "Ana", "Juliana", "Beatriz", "Fernanda", "Patricia", "Camila", "Leticia", "Aline", "Priscila", "Vanessa", "Mariana", "Tatiana", "Carla", "Simone", "Renata", "Cristina", "Sandra", "Monica", "Lucia", "Livia", "Isabela", "Giovanna", "Amanda", "Larissa", "Gabriela", "Lara", "Eduarda", "Vitoria", "Yasmin"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Ferreira", "Rocha", "Costa", "Pereira", "Alves", "Gomes", "Ribeiro", "Carvalho", "Martins", "Lopes", "Barbosa", "Almeida", "Castro", "Nascimento", "Vieira", "Melo", "Dantas", "Cavalcanti", "Bezerra", "Farias", "Guedes", "Xavier", "Brito", "Nunes", "Sales"]

MATERIAS_BASE = ["Matematica", "Lingua Portuguesa", "Fisica", "Quimica", "Biologia", "Historia", "Geografia", "Filosofia", "Sociologia", "Ingles", "Educacao Fisica", "Algoritmos", "Banco de Dados"]
TIPOS_SANGUINEOS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
ALERGIAS = ["Dipirona", "Penicilina", "Amendoim", "Lactose", "Ibuprofeno", "Poeira", "Mofo"]
DOENCAS_COMUNS = ["Asma", "Rinite Alergica", "Enxaqueca", "Gastrite"]

def gerar_nome(genero=None):
    primeiro = random.choice(PRIMEIROS_NOMES_M) if genero == 'M' else random.choice(PRIMEIROS_NOMES_F) if genero == 'F' else random.choice(PRIMEIROS_NOMES_M + PRIMEIROS_NOMES_F)
    return f"{primeiro} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"

def gerar_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def gerar_telefone():
    return f"(84) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def limpar_banco():
    print("Aviso: Apagando dados existentes (Hard Reset)...")
    modelos = [
        MovimentacaoEstoque, SaldoEstoque, ItemEstoque, ManutencaoBem, ItemPatrimonio, Ambiente, CategoriaBem, UnidadeEscolar,
        Pagamento, Lancamento, Fatura, FolhaPagamento, CategoriaFinanceira, CentroCusto,
        RegistroVacina, AtestadoMedico, FichaMedica, Emprestimo, Livro,
        Frequencia, NotaAtividade, Nota, AtividadeProfessor, PlanejamentoAula, MaterialDidatico, GradeHorario, Disciplina, Turma,
        Notificacao, EventoCalendario, Comunicado, Gestor, Professor, Aluno
    ]
    for m in modelos:
        m.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    print("Banco de dados limpo.\n")

@transaction.atomic
def seed_infra_e_financas():
    print("[1/8] Semeando Infraestrutura, Almoxarifado, Patrimonio e Configuracoes Financeiras...")
    
    escola = UnidadeEscolar.objects.create(nome="IFRN - Campus Sede", endereco="Av. Senador Salgado Filho, 1559, Natal-RN", eh_sede=True)
    ambientes = [Ambiente.objects.create(nome=nome, unidade=escola) for nome in ["Sala 101", "Sala 102", "Lab Informatica", "Biblioteca", "Diretoria", "Enfermaria", "Almoxarifado Central"]]

    cat_eletr = CategoriaBem.objects.create(nome="Eletronicos e TI")
    cat_mov = CategoriaBem.objects.create(nome="Mobiliario Escolar")
    
    # Gerando 50 computadores (Patrimonio e Manutencao)
    for i in range(50):
        pat_comp = ItemPatrimonio.objects.create(tombamento=f"TI-{2016+i}-{random.randint(1000,9999)}", nome=f"Computador Dell OptiPlex {i}", categoria=cat_eletr, unidade=escola, ambiente=ambientes[2], data_aquisicao=date(2018, 5, 10), valor_aquisicao=Decimal('3500.00'), estado_conservacao=random.choice(['BOM', 'REGULAR']))
        # Simula uma manutencao em alguns
        if random.random() > 0.8:
            ManutencaoBem.objects.create(item=pat_comp, descricao_problema="Fonte queimada", servico_realizado="Troca de fonte ATX", custo=Decimal('150.00'), executor="TI Interna", data_solicitacao=date(2023, 2, 10), data_realizacao=date(2023, 2, 12))
            
    # Gerando 200 cadeiras
    for i in range(200):
        ItemPatrimonio.objects.create(tombamento=f"MOV-{2016+i}-{random.randint(1000,9999)}", nome=f"Carteira Universitária {i}", categoria=cat_mov, unidade=escola, ambiente=ambientes[0], data_aquisicao=date(2016, 1, 20), valor_aquisicao=Decimal('250.00'), estado_conservacao=random.choice(['BOM', 'REGULAR', 'DANIFICADO']))

    # Estoque (Materiais de Consumo)
    itens_est = []
    for nome, un, min_e in [("Papel A4", "CX", 10), ("Pincel Quadro Branco", "UN", 50), ("Tinta Impressora", "LT", 5), ("Sabonete Liquido", "LT", 20)]:
        ie = ItemEstoque.objects.create(nome=nome, unidade_medida=un, estoque_minimo=min_e)
        SaldoEstoque.objects.create(item=ie, unidade=escola, quantidade=min_e * 3)
        itens_est.append(ie)
        
    # Movimentacao de estoque de 10 anos
    for _ in range(50):
        MovimentacaoEstoque.objects.create(item=random.choice(itens_est), unidade=escola, tipo=random.choice(['ENTRADA', 'SAIDA']), quantidade=random.randint(1, 20), justificativa="Consumo do mes")

    # Financeiro Setup
    CategoriaFinanceira.objects.create(nome="Mensalidade Aluno", tipo="RECEITA")
    CategoriaFinanceira.objects.create(nome="Folha de Pagamento", tipo="DESPESA")
    CategoriaFinanceira.objects.create(nome="Tributos e Impostos", tipo="DESPESA")
    for cat in ["Agua e Esgoto", "Energia Eletrica", "Internet e Telefonia", "Manutencao Predial"]:
        CategoriaFinanceira.objects.create(nome=cat, tipo="DESPESA")

    for cc in ["Administrativo", "Pedagogico", "Infraestrutura e TI"]:
        CentroCusto.objects.create(nome=cc)
    
    print("      [OK] Infraestrutura e Finanças criadas.")
    return escola

@transaction.atomic
def seed_rh_e_biblioteca():
    print("[2/8] Semeando Gestores, Professores e Acervo Bibliografico...")
    
    u_gestor = User.objects.create_user(username="gestor_0", email="gestor@ifrn.edu.br", password="1")
    Gestor.objects.create(user=u_gestor, nome_completo="Joao Augusto Ferreira (Gestao)", cpf=gerar_cpf(), cargo="diretor")
    
    professores = []
    for i in range(15):
        u = User.objects.create_user(username=f"prof_{i}", email=f"prof_{i}@ifrn.edu.br", password="1")
        p = Professor.objects.create(user=u, nome_completo=f"Prof. {gerar_nome()}", cpf=gerar_cpf(), area_atuacao="Ensino Basico e Tecnologico")
        professores.append(p)
        
        # Atestados passados para professores
        if random.random() > 0.6:
            AtestadoMedico.objects.create(usuario=u, arquivo='saude/atestados/dummy.pdf', data_inicio=date(2021, 5, 10), data_fim=date(2021, 5, 15), descricao="Covid-19", status='APROVADO')

    livros = []
    print("      Iniciando download de capas de 200 Best Sellers mundiais via OpenLibrary API...")
    import requests
    from django.core.files.base import ContentFile
    
    subjects = ["classics", "science_fiction", "thriller", "historical_fiction", "fantasy"]
    
    for subject in subjects:
        try:
            url = f"https://openlibrary.org/subjects/{subject}.json?limit=40"
            resp = requests.get(url, timeout=15)
            data = resp.json()
            works = data.get("works", [])
            for work in works:
                titulo = work.get("title")
                autores = ", ".join([a["name"] for a in work.get("authors", [])]) if work.get("authors") else "Autor Desconhecido"
                cover_id = work.get("cover_id")
                
                l = Livro.objects.create(
                    titulo=titulo[:199],
                    autor=autores[:199],
                    isbn=f"OL-{work.get('key', '').split('/')[-1]}",
                    ano_publicacao=random.randint(1950, 2023),
                    quantidade_total=random.randint(2, 6)
                )
                livros.append(l)
                
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    try:
                        img_resp = requests.get(cover_url, timeout=10)
                        if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                            l.capa.save(f"capa_{cover_id}.jpg", ContentFile(img_resp.content), save=True)
                            print(f"        [+] Capa baixada: {titulo[:40]}...")
                    except Exception:
                        pass
                time.sleep(0.2) # Respeitando limites da API
        except Exception as e:
            print(f"        [-] Erro ao processar categoria {subject}: {e}")

    print(f"      [OK] Equipe RH e {len(livros)} livros criados.")
    return professores, u_gestor, livros

@transaction.atomic
def seed_academico_financeiro_10_anos(professores, u_gestor, escola, livros):
    print("[3/8] Iniciando a Maquina do Tempo: 10 Anos de Escola Real (2016-2026)...")
    print("      Este passo pode demorar varios minutos devido ao volume extremo de operacoes financeiras e de notas.")
    
    cat_mensal = CategoriaFinanceira.objects.get(nome="Mensalidade Aluno")
    cat_salarios = CategoriaFinanceira.objects.get(nome="Folha de Pagamento")
    cat_energia = CategoriaFinanceira.objects.get(nome="Energia Eletrica")
    cat_agua = CategoriaFinanceira.objects.get(nome="Agua e Esgoto")
    cat_internet = CategoriaFinanceira.objects.get(nome="Internet e Telefonia")
    cat_tributos = CategoriaFinanceira.objects.get(nome="Tributos e Impostos")
    
    cc_adm = CentroCusto.objects.get(nome="Administrativo")
    cc_infra = CentroCusto.objects.get(nome="Infraestrutura e TI")

    todas_faturas = []
    todos_pagamentos = []
    todos_lancamentos = []
    todas_folhas = []
    todas_frequencias = []
    todas_notas = []
    todos_emprestimos = []
    alunos_ano_list = []

    total_alunos_idx = 0

    for ano in range(2016, 2027):
        # Turmas
        turmas_ano = []
        for serie in ["1o Ano", "2o Ano", "3o Ano"]:
            t = Turma.objects.create(nome=f"{serie} B ({ano})", ano=ano, turno='manha')
            turmas_ano.append(t)
            
            # Disciplinas
            for idx_mat, nome_mat in enumerate(MATERIAS_BASE[:8]):
                Disciplina.objects.create(nome=nome_mat, turma=t, professor=professores[idx_mat % len(professores)])
                
        # Alunos daquele ano
        qtd_alunos = 20 if ano < 2026 else 40 # 2026 tem mais pra visualização atual
        for _ in range(qtd_alunos):
            total_alunos_idx += 1
            
            # Decide o destino do aluno
            if ano < 2024:
                status_mat = random.choices(['FORMADO', 'EVADIDO', 'TRANSFERIDO'], weights=[0.75, 0.15, 0.10])[0]
            elif ano == 2024 or ano == 2025:
                status_mat = random.choices(['ATIVO', 'EVADIDO'], weights=[0.85, 0.15])[0]
            else:
                status_mat = 'ATIVO'

            u_aluno = User.objects.create_user(username=f"aluno_{total_alunos_idx}_{ano}", email=f"a{total_alunos_idx}@ifrn.edu.br", password="1")
            turma_alvo = random.choice(turmas_ano)
            
            aluno = Aluno.objects.create(user=u_aluno, nome_completo=gerar_nome(), cpf=gerar_cpf(), status_matricula=status_mat, turma=turma_alvo)
            alunos_ano_list.append(aluno)
            
            # Saude e PCD
            is_pcd = random.random() > 0.9
            FichaMedica.objects.create(aluno=aluno, tipo_sanguineo=random.choice(TIPOS_SANGUINEOS), alergias=random.choice(['Nenhuma'] * 5 + ALERGIAS), medicamentos_continuos="Nenhum", condicoes_pcd=is_pcd, detalhes_pcd="Autismo Leve" if is_pcd else "")
            
            # Vacinas (Se recente)
            if ano > 2023:
                RegistroVacina.objects.create(ficha=aluno.ficha_medica, nome_vacina="Covid-19 Bivalente", data_dose=date(2024, 5, 20), lote="XXYYZZ")

            # Desempenho e Frequencia do Aluno naquele ano (Amostragem para caber na RAM e SQLite)
            disciplinas = list(turma_alvo.disciplinas.all())
            
            # Status: Aprovado, Reprovado por Falta, Reprovado por Nota (influencia notas e frequencia)
            if status_mat == 'FORMADO' or status_mat == 'ATIVO':
                is_bom = random.random() > 0.2
            else:
                is_bom = random.random() > 0.7 # Evadidos geralmente tem notas piores
                
            for disc in disciplinas:
                if is_bom:
                    todas_notas.append(Nota(aluno=aluno, disciplina=disc, nota1=Decimal(random.randint(6,10)), nota2=Decimal(random.randint(6,10)), nota3=Decimal(random.randint(6,10)), nota4=Decimal(random.randint(6,10))))
                else:
                    todas_notas.append(Nota(aluno=aluno, disciplina=disc, nota1=Decimal(random.randint(2,6)), nota2=Decimal(random.randint(2,6)), nota3=Decimal(random.randint(2,6)), nota4=Decimal(random.randint(2,6))))
                
                # Frequencias: 10 chamadas no ano para amostragem
                for mes in range(3, 11):
                    dt_aula = date(ano, mes, random.randint(1, 28))
                    presente = random.random() > 0.15 if is_bom else random.random() > 0.4
                    todas_frequencias.append(Frequencia(aluno=aluno, disciplina=disc, data=dt_aula, presente=presente))

            # Faturas Mensais (12 faturas)
            # Fevereiro a Janeiro (Mensalidades)
            for mes in range(1, 13):
                dt_venc = date(ano, mes, 5)
                # Se for um ano atual (2026) e um mês futuro, deixa PENDENTE
                if ano == 2026 and dt_venc > timezone.now().date():
                    status_fat = 'PENDENTE'
                else:
                    # Anos/meses passados: Evadidos tem inadimplencia, Formados pagam tudo
                    if status_mat == 'EVADIDO' and mes > 6:
                        status_fat = 'PENDENTE' # Ficou inadimplente e sumiu
                    else:
                        status_fat = 'PAGO' if random.random() > 0.05 else 'PENDENTE' # 5% de inadimplencia historica de esquecimento
                        
                fat = Fatura(aluno=aluno, descricao=f"Mensalidade {mes:02d}/{ano}", valor=Decimal('500.00'), data_vencimento=dt_venc, status=status_fat)
                todas_faturas.append(fat)
                
            # Biblioteca
            if random.random() > 0.5:
                dt_emp = date(ano, 5, random.randint(1, 28))
                dt_dev = dt_emp + timedelta(days=14)
                devolveu = status_mat != 'EVADIDO'
                todos_emprestimos.append(Emprestimo(livro=random.choice(livros), usuario_aluno=aluno, data_emprestimo=dt_emp, data_devolucao_prevista=dt_dev, data_devolucao_real=dt_dev if devolveu else None, status='DEVOLVIDO' if devolveu else 'ATRASADO', status_leitura='FINALIZADO'))

        # Lançamentos Mensais Corporativos da Escola naquele ano (12 meses)
        for mes in range(1, 13):
            if ano == 2026 and mes > timezone.now().month:
                break
            dt_base = date(ano, mes, 15)
            # Custos Base
            todos_lancamentos.append(Lancamento(tipo='SAIDA', categoria=cat_energia, data_pagamento=dt_base, valor=Decimal(random.randint(3000, 5000) + (ano - 2016)*200), descricao=f"Energia {mes}/{ano}", centro_custo=cc_infra, autorizado_por=u_gestor))
            todos_lancamentos.append(Lancamento(tipo='SAIDA', categoria=cat_agua, data_pagamento=dt_base, valor=Decimal(random.randint(1000, 2000)), descricao=f"Agua {mes}/{ano}", centro_custo=cc_infra, autorizado_por=u_gestor))
            todos_lancamentos.append(Lancamento(tipo='SAIDA', categoria=cat_internet, data_pagamento=dt_base, valor=Decimal('1500.00'), descricao=f"Internet {mes}/{ano}", centro_custo=cc_infra, autorizado_por=u_gestor))
            todos_lancamentos.append(Lancamento(tipo='SAIDA', categoria=cat_tributos, data_pagamento=dt_base, valor=Decimal(random.randint(8000, 15000)), descricao=f"Impostos ISS/INSS {mes}/{ano}", centro_custo=cc_adm, autorizado_por=u_gestor))
            
            # Folha de Pagamento Professores
            for prof in professores:
                sal_base = Decimal('4000.00') + Decimal((ano - 2016) * 200) # Simula aumento de salario ao longo dos anos
                todas_folhas.append(FolhaPagamento(funcionario=prof.user, mes_referencia=mes, ano_referencia=ano, salario_base=sal_base, impostos_encargos=Decimal('800.00'), pago=True, data_pagamento=dt_base))
                todos_lancamentos.append(Lancamento(tipo='SAIDA', categoria=cat_salarios, data_pagamento=dt_base, valor=sal_base, descricao=f"Salario {prof.nome_completo}", centro_custo=cc_adm, autorizado_por=u_gestor))

        print(f"      [{ano}] Processado. Gerando DB records em memória...")
        
    print("[4/8] Gravando Historico no Banco de Dados (Pode demorar uns minutos)...")
    Fatura.objects.bulk_create(todas_faturas, batch_size=2000)
    print("      Faturas (OK)")
    
    # Criando Pagamentos baseados nas Faturas Pagas
    print("      Processando cruzamento financeiro de receitas (Pagamentos e Livro Diario)...")
    faturas_salvas = Fatura.objects.filter(status='PAGO').select_related('aluno', 'aluno__user')
    for f in faturas_salvas:
        dt_pag = f.data_vencimento - timedelta(days=random.randint(0, 4))
        # timezone aware
        dt_pag_dt = timezone.make_aware(datetime.combine(dt_pag, datetime.min.time()))
        todos_pagamentos.append(Pagamento(fatura=f, valor_pago=f.valor, data_pagamento=dt_pag_dt, metodo=random.choice(['PIX', 'BOLETO'])))
        todos_lancamentos.append(Lancamento(tipo='ENTRADA', categoria=cat_mensal, data_pagamento=dt_pag, valor=f.valor, descricao=f"Mensalidade {f.aluno.nome_completo}", centro_custo=cc_adm, autorizado_por=f.aluno.user, fatura_origem=f))
        
    Pagamento.objects.bulk_create(todos_pagamentos, batch_size=2000)
    Lancamento.objects.bulk_create(todos_lancamentos, batch_size=2000)
    FolhaPagamento.objects.bulk_create(todas_folhas, batch_size=2000)
    Emprestimo.objects.bulk_create(todos_emprestimos, batch_size=2000)
    Nota.objects.bulk_create(todas_notas, batch_size=2000)
    Frequencia.objects.bulk_create(todas_frequencias, batch_size=2000)
    print("      [OK] Bulk Creates concluidos com sucesso.")


@transaction.atomic
def seed_rotinas_2026_atuais():
    print("[5/8] Simulando Rotina Atual e Diários (2026)...")
    # Focar em turmas de 2026
    turmas = Turma.objects.filter(ano=2026)
    alunos = Aluno.objects.filter(turma__ano=2026, status_matricula='ATIVO')
    
    # Planejamentos, Atestados e Eventos de Calendario
    EventoCalendario.objects.create(data=date(2026, 2, 5), tipo='DI_LETIVO', descricao="Inicio do Ano Letivo")
    EventoCalendario.objects.create(data=date(2026, 3, 2), tipo='RECESSO', descricao="Carnaval")
    EventoCalendario.objects.create(data=date(2026, 4, 15), tipo='PROVA', descricao="Semana de Provas do 1 Bimestre")
    
    Comunicado.objects.create(titulo="Uso Obrigatorio de Uniforme", conteudo="A partir de segunda, todos devem portar fardamento.", importancia="ALTA", publico_alvo="ALUNOS")
    
    for turma in turmas:
        for disc in turma.disciplinas.all()[:3]: # Apenas 3 materias pra poupar tempo
            PlanejamentoAula.objects.create(disciplina=disc, data_aula=date(2026, 3, 10), horario_aula="07:00 - 08:40", professor=disc.professor, turma=turma, conteudo=f"Unidade Introdutória - {disc.nome}", concluido=True)
            AtividadeProfessor.objects.create(disciplina=disc, titulo=f"Prova 1 - {disc.nome}", tipo="PROVA", data=date(2026, 4, 15), descricao="Prova presencial")
            MaterialDidatico.objects.create(disciplina=disc, titulo="Apostila PDF", tipo="ARQUIVO", descricao="Livro texto")
            
            GradeHorario.objects.create(turma=turma, disciplina=disc, dia='segunda', horario="07:00 - 08:40")

    # Alguns alunos com atestado recente e notificacoes
    gestor = Gestor.objects.first()
    for aluno in alunos[:5]:
        AtestadoMedico.objects.create(usuario=aluno.user, arquivo="saude/atestado.pdf", data_inicio=date(2026, 3, 15), data_fim=date(2026, 3, 18), descricao="Conjuntivite", status="APROVADO", analisado_por=gestor)
        Notificacao.objects.create(usuario=aluno.user, titulo="Atestado Aceito", mensagem="Suas faltas serao abonadas.", tipo='SISTEMA')
        
    print("      [OK] Ano atual populado (Calendario, Mural, Diarios, Notificacoes).")


def seed():
    print("\n" + "=" * 70)
    print("  SIGE - GERADOR MASSIVO DE DADOS (ESCOLA REAL - 10 ANOS)")
    print("=" * 70)
    start_time = time.time()
    
    limpar_banco()
    seed_infra_e_financas()
    professores, u_gestor, livros = seed_rh_e_biblioteca()
    seed_academico_financeiro_10_anos(professores, u_gestor, None, livros)
    seed_rotinas_2026_atuais()
    
    end_time = time.time()
    print("\n" + "=" * 70)
    print(f"  BANCO DE DADOS PREENCHIDO COM SUCESSO! ({round(end_time - start_time, 2)}s)")
    print("=" * 70)
    print(f"  Contagem de Registros Massivos:")
    print(f"    - Alunos: {Aluno.objects.count()}")
    print(f"    - Faturas: {Fatura.objects.count()}")
    print(f"    - Lançamentos Financeiros (Livro Diário): {Lancamento.objects.count()}")
    print(f"    - Folhas de Pagamento: {FolhaPagamento.objects.count()}")
    print(f"    - Frequencias de Aula: {Frequencia.objects.count()}")
    print(f"    - Notas: {Nota.objects.count()}")
    print(f"    - Movimentacoes Estoque: {MovimentacaoEstoque.objects.count()}")
    print("=" * 70)
    print("  Usuarios de Acesso (Senha padrao: 1):")
    print("    Gestor: gestor_0")
    print("    Professor: prof_0")
    print("    Alunos (Ex): aluno_1_2016 ... aluno_240_2026")
    print("=" * 70)

if __name__ == "__main__":
    seed()