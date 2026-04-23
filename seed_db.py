"""
SIGE - Super Script de Populacao de Banco de Dados
Padrao: IFRN (Instituto Federal do Rio Grande do Norte)

Como executar:
  PowerShell: ..\venv\Scripts\python.exe seed_db.py
  CMD:        ..\venv\Scripts\python seed_db.py
  Linux/Mac:  ../venv/bin/python seed_db.py

O script e idempotente: pode ser rodado multiplas vezes sem duplicar dados.
"""

import os
import django
import random
import requests
import time
from django.utils import timezone
from datetime import date, timedelta, time as dt_time
from decimal import Decimal
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.usuarios.models.perfis import Gestor, Professor, Aluno
from apps.biblioteca.models.biblioteca import Livro
from apps.saude.models.ficha_medica import FichaMedica, AtestadoMedico
from apps.financeiro.models import Fatura
from apps.academico.models.academico import Turma, Disciplina, PlanejamentoAula, AtividadeProfessor, MaterialDidatico, GradeHorario
from apps.academico.models.desempenho import Frequencia, Nota
from apps.calendario.models.calendario import EventoCalendario
from apps.comunicacao.models.comunicado import Comunicado

User = get_user_model()

# ═══════════════════════════════════════════════════════════════════
# NOMES BRASILEIROS
# ═══════════════════════════════════════════════════════════════════
PRIMEIROS_NOMES_M = [
    "Joao", "Jose", "Carlos", "Paulo", "Lucas", "Marcos", "Ricardo",
    "Gabriel", "Diego", "Roberto", "Felipe", "Thiago", "Bruno", "Eduardo",
    "Rodrigo", "Anderson", "Gustavo", "Leonardo", "Alexandre", "Fabio",
    "Henrique", "Sergio", "Rafael", "Leandro", "Marcelo", "Daniel", "Igor",
    "Caio", "Victor", "Arthur", "Samuel", "Matheus", "Pedro", "Vitor",
    "Jonathan", "Luiz", "Francisco", "Raimundo", "Aldair", "Wendell",
    "Wilker", "Davi", "Enzo", "Nicolas", "Lorenzo", "Kayke", "Raul",
    "Murilo", "Otavio", "Nathan"
]

PRIMEIROS_NOMES_F = [
    "Maria", "Ana", "Juliana", "Beatriz", "Fernanda", "Patricia", "Camila",
    "Leticia", "Aline", "Priscila", "Vanessa", "Mariana", "Tatiana",
    "Carla", "Simone", "Renata", "Cristina", "Sandra", "Monica", "Lucia",
    "Denise", "Claudia", "Rosana", "Elaine", "Viviane", "Natalia", "Livia",
    "Isabela", "Giovanna", "Amanda", "Larissa", "Gabriela", "Lara",
    "Eduarda", "Vitoria", "Yasmin", "Bianca", "Stephanie", "Debora",
    "Raquel", "Caroline", "Julienne", "Rebeca", "Mayara", "Nathalia",
    "Ingrid", "Bruna", "Thalita", "Jeniffer", "Keila"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Ferreira", "Rocha",
    "Costa", "Pereira", "Alves", "Gomes", "Ribeiro", "Carvalho", "Martins",
    "Lopes", "Barbosa", "Almeida", "Castro", "Nascimento", "Vieira",
    "Melo", "Dantas", "Cavalcanti", "Bezerra", "Farias", "Guedes",
    "Xavier", "Brito", "Nunes", "Sales", "Medeiros", "Araujo", "Cardoso",
    "Moura", "Teixeira", "Pinto", "Macedo", "Freitas", "Azevedo", "Cunha"
]

# ═══════════════════════════════════════════════════════════════════
# 100 BEST SELLERS MUNDIAIS
# ═══════════════════════════════════════════════════════════════════
LIVROS_BESTSELLERS = [
    ("Dom Quixote", "Miguel de Cervantes", "978-85-359-0277-5"),
    ("O Alquimista", "Paulo Coelho", "978-85-200-0770-0"),
    ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", "978-85-325-0479-3"),
    ("O Pequeno Principe", "Antoine de Saint-Exupery", "978-85-250-0339-5"),
    ("O Senhor dos Aneis", "J.R.R. Tolkien", "978-85-287-0010-8"),
    ("Cem Anos de Solidao", "Gabriel Garcia Marquez", "978-85-01-00236-0"),
    ("A Biblia", "Varios Autores", "978-85-326-0017-5"),
    ("Pense e Enriqueca", "Napoleon Hill", "978-85-7448-040-5"),
    ("O Codigo Da Vinci", "Dan Brown", "978-85-01-06908-0"),
    ("Orgulho e Preconceito", "Jane Austen", "978-85-213-1530-1"),
    ("1984", "George Orwell", "978-85-351-0274-9"),
    ("Crime e Castigo", "Fiodor Dostoievski", "978-85-325-0113-6"),
    ("A Metamorfose", "Franz Kafka", "978-85-7616-086-1"),
    ("O Coracao das Trevas", "Joseph Conrad", "978-85-7736-225-9"),
    ("Admiravel Mundo Novo", "Aldous Huxley", "978-85-351-0147-6"),
    ("O Velho e o Mar", "Ernest Hemingway", "978-85-01-00168-4"),
    ("Moby Dick", "Herman Melville", "978-85-261-0105-2"),
    ("A Divina Comedia", "Dante Alighieri", "978-85-390-0063-1"),
    ("Guerra e Paz", "Lev Tolstoi", "978-85-01-02053-0"),
    ("Anna Karenina", "Lev Tolstoi", "978-85-01-02054-7"),
    ("O Apanhador no Campo de Centeio", "J.D. Salinger", "978-85-325-1617-8"),
    ("Lolita", "Vladimir Nabokov", "978-85-359-0182-2"),
    ("O Retrato de Dorian Gray", "Oscar Wilde", "978-85-7622-182-4"),
    ("Frankenstein", "Mary Shelley", "978-85-7888-042-3"),
    ("Dracula", "Bram Stoker", "978-85-7887-892-5"),
    ("Alice no Pais das Maravilhas", "Lewis Carroll", "978-85-7616-452-4"),
    ("A Volta ao Mundo em 80 Dias", "Julio Verne", "978-85-374-0014-3"),
    ("O Hobbit", "J.R.R. Tolkien", "978-85-287-0122-8"),
    ("As Cronicas de Narnia", "C.S. Lewis", "978-85-264-1105-4"),
    ("O Diario de Anne Frank", "Anne Frank", "978-85-7632-045-9"),
    ("Sapiens - Breve Historia da Humanidade", "Yuval Noah Harari", "978-85-437-0489-1"),
    ("Homo Deus", "Yuval Noah Harari", "978-85-437-0578-2"),
    ("21 Licoes para o Seculo 21", "Yuval Noah Harari", "978-85-437-0788-5"),
    ("O Poder do Habito", "Charles Duhigg", "978-85-8057-310-3"),
    ("Comece pelo Porque", "Simon Sinek", "978-85-8057-256-4"),
    ("A Startup Enxuta", "Eric Ries", "978-85-7608-629-4"),
    ("Zero to One", "Peter Thiel", "978-85-437-0289-7"),
    ("Pai Rico Pai Pobre", "Robert T. Kiyosaki", "978-85-7530-034-0"),
    ("Inteligencia Emocional", "Daniel Goleman", "978-85-325-0701-5"),
    ("A Arte da Guerra", "Sun Tzu", "978-85-254-0887-1"),
    ("Introducao aos Algoritmos", "Thomas H. Cormen", "978-85-352-3014-9"),
    ("Redes de Computadores", "Andrew S. Tanenbaum", "978-85-7641-797-9"),
    ("Banco de Dados - Sistemas e Conceitos", "Ramakrishnan & Gehrke", "978-85-8143-069-1"),
    ("Fisica para Cientistas e Engenheiros", "Raymond A. Serway", "978-85-221-0417-6"),
    ("Calculo Volume 1", "James Stewart", "978-85-221-0547-0"),
    ("Calculo Volume 2", "James Stewart", "978-85-221-0548-7"),
    ("Quimica Organica", "Jonathan Clayden", "978-85-7143-980-4"),
    ("Biologia Celular e Molecular", "Albert Bruce", "978-85-7600-275-3"),
    ("Historia do Brasil", "Boris Fausto", "978-85-314-0348-4"),
    ("O Homem que Calculava", "Malba Tahan", "978-85-01-01618-2"),
    ("Matematica - Hamilton Guidorizzi", "Hamilton L. Guidorizzi", "978-85-216-1266-7"),
    ("Sociologia", "Anthony Giddens", "978-85-82129-04-2"),
    ("Filosofia - Uma Introducao", "Thomas Nagel", "978-85-7811-066-2"),
    ("Ingles para Comunicacao", "Samuela Eckstut", "978-85-343-0196-4"),
    ("Empreendedorismo - Como Nascem os Negocios", "Jose Dornelas", "978-85-352-3832-9"),
    ("Gestao de Projetos - PMI Guide", "Project Management Institute", "978-85-8143-450-7"),
    ("Python para Todos", "Charles R. Severance", "978-85-7893-293-1"),
    ("Linguagem de Programacao C", "Brian W. Kernighan", "978-85-7614-093-2"),
    ("Programacao Web com HTML e CSS", "Jon Duckett", "978-85-7657-207-4"),
    ("JavaScript - O Guia Definitivo", "David Flanagan", "978-85-7780-691-2"),
    ("Sistemas Operacionais Modernos", "Andrew S. Tanenbaum", "978-85-7641-518-0"),
    ("Arquitetura de Computadores", "David Patterson", "978-85-352-3038-5"),
    ("Machine Learning - Tom Mitchell", "Tom Mitchell", "978-85-8143-451-4"),
    ("Deep Learning", "Ian Goodfellow", "978-85-352-8988-7"),
    ("Inteligencia Artificial - Norvig", "Russell & Norvig", "978-85-352-1177-3"),
    ("Seguranca em Computacao", "William Stallings", "978-85-7780-693-6"),
    ("Engenharia de Software - Sommerville", "Ian Sommerville", "978-85-7936-073-2"),
    ("Padroes de Projeto", "Erich Gamma et al.", "978-85-7780-162-7"),
    ("Codigo Limpo", "Robert C. Martin", "978-85-7780-484-0"),
    ("O Programador Pragmatico", "Andrew Hunt", "978-85-7522-288-5"),
    ("Estrutura de Dados em C", "Peter Brass", "978-85-7722-400-0"),
    ("Logica de Programacao", "Silvio Lago", "978-85-7522-050-8"),
    ("Teoria dos Grafos", "Lucchesi & Kohayakawa", "978-85-225-0630-2"),
    ("Algebra Linear", "Gilbert Strang", "978-85-221-0870-9"),
    ("Probabilidade e Estatistica", "Degroot & Schervish", "978-85-221-0872-3"),
    ("Pesquisa Operacional", "Frederick Hillier", "978-85-7600-264-7"),
    ("Economia", "Paul Samuelson", "978-85-352-1020-2"),
    ("Direito Constitucional", "Alexandre de Moraes", "978-85-97-00302-3"),
    ("Sociologia Juridica", "Roberto Lyra Filho", "978-85-230-0780-1"),
    ("Etica em Computacao", "Herman T. Tavani", "978-85-7614-567-8"),
    ("Privacidade e Seguranca Digital", "Bruce Schneier", "978-85-7893-190-3"),
    ("O Mundo de Sofia", "Jostein Gaarder", "978-85-325-0682-7"),
    ("A Insustentavel Leveza do Ser", "Milan Kundera", "978-85-359-0291-1"),
    ("A Quinta Montanha", "Paulo Coelho", "978-85-200-0395-5"),
    ("Brida", "Paulo Coelho", "978-85-200-0316-0"),
    ("Veronika Decide Morrer", "Paulo Coelho", "978-85-200-0439-6"),
    ("O Diario de um Mago", "Paulo Coelho", "978-85-200-0127-2"),
    ("A Cabana", "William P. Young", "978-85-01-08009-3"),
    ("O Shack", "William P. Young", "978-85-01-08010-9"),
    ("Tuesdays with Morrie", "Mitch Albom", "978-85-7522-051-5"),
    ("Cinco Pessoas que Voce Encontra no Ceu", "Mitch Albom", "978-85-7522-285-4"),
    ("A Hora da Estrela", "Clarice Lispector", "978-85-359-0149-5"),
    ("Dom Casmurro", "Machado de Assis", "978-85-259-0040-7"),
    ("Memorias Postumas de Bras Cubas", "Machado de Assis", "978-85-259-0042-1"),
    ("Iracema", "Jose de Alencar", "978-85-259-0037-7"),
    ("Grande Sertao: Veredas", "Joao Guimaraes Rosa", "978-85-301-0079-4"),
    ("Vidas Secas", "Graciliano Ramos", "978-85-01-01626-7"),
    ("Menino de Engenho", "Jose Lins do Rego", "978-85-01-01627-4"),
    ("O Auto da Compadecida", "Ariano Suassuna", "978-85-259-0008-7"),
    ("A Pedra do Reino", "Ariano Suassuna", "978-85-259-0029-2"),
]

# ═══════════════════════════════════════════════════════════════════
# 40 DISCIPLINAS
# ═══════════════════════════════════════════════════════════════════
MATERIAS = [
    # Nucleo Comum
    "Matematica I", "Matematica II", "Matematica III",
    "Lingua Portuguesa I", "Lingua Portuguesa II", "Literatura Brasileira",
    "Fisica I", "Fisica II", "Fisica III",
    "Quimica I", "Quimica II",
    "Biologia I", "Biologia II",
    "Historia I", "Historia II",
    "Geografia I", "Geografia II",
    "Sociologia", "Filosofia", "Educacao Fisica",
    # Nucleo Tecnico
    "Algoritmos e Logica de Programacao",
    "Programacao Orientada a Objetos",
    "Estrutura de Dados",
    "Banco de Dados I",
    "Banco de Dados II",
    "Redes de Computadores I",
    "Redes de Computadores II",
    "Sistemas Operacionais",
    "Programacao Web Frontend",
    "Programacao Web Backend",
    "Desenvolvimento Mobile",
    "Seguranca da Informacao",
    "Engenharia de Software",
    "Inteligencia Artificial",
    "Computacao em Nuvem",
    "Ingles Tecnico I",
    "Ingles Tecnico II",
    # Eletivas/Complementares
    "Empreendedorismo",
    "Gestao de Projetos",
    "Etica Profissional e Legislacao",
]

# ═══════════════════════════════════════════════════════════════════
# DADOS DE SAUDE
# ═══════════════════════════════════════════════════════════════════
ALERGIAS = [
    "Dipirona", "Penicilina", "Amoxicilina", "Ibuprofeno", "Aspirina",
    "Lactose", "Gluten", "Frutos do mar", "Amendoim", "Soja",
    "Poeira", "Polens", "Acaro", "Mofo", "Pelos de animais",
    "Latex", "Niquel", "Corantes artificiais", "Sulfas", "Cefalosporinas",
    "Metronidazol", "Contraste iodado", "Ovo", "Trigo", "Nozes",
]

MEDICAMENTOS = [
    "Ritalina (metilfenidato) 10mg - 1x ao dia (manha)",
    "Concerta (metilfenidato) 18mg - 1x ao dia (manha)",
    "Strattera (atomoxetina) 40mg - 1x ao dia (noite)",
    "Seroquel (quetiapina) 25mg - 1x ao dia (noite)",
    "Rivotril (clonazepam) 0,5mg - 1x ao dia (noite)",
    "Fluoxetina 20mg - 1x ao dia (manha)",
    "Sertralina 50mg - 1x ao dia (manha)",
    "Escitalopram 10mg - 1x ao dia (manha)",
    "Losartana 50mg - 1x ao dia",
    "Metformina 500mg - 2x ao dia (refeicoes)",
    "Levotiroxina 50mcg - 1x ao dia (jejum)",
    "Salbutamol spray 100mcg - uso quando necessario",
    "Seretide (salmeterol+fluticasona) - 2x ao dia",
    "Tegretol (carbamazepina) 200mg - 2x ao dia",
    "Depakote (valproato) 500mg - 2x ao dia",
    "Insulina Glargina 20UI - 1x ao dia (noite)",
    "Insulina Lispro - conforme glicemia pre-prandial",
    "Omeprazol 20mg - 1x ao dia (jejum)",
    "Atenolol 25mg - 1x ao dia (manha)",
    "Clonidina 0,1mg - 2x ao dia",
    "Risperidona 1mg - 1x ao dia (noite)",
    "Aripiprazol 5mg - 1x ao dia (manha)",
    "Melatonina 3mg - 1x ao dia (noite)",
    "Topiramato 25mg - 2x ao dia",
    "Lamotrigina 50mg - 2x ao dia",
    "Prednisolona 5mg - uso continuo",
    "Azatioprina 50mg - 1x ao dia",
    "Mesalazina 400mg - 3x ao dia",
    "Sulfassalazina 500mg - 2x ao dia",
    "Hidroxicloroquina 400mg - 1x ao dia",
]

PERFIS_PCD = [
    ("TDAH - Transtorno de Deficit de Atencao e Hiperatividade (Grau Moderado)", True,
     "Necessita de sala de prova diferenciada e tempo adicional de 1h. Evitar distractores visuais."),
    ("TDAH - Transtorno de Deficit de Atencao e Hiperatividade (Grau Leve)", True,
     "Tempo adicional de 30 minutos nas provas. Sala de menor circulacao recomendada."),
    ("TEA - Transtorno do Espectro Autista (Nivel 1 - Leve)", True,
     "Comunicacao assistida; mediador em sala recomendado. Rotinas previsíveis sao essenciais."),
    ("TEA - Transtorno do Espectro Autista (Nivel 2 - Moderado)", True,
     "Necessita de monitor e material didatico adaptado. Sala de recursos disponivel."),
    ("Deficiencia Visual - Baixa Visao (acuidade 20/200 com oculos)", True,
     "Provas em fonte 18, ampliacao de tela 200%. Sentado na frente da sala."),
    ("Deficiencia Visual - Cegueira Total (usuario de Braille e JAWS)", True,
     "Prova em Braille ou com ledor; sala equipada com software JAWS. Tempo adicional de 1h."),
    ("Deficiencia Auditiva - Perda Parcial 50dB (usa aparelho auditivo)", True,
     "Sentado proximo ao professor; interprete de LIBRAS recomendado quando possivel."),
    ("Deficiencia Auditiva - Surdez Total (usuario fluente de LIBRAS)", True,
     "Interprete de LIBRAS obrigatorio em todas as aulas e avaliacoes presenciais."),
    ("Deficiencia Fisica - Paraplegia (usuario de cadeira de rodas)", True,
     "Acesso por rampa; banheiro adaptado; mesa com altura regulavel obrigatoria."),
    ("Deficiencia Fisica - Hemiplegia Leve (dificuldade motora mao direita)", True,
     "Permite uso de computador para provas discursivas. Mesa do lado esquerdo da sala."),
    ("Dislexia e Disortografia (Laudo Neurologico - CID F81)", True,
     "Tempo adicional de 30min; avaliacao oral permitida; nao penalizar ortografia."),
    ("Discalculia (Laudo Psicopedagogico - CID F81.2)", True,
     "Permite uso de calculadora simples; formula sheets fornecidas nas provas."),
    ("Sindrome de Down - Trissomia 21 (QI Limite - curriculo adaptado)", True,
     "Curriculo adaptado; acompanhamento psicopedagogico semanal; avaliacao diferenciada."),
    ("Transtorno de Ansiedade Generalizada com Laudo Psiquiatrico (CID F41.1)", False,
     "Sala de prova com menor numero de alunos recomendada. Medicacao na secretaria."),
    ("Epilepsia Controlada por Medicacao (CID G40)", False,
     "Medicacao disponivel na enfermaria; professores orientados sobre primeiros socorros."),
    ("Diabetes Tipo 1 (usuario de bomba de insulina)", False,
     "Permissao para sair da sala para monitorar glicemia; lanchinhos autorizados."),
    ("Doenca de Crohn (CID K50) - Fase de Remissao", False,
     "Permissao para usar o banheiro sem restricoes. Evitar periodos prolongados sem intervalo."),
    ("Lupus Eritematoso Sistemico (CID M32) - Fase Estavel", False,
     "Evitar exposicao prolongada ao sol. Aulas externas requerem protecao solar adequada."),
    ("Transtorno de Processamento Sensorial (Laudo OT)", True,
     "Fones de ouvido permitidos durante avaliacoes. Evitar luz fluorescente intensa."),
    ("Paralisia Cerebral - Diplegia Espastica (CID G80.1)", True,
     "Cadeira de rodas; escrita assistida por computador; tempo adicional de 1h."),
]

DOENCAS_COMUNS = [
    "Asma (CID J45) - controlada",
    "Rinite Alergica (CID J30) - perene",
    "Hipotireoidismo (CID E03) - uso de Levotiroxina",
    "Gastrite Cronica (CID K29.7)",
    "Hipertensao Arterial Leve (CID I10)",
    "Anemia Ferropriva (CID D50)",
    "Ansiedade Social (CID F40.1)",
    "Depressao Leve (CID F32.0)",
    "Cefaleia Tensional Cronica (CID G44.2)",
    "Hernia de Disco Lombar (CID M51.1)",
    "Escoliose Leve (CID M41.9)",
    "Diabetes Tipo 2 Inicial (CID E11)",
    "Hipoglicemia Reativa",
    "Miopia Alta (CID H52.1)",
    "",  # Sem doencas cronicas (maioria dos alunos)
    "",
    "",
    "",
    "",
    "",
]

# ═══════════════════════════════════════════════════════════════════
# DADOS ACADEMICOS
# ═══════════════════════════════════════════════════════════════════
CARGOS = ["diretor", "vice_diretor", "coordenador", "secretario"]

TIPOS_SANGUINEOS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

FORMACOES_PROF = [
    "Doutorado em Matematica Aplicada - UFRN",
    "Doutorado em Ciencia da Computacao - UFPE",
    "Doutorado em Fisica - UFRN",
    "Doutorado em Quimica - UFC",
    "Doutorado em Biologia Molecular - UFRN",
    "Doutorado em Historia - UFPB",
    "Doutorado em Linguistica - UFPE",
    "Doutorado em Educacao Matematica - UFRN",
    "Mestrado em Ciencia da Computacao - UFRN",
    "Mestrado em Engenharia de Software - UFPE",
    "Mestrado em Redes de Computadores - UFRN",
    "Mestrado em Banco de Dados - UFC",
    "Mestrado em Linguistica Aplicada - UFRN",
    "Mestrado em Fisica Aplicada - UFRN",
    "Especialista em Informatica na Educacao - IFRN",
    "Especialista em Gestao Publica - UFRN",
    "Especialista em Seguranca da Informacao - UNICAMP",
    "Especialista em Desenvolvimento Web - PUC-Rio",
    "Graduado em Ciencia da Computacao - UFRN",
    "Graduado em Matematica - UFRN",
]

LINKS_MATERIAIS = [
    ("Khan Academy - Matematica", "https://pt.khanacademy.org/math"),
    ("Khan Academy - Fisica", "https://pt.khanacademy.org/science/physics"),
    ("Khan Academy - Quimica", "https://pt.khanacademy.org/science/chemistry"),
    ("Khan Academy - Biologia", "https://pt.khanacademy.org/science/biology"),
    ("YouTube - Matematica Rio", "https://www.youtube.com/@matematicario"),
    ("YouTube - Me Salva!", "https://www.youtube.com/@mesalva"),
    ("YouTube - Descomplica", "https://www.youtube.com/@descomplica"),
    ("Coursera - Programming for Everybody", "https://www.coursera.org/learn/python"),
    ("freeCodeCamp - Web Development", "https://www.freecodecamp.org/"),
    ("MDN Web Docs - HTML/CSS/JS", "https://developer.mozilla.org/pt-BR/"),
    ("W3Schools - Tutorial Online", "https://www.w3schools.com/"),
    ("GeeksforGeeks - CS Portal", "https://www.geeksforgeeks.org/"),
    ("Cisco NetAcad - Redes", "https://www.netacad.com/"),
    ("Oracle Academy - Banco de Dados", "https://academy.oracle.com/"),
    ("Google Developers - Mobile", "https://developers.google.com/"),
    ("AWS Training - Cloud", "https://aws.amazon.com/training/"),
    ("IFRN Moodle - Plataforma EAD", "https://moodle.ifrn.edu.br/"),
    ("SUAP IFRN - Sistema Academico", "https://suap.ifrn.edu.br/"),
    ("MIT OpenCourseWare - CS", "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"),
    ("Codecademy - Learn Python", "https://www.codecademy.com/learn/learn-python-3"),
    ("LeetCode - Algoritmos", "https://leetcode.com/"),
    ("HackerRank - Pratica", "https://www.hackerrank.com/"),
    ("YouTube - Programacao em C", "https://www.youtube.com/@bosontreinamentos"),
    ("Portugues Redacao ENEM", "https://www.stoodi.com.br/"),
    ("Historia - Brasil Escola", "https://brasilescola.uol.com.br/historiab"),
    ("IBGE Educa - Geografia", "https://educa.ibge.gov.br/"),
    ("Filosofia - Toda Materia", "https://www.todamateria.com.br/filosofia/"),
    ("Sociologia - Info Escola", "https://www.infoescola.com/sociologia/"),
]

TIPOS_EVENTOS_CALENDARIO = [
    ("Inicio do Ano Letivo 2026", "AULA", False),
    ("Recesso de Carnaval", "FERIAS", True),
    ("Semana de Provas - 1o Bimestre", "PROVA", False),
    ("Semana Santa - Feriado Nacional", "FERIADO", True),
    ("Reuniao Pedagogica - Planejamento", "REUNIAO", False),
    ("Ferias do 1o Semestre (Julho)", "FERIAS", True),
    ("Retorno do 2o Semestre", "AULA", False),
    ("Semana de Provas - 3o Bimestre", "PROVA", False),
    ("Dia dos Professores - Feriado Escolar", "FERIADO", True),
    ("Semana de Provas - 4o Bimestre", "PROVA", False),
    ("Feira de Ciencia e Tecnologia do IFRN", "EVENTO", False),
    ("Formatura das Turmas Concluintes", "EVENTO", False),
    ("Encerramento do Ano Letivo", "AULA", False),
    ("Recesso Fim de Ano", "FERIAS", True),
    ("Dia da Consciencia Negra - Feriado", "FERIADO", True),
    ("Dia da Republica - Feriado Nacional", "FERIADO", True),
    ("Independencia do Brasil - Feriado", "FERIADO", True),
    ("Tiradentes - Feriado Nacional", "FERIADO", True),
    ("Corpus Christi - Feriado Nacional", "FERIADO", True),
    ("Nossa Senhora Aparecida - Feriado", "FERIADO", True),
    ("Finados - Feriado Nacional", "FERIADO", True),
    ("Simulado Nacional ENEM", "PROVA", False),
    ("Semana da Tecnologia e Inovacao", "EVENTO", False),
    ("Olimpiada de Matematica - OBMEP", "EVENTO", False),
    ("Olimpiada Brasileira de Informatica", "EVENTO", False),
    ("Visita Tecnica - Empresas Parceiras", "EVENTO", False),
    ("Semana de Orientacao Profissional", "REUNIAO", False),
    ("Gincana Cultural Interdisciplinar", "EVENTO", False),
    ("Reuniao de Pais e Mestres - 1o Bimestre", "REUNIAO", False),
    ("Reuniao de Pais e Mestres - 2o Bimestre", "REUNIAO", False),
    ("Reuniao de Pais e Mestres - 3o Bimestre", "REUNIAO", False),
    ("Reuniao de Pais e Mestres - 4o Bimestre", "REUNIAO", False),
    ("Conselho de Classe - 1o Bimestre", "REUNIAO", False),
    ("Conselho de Classe - 2o Bimestre", "REUNIAO", False),
    ("Conselho de Classe - 3o Bimestre", "REUNIAO", False),
    ("Conselho de Classe - 4o Bimestre", "REUNIAO", False),
    ("Exame Final - Recuperacao", "PROVA", False),
    ("Matriculas 2027 - Novos Alunos", "EVENTO", False),
    ("Palestra sobre Profissoes e Mercado de Trabalho", "EVENTO", False),
    ("Hackathon IFRN 2026", "EVENTO", False),
]

AVISOS_MURAL = [
    {
        "titulo": "⚠️ ATENCAO: Entrega de Documentos Pendentes",
        "conteudo": "Alunos que ainda nao entregaram a documentacao de matricula (RG, CPF, historico escolar e comprovante de residencia) devem comparecer a secretaria academica ate o dia 31/01/2026 impreterivelmente. Apos essa data, a matricula sera cancelada.",
        "tipo": "URGENTE",
    },
    {
        "titulo": "📚 Abertura da Biblioteca para o Semestre 2026.1",
        "conteudo": "A biblioteca do campus retoma o pleno funcionamento a partir de 05/02/2026. Novos titulos foram adquiridos, incluindo os best-sellers de tecnologia e as obras indicadas pelos professores para o semestre. Acesse o catalogo online pelo SUAP.",
        "tipo": "INFORMATIVO",
    },
    {
        "titulo": "🏆 OBMEP 2026 - Inscricoes Abertas",
        "conteudo": "Estao abertas as inscricoes para a Olimpiada Brasileira de Matematica das Escolas Publicas (OBMEP) 2026. Alunos interessados devem procurar o Prof. de Matematica de sua turma. As provas serao realizadas em maio e agosto. Premios incluem bolsas de iniciacao cientifica.",
        "tipo": "EVENTO",
    },
    {
        "titulo": "💉 Campanha de Vacinacao - Hepatite B e HPV",
        "conteudo": "A Secretaria de Saude do RN realizara campanha de vacinacao no campus nos dias 12 e 13 de marco de 2026. Alunos entre 9 e 19 anos poderao se vacinar gratuitamente contra Hepatite B (multiplas doses) e HPV. Traga a caderneta de vacinacao.",
        "tipo": "SAUDE",
    },
    {
        "titulo": "🖥️ Laboratorios de Informatica - Normas de Uso 2026",
        "conteudo": "Lembramos as normas dos laboratorios: (1) Proibido alimentos e bebidas; (2) Uso somente para atividades pedagogicas; (3) Deixe o computador organizado ao sair; (4) Relatar problemas tecnicos ao monitor de TI; (5) Instalacao de softwares nao autorizados sujeita a suspensao.",
        "tipo": "NORMATIVO",
    },
    {
        "titulo": "🎓 Feira de Profissoes IFRN - Inscricoes para Apresentadores",
        "conteudo": "A Feira de Profissoes 2026 acontecera em 15/04/2026. Alunos do 3o Ano que desejam apresentar projetos de TCC ou trabalhos de conclusao de curso devem se inscrever ate 28/02/2026 pelo link: forms.ifrn.edu.br/feira2026. Vagas limitadas!",
        "tipo": "EVENTO",
    },
    {
        "titulo": "📝 Calendario de Provas Bimestrais - 1o Bimestre",
        "conteudo": "As provas do 1o Bimestre serao realizadas de 24/03 a 04/04/2026. O calendario completo por disciplina esta disponivel no SUAP. Alunos com necessidades especiais (atendimento diferenciado) devem confirmar com a coordenacao ate 10/03/2026.",
        "tipo": "ACADEMICO",
    },
    {
        "titulo": "🚌 Transporte Escolar - Rotas 2026",
        "conteudo": "Os horarios e rotas do transporte escolar municipal para o IFRN foram atualizados. Consulte o novo mapa de rotas na secretaria ou no site da prefeitura. Alunos que necessitam de transporte adaptado (PCD) devem entrar em contato com a assistencia estudantil.",
        "tipo": "INFORMATIVO",
    },
    {
        "titulo": "💰 Auxilio Estudantil - Resultado da Selecao",
        "conteudo": "O resultado da selecao para o Programa de Assistencia Estudantil 2026 (auxilio transporte, alimentacao e permanencia) foi divulgado no SUAP. Candidatos aprovados devem comparecer a CAEST para assinar o termo de compromisso ate 20/02/2026.",
        "tipo": "ASSISTENCIA",
    },
    {
        "titulo": "🔒 Regras de Uso do Wi-Fi do Campus",
        "conteudo": "O acesso a rede Wi-Fi do IFRN e monitorado. Eh terminantemente proibido: acesso a sites de conteudo adulto, download de torrents, uso de VPN nao autorizada e ataques a rede. O descumprimento sujeita o aluno a processo disciplinar. Login com suas credenciais do SUAP.",
        "tipo": "NORMATIVO",
    },
    {
        "titulo": "🏅 Hackathon IFRN 2026 - Tema: IA para Educacao",
        "conteudo": "O Hackathon IFRN 2026 acontecera nos dias 20 e 21 de junho com o tema 'Inteligencia Artificial para Educacao Publica'. Equipes de 3 a 5 alunos podem se inscrever. Premio: R$ 5.000 para o 1o lugar, R$ 3.000 para o 2o e R$ 1.500 para o 3o. Inscricoes: hackathon.ifrn.edu.br",
        "tipo": "EVENTO",
    },
    {
        "titulo": "📋 Entrega de Atestados Medicos",
        "conteudo": "Alunos que faltaram por motivo de saude devem entregar o atestado medico original na secretaria em ate 3 dias uteis apos o retorno. Atestados fotografados ou digitalizados nao serao aceitos. O documento justifica a falta mas nao exime o aluno das avaliacoes.",
        "tipo": "NORMATIVO",
    },
    {
        "titulo": "🌱 Semana do Meio Ambiente - Programacao",
        "conteudo": "De 01 a 05 de junho de 2026 o IFRN realiza a Semana do Meio Ambiente com palestras, oficinas e a tradicional Gincana Verde. Todas as turmas participarao de pelo menos 2 atividades. A disciplina de Biologia coordenara as acoes. Confirme com seu professor.",
        "tipo": "EVENTO",
    },
    {
        "titulo": "📊 Boletins do 1o Bimestre Disponiveis no SUAP",
        "conteudo": "Os boletins com as notas e frequencia do 1o Bimestre ja estao disponiveis para consulta no SUAP (Ensino > Meu Diario). Alunos com notas abaixo de 6,0 ou frequencia inferior a 75% devem procurar a coordenacao de curso para orientacao. Responsaveis tambem podem acessar pelo CPF do aluno.",
        "tipo": "ACADEMICO",
    },
    {
        "titulo": "🎭 Apresentacoes Culturais - Semana Junina IFRN",
        "conteudo": "A tradicional Festa Junina do IFRN acontecera no dia 26 de junho de 2026 no patio central do campus. Cada turma deve preparar uma apresentacao cultural (quadrilha, musica, teatro ou danca). Ensaios podem ser realizados nas sextas-feiras das 16h as 18h no gimnasio.",
        "tipo": "EVENTO",
    },
]

MOTIVOS_ATESTADO = [
    "Consulta medica - Clinica Geral",
    "Consulta medica - Pediatria",
    "Consulta medica - Psiquiatria",
    "Consulta medica - Neurologia",
    "Consulta odontologica - Procedimento",
    "Sindrome gripal com febre (3 dias de repouso)",
    "Gastroenterite aguda (2 dias de repouso)",
    "Crise de enxaqueca severa",
    "Procedimento cirurgico ambulatorial",
    "Internacao hospitalar",
    "Crise asmatica - atendimento emergencia",
    "Crise epileptica - observacao hospitalar",
    "Crise hipoglicemica",
    "Luxacao/entorse - fisioterapia",
    "Conjuntivite bacteriana (afastamento 3 dias)",
    "COVID-19 - isolamento preventivo",
    "Crise de ansiedade - acompanhamento psicologico",
    "Exame complementar - Raio-X/Ultrassom",
    "Tratamento fisioterapeutico continuo",
    "Acompanhamento de familiar doente (menor)",
]

NATURALIDADES_RN = [
    "Natal/RN", "Mossoro/RN", "Parnamirim/RN", "Canguaretama/RN",
    "Caico/RN", "Assu/RN", "Currais Novos/RN", "Macaiba/RN",
    "Sao Goncalo do Amarante/RN", "Ceara-Mirim/RN",
    "Nova Cruz/RN", "Santa Cruz/RN", "Pau dos Ferros/RN",
    "Joao Camara/RN", "Apodi/RN"
]


def gerar_nome(genero=None):
    if genero == "M":
        primeiro = random.choice(PRIMEIROS_NOMES_M)
    elif genero == "F":
        primeiro = random.choice(PRIMEIROS_NOMES_F)
    else:
        todos = PRIMEIROS_NOMES_M + PRIMEIROS_NOMES_F
        primeiro = random.choice(todos)
    return f"{primeiro} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"


def gerar_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"


def gerar_telefone():
    return f"(84) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"


def data_aleatoria_entre(inicio, fim):
    delta = fim - inicio
    return inicio + timedelta(days=random.randint(0, delta.days))


# ═══════════════════════════════════════════════════════════════════
# HELPERS DE CAPA
# ═══════════════════════════════════════════════════════════════════
def _get_capa_openlibrary(isbn):
    """Tenta buscar capa no Open Library pelo ISBN."""
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-L.jpg?default=false"
    try:
        res = requests.get(url, timeout=8, stream=True)
        if res.status_code == 200 and int(res.headers.get("Content-Length", 0)) > 1000:
            return url
    except Exception:
        pass
    return None


def _get_capa_google(titulo, autor):
    """Tenta buscar capa no Google Books pelo titulo/autor."""
    query = f"intitle:{titulo}"
    if autor and autor not in ("Varios Autores", "Varios"):
        query += f" inauthor:{autor}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if "items" in data:
                links = data["items"][0].get("volumeInfo", {}).get("imageLinks", {})
                img = (
                    links.get("extraLarge") or links.get("large") or
                    links.get("medium") or links.get("thumbnail") or
                    links.get("smallThumbnail")
                )
                if img:
                    return img.replace("http://", "https://").replace("&zoom=1", "&zoom=0")
    except Exception:
        pass
    return None


def _salvar_capa(livro, img_url):
    """Faz o download e salva a capa no livro."""
    try:
        res = requests.get(img_url, timeout=10)
        if res.status_code == 200 and len(res.content) > 1000:
            ext = "png" if "png" in img_url.lower() else "jpg"
            livro.capa.save(f"capa_{livro.id}.{ext}", ContentFile(res.content), save=True)
            return True
    except Exception:
        pass
    return False


def baixar_capa_livro(livro, titulo, autor, isbn, idx, total):
    """Tenta baixar a capa de um livro por OpenLibrary e depois Google Books."""
    print(f"   [{idx:03d}/{total}] {titulo[:50]:<50}", end=" -> ")

    img_url = _get_capa_openlibrary(isbn)
    fonte = "OpenLibrary"

    if not img_url:
        img_url = _get_capa_google(titulo, autor)
        fonte = "GoogleBooks"

    if img_url and _salvar_capa(livro, img_url):
        print(f"OK [{fonte}]")
        return True
    else:
        print("nao encontrada")
        return False


# ═══════════════════════════════════════════════════════════════════
# FUNCAO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
def seed():
    print("=" * 65)
    print("   SIGE - Populacao de Dados Completa (Padrao IFRN 2026)")
    print("=" * 65)

    # ── 1. GESTORES ──────────────────────────────────────────────────
    print("\n[1/11] Criando Gestores...")
    gestores_dados = [
        ("gestor_0", "diretor",      "Joao Augusto Ferreira Pinto",    "Doutorado em Administracao Publica - UFRN"),
        ("gestor_1", "vice_diretor", "Maria Claudia Santos Oliveira",  "Mestrado em Gestao Educacional - UFPB"),
        ("gestor_2", "coordenador",  "Carlos Eduardo Lima Cavalcanti", "Especialista em Coordenacao Pedagogica - IFRN"),
        ("gestor_3", "coordenador",  "Ana Paula Rocha Guedes",         "Especialista em Gestao Escolar - UFRN"),
        ("gestor_4", "secretario",   "Roberto Dantas Bezerra",         "Tecnico Administrativo em Educacao - IFRN"),
    ]
    for username, cargo, nome, _ in gestores_dados:
        u, created = User.objects.get_or_create(
            username=username, defaults={'email': f'{username}@ifrn.edu.br'}
        )
        if created:
            u.set_password('admin123')
            u.save()
        Gestor.objects.get_or_create(user=u, defaults={
            'nome_completo': nome, 'cargo': cargo,
            'cpf': gerar_cpf(), 'telefone': gerar_telefone(),
        })
    print("   [OK] 5 gestores verificados.")

    # ── 2. PROFESSORES (20) ──────────────────────────────────────────
    print("\n[2/11] Criando 20 Professores...")
    profs = []
    for i in range(20):
        username = f"prof_{i}"
        genero = "M" if i % 3 != 0 else "F"
        u, created = User.objects.get_or_create(
            username=username, defaults={'email': f'{username}@ifrn.edu.br'}
        )
        if created:
            u.set_password('admin123')
            u.save()
        p, _ = Professor.objects.get_or_create(user=u, defaults={
            'nome_completo': gerar_nome(genero),
            'formacao': FORMACOES_PROF[i % len(FORMACOES_PROF)],
            'cpf': gerar_cpf(),
            'telefone': gerar_telefone(),
        })
        profs.append(p)
    print("   [OK] 20 professores verificados.")

    # ── 3. TURMAS (6 turmas: 1o, 2o, 3o Ano - manha e tarde) ────────
    print("\n[3/11] Criando 6 Turmas...")
    turmas = []
    config_turmas = [
        ("1o Ano INFO - Manha",  2026, "manha"),
        ("1o Ano INFO - Tarde",  2026, "tarde"),
        ("2o Ano INFO - Manha",  2026, "manha"),
        ("2o Ano INFO - Tarde",  2026, "tarde"),
        ("3o Ano INFO - Manha",  2026, "manha"),
        ("3o Ano INFO - Tarde",  2026, "tarde"),
    ]
    for nome_t, ano_t, turno_t in config_turmas:
        t, _ = Turma.objects.get_or_create(
            nome=nome_t, defaults={'ano': ano_t, 'turno': turno_t}
        )
        turmas.append(t)
    print("   [OK] 6 turmas verificadas.")

    # ── 4. DISCIPLINAS (40) ──────────────────────────────────────────
    print("\n[4/11] Criando 40 Disciplinas com Planejamentos e Atividades...")
    disciplinas_objs = []
    horarios_possiveis = [
        "07:00 - 08:40", "08:40 - 10:20", "10:30 - 12:10",
        "13:00 - 14:40", "14:40 - 16:20", "16:30 - 18:10",
    ]
    tipos_atividade = ['ATIVIDADE', 'TRABALHO', 'PROVA', 'TRABALHO', 'ATIVIDADE']

    for i, nome_mat in enumerate(MATERIAS):
        turma = turmas[i % len(turmas)]
        prof = profs[i % len(profs)]

        disc, _ = Disciplina.objects.get_or_create(
            nome=nome_mat, turma=turma, defaults={'professor': prof}
        )
        disciplinas_objs.append(disc)

        for d in range(1, 7):
            try:
                PlanejamentoAula.objects.get_or_create(
                    disciplina=disc,
                    data_aula=date(2026, 2, 1) + timedelta(weeks=d * 3),
                    horario_aula=horarios_possiveis[d % len(horarios_possiveis)],
                    defaults={
                        'professor': prof,
                        'turma': turma,
                        'conteudo': (
                            f"Unidade {d} - {nome_mat}\n"
                            f"Objetivo: {['Introducao', 'Desenvolvimento', 'Aprofundamento', 'Revisao', 'Consolidacao', 'Avaliacao'][d-1]} do conteudo.\n"
                            f"Metodologia: {'Aula expositiva dialogada, resolucao de problemas em duplas.' if d % 2 == 0 else 'Flipped classroom com video-aulas previas e discussao em sala.'}\n"
                            f"Recursos: Quadro branco, datashow, slides em PDF, kahoot de fixacao.\n"
                            f"Avaliacao: {'Exercicios de fixacao' if d < 4 else 'Producao de projeto pratico'}."
                        ),
                        'status': 'NORMAL',
                        'concluido': d <= 3,
                    }
                )
            except Exception:
                pass

        for a in range(1, 6):
            tipo = tipos_atividade[a - 1]
            data_ativ = date(2026, 2, 1) + timedelta(days=a * 20)
            AtividadeProfessor.objects.get_or_create(
                disciplina=disc,
                titulo=f"{tipo} {a} - {nome_mat}",
                defaults={
                    'tipo': tipo,
                    'data': data_ativ,
                    'descricao': (
                        f"{'Lista de exercicios com 10 questoes sobre' if tipo == 'ATIVIDADE' else 'Desenvolvimento de' if tipo == 'TRABALHO' else 'Avaliacao formal de'} "
                        f"{nome_mat} - Unidade {a}. "
                        f"{'Entregar via SUAP ate as 23:59 do dia.' if tipo != 'PROVA' else 'Presencial, sem consulta, duracao de 100 minutos.'}"
                    ),
                }
            )

    print(f"   [OK] {len(MATERIAS)} disciplinas verificadas.")

    # ── 5. BIBLIOTECA (100 Best Sellers) + CAPAS ────────────────────
    print("\n[5/11] Populando Biblioteca com 100 Best Sellers e baixando capas...")
    print("        (OpenLibrary -> Google Books como fallback)\n")
    livros_objs = []
    total_livros = len(LIVROS_BESTSELLERS)
    capas_ok = 0

    for idx, (titulo, autor, isbn) in enumerate(LIVROS_BESTSELLERS, 1):
        livro, criado = Livro.objects.get_or_create(
            isbn=isbn,
            defaults={
                'titulo': titulo,
                'autor': autor,
                'quantidade_total': random.randint(2, 8),
            }
        )
        livros_objs.append(livro)

        # Baixa a capa para todos os livros (force = sempre)
        if baixar_capa_livro(livro, titulo, autor, isbn, idx, total_livros):
            capas_ok += 1

        time.sleep(0.4)  # Delay amigavel para as APIs

    print(f"\n   [OK] {total_livros} livros verificados. Capas baixadas: {capas_ok}/{total_livros}.")

    # ── 6. MATERIAIS DIDATICOS ───────────────────────────────────────
    print("\n[6/11] Vinculando Materiais Didaticos (links + livros)...")
    link_idx = 0
    for disc in disciplinas_objs:
        link_nome, link_url = LINKS_MATERIAIS[link_idx % len(LINKS_MATERIAIS)]
        MaterialDidatico.objects.get_or_create(
            disciplina=disc,
            titulo=f"[LINK] {link_nome}",
            defaults={
                'tipo': 'LINK',
                'url': link_url,
                'descricao': f'Material digital de apoio para {disc.nome}. Acesse pelo navegador ou pelo SUAP.',
            }
        )
        link_idx += 1

        livro_base = livros_objs[link_idx % len(livros_objs)]
        MaterialDidatico.objects.get_or_create(
            disciplina=disc,
            titulo=f"[LIVRO] {livro_base.titulo}",
            defaults={
                'tipo': 'LIVRO',
                'livro': livro_base,
                'descricao': f'Obra de referencia para {disc.nome}. Disponivel para retirada na biblioteca do campus.',
            }
        )

        MaterialDidatico.objects.get_or_create(
            disciplina=disc,
            titulo=f"[SLIDE] Slides - {disc.nome}",
            defaults={
                'tipo': 'LINK',
                'url': f"https://drive.google.com/drive/folders/ifrn_{disc.id}",
                'descricao': f'Slides das aulas de {disc.nome} - compartilhados pelo professor via Google Drive.',
            }
        )
    print("   [OK] Materiais didaticos vinculados (3 por disciplina).")

    # ── 7. CALENDARIO ACADEMICO 2026 ─────────────────────────────────
    print("\n[7/11] Criando Calendario Academico 2026...")
    if EventoCalendario:
        eventos_calendario = [
            ("Inicio do Ano Letivo 2026", date(2026, 2, 2), "DI_LETIVO", "Acolhida dos calouros e retorno dos veteranos."),
            ("Recesso de Carnaval", date(2026, 3, 2), "RECESSO", "Recesso de Carnaval."),
            ("Feriado Tiradentes", date(2026, 4, 21), "FERIADO", "Feriado Nacional."),
            ("Semana de Provas 1o Bimestre", date(2026, 4, 1), "PROVA", "Avaliacoes do primeiro bimestre."),
        ]
        for nome_ev, dt, tipo_ev, descricao_ev in eventos_calendario:
            EventoCalendario.objects.get_or_create(
                data=dt,
                defaults={
                    'tipo': tipo_ev,
                    'descricao': f"{nome_ev}: {descricao_ev}",
                }
            )
        print(f"   [OK] Eventos no calendario academico.")

    # ── 8. MURAL DE AVISOS ───────────────────────────────────────────
    print("\n[8/11] Populando Mural de Avisos...")
    if Comunicado:
        for av in AVISOS_MURAL:
            Comunicado.objects.get_or_create(
                titulo=av['titulo'],
                defaults={
                    'conteudo': av['conteudo'],
                    'importancia': 'ALTA' if av.get('tipo') == 'URGENTE' else 'NORMAL',
                    'data_publicacao': timezone.now(),
                }
            )
        print(f"   [OK] Comunicados no mural.")

    # ── 9. ATESTADOS DE PROFESSORES ──────────────────────────────────
    print("\n[9/11] Gerando Atestados Medicos de Professores...")
    if AtestadoMedico:
        profs_com_atestado = random.sample(profs, min(8, len(profs)))
        for prof in profs_com_atestado:
            num_atestados = random.randint(1, 2)
            for _ in range(num_atestados):
                data_atestado = data_aleatoria_entre(date(2026, 2, 2), date(2026, 11, 30))
                dias = random.randint(1, 5)
                AtestadoMedico.objects.get_or_create(
                    usuario=prof.user,
                    data_inicio=data_atestado,
                    defaults={
                        'data_fim': data_atestado + timedelta(days=dias),
                        'descricao': f"Motivo: {random.choice(MOTIVOS_ATESTADO)}. CRM validado.",
                        'status': 'APROVADO',
                        'arquivo': 'saude/atestados/dummy.pdf'
                    }
                )
        print(f"   [OK] Atestados de professores gerados.")
    else:
        print("   ⚠ Modelo AtestadoMedico nao encontrado. Pulando.")

    # ── 10. ALUNOS (100) ─────────────────────────────────────────────
    print("\n[10/11] Criando 100 Alunos com Saude, Frequencia, Notas e Faturas...")
    print("         Aguarde - este processo pode demorar alguns minutos...")

    nomes_usados = set()
    alunos_criados = []

    for i in range(100):
        username = f"aluno_{i}"
        genero = "F" if i % 3 == 0 else "M"
        u, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@estudante.ifrn.br'}
        )
        if created:
            u.set_password('admin123')
            u.save()

        nome = gerar_nome(genero)
        tentativas = 0
        while nome in nomes_usados and tentativas < 20:
            nome = gerar_nome(genero)
            tentativas += 1
        nomes_usados.add(nome)

        turma_aluno = turmas[i % len(turmas)]
        data_nasc = date(2006, random.randint(1, 12), random.randint(1, 28))

        aluno, _ = Aluno.objects.get_or_create(
            user=u,
            defaults={
                'nome_completo': nome,
                'turma': turma_aluno,
                'cpf': gerar_cpf(),
                'naturalidade': random.choice(NATURALIDADES_RN),
                'telefone': gerar_telefone(),
            }
        )
        alunos_criados.append(aluno)

        if i < 15:
            perfil = PERFIS_PCD[i % len(PERFIS_PCD)]
            detalhes_pcd, pne, desc_pne = perfil
            aluno.possui_necessidade_especial = pne
            aluno.descricao_necessidade = desc_pne
            aluno.save()
            FichaMedica.objects.update_or_create(aluno=aluno, defaults={
                'tipo_sanguineo': random.choice(TIPOS_SANGUINEOS),
                'alergias': "Nenhuma conhecida",
                'medicamentos_continuos': random.choice(MEDICAMENTOS[:8]),
                'condicoes_pcd': True,
                'detalhes_pcd': detalhes_pcd,
                'contato_emergencia_nome': f"Responsavel de {nome.split()[0]}",
                'contato_emergencia_fone': gerar_telefone(),
                'observacoes_medicas': f"Laudo arquivado na secretaria. {desc_pne}",
            })
        elif i < 25:
            perfil = PERFIS_PCD[i % len(PERFIS_PCD)]
            detalhes_pcd, pne, desc_pne = perfil
            alergia1 = random.choice(ALERGIAS)
            alergia2 = random.choice([a for a in ALERGIAS if a != alergia1])
            aluno.possui_necessidade_especial = pne
            aluno.descricao_necessidade = desc_pne
            aluno.save()
            FichaMedica.objects.update_or_create(aluno=aluno, defaults={
                'tipo_sanguineo': random.choice(TIPOS_SANGUINEOS),
                'alergias': f"{alergia1}, {alergia2}",
                'medicamentos_continuos': f"{random.choice(MEDICAMENTOS)} | Anti-histaminico: Loratadina 10mg",
                'condicoes_pcd': True,
                'detalhes_pcd': detalhes_pcd,
                'contato_emergencia_nome': f"Responsavel de {nome.split()[0]}",
                'contato_emergencia_fone': gerar_telefone(),
                'observacoes_medicas': f"PCD com alergia declarada. {desc_pne} Epineta disponivel na enfermaria.",
            })
        elif i < 35:
            alergia = random.choice(ALERGIAS)
            medicamento = random.choice([
                "Loratadina 10mg - 1x ao dia",
                "Desloratadina 5mg - 1x ao dia",
                "Cetirizina 10mg - 1x ao dia (noite)",
                "Fexofenadina 180mg - 1x ao dia",
                "Nenhum medicamento continuo - manejo ambiental",
            ])
            FichaMedica.objects.update_or_create(aluno=aluno, defaults={
                'tipo_sanguineo': random.choice(TIPOS_SANGUINEOS),
                'alergias': alergia,
                'medicamentos_continuos': medicamento,
                'condicoes_pcd': False,
                'detalhes_pcd': "",
                'contato_emergencia_nome': f"Responsavel de {nome.split()[0]}",
                'contato_emergencia_fone': gerar_telefone(),
                'observacoes_medicas': f"Alergia a {alergia}. {random.choice(['Epineta disponivel na enfermaria.', 'Aluno orientado sobre reacoes alergicas.', 'Professores notificados.'])}",
            })
        elif i < 50:
            doenca = random.choice([d for d in DOENCAS_COMUNS if d])
            medicamento = random.choice(MEDICAMENTOS[8:])
            FichaMedica.objects.update_or_create(aluno=aluno, defaults={
                'tipo_sanguineo': random.choice(TIPOS_SANGUINEOS),
                'alergias': random.choice(["Nenhuma conhecida", "Nenhuma conhecida", random.choice(ALERGIAS)]),
                'medicamentos_continuos': medicamento,
                'condicoes_pcd': False,
                'detalhes_pcd': "",
                'contato_emergencia_nome': f"Responsavel de {nome.split()[0]}",
                'contato_emergencia_fone': gerar_telefone(),
                'observacoes_medicas': f"Diagnostico: {doenca}. Medicacao disponivel na enfermaria se necessario.",
            })
        else:
            FichaMedica.objects.update_or_create(aluno=aluno, defaults={
                'tipo_sanguineo': random.choice(TIPOS_SANGUINEOS),
                'alergias': "Nenhuma conhecida",
                'medicamentos_continuos': "",
                'condicoes_pcd': False,
                'detalhes_pcd': "",
                'contato_emergencia_nome': f"Responsavel de {nome.split()[0]}",
                'contato_emergencia_fone': gerar_telefone(),
                'observacoes_medicas': "",
            })

        if AtestadoMedico and i % 5 == 0:
            num_atestados = random.randint(1, 2)
            for _ in range(num_atestados):
                data_at = data_aleatoria_entre(date(2026, 2, 5), date(2026, 11, 20))
                dias_at = random.randint(1, 3)
                try:
                    AtestadoMedico.objects.get_or_create(
                        usuario=aluno.user,
                        data_inicio=data_at,
                        defaults={
                            'data_fim': data_at + timedelta(days=dias_at),
                            'descricao': f"Atestado Aluno: {random.choice(MOTIVOS_ATESTADO)}",
                            'status': 'APROVADO',
                            'arquivo': 'saude/atestados/dummy.pdf'
                        }
                    )
                except Exception:
                    pass

        if Frequencia:
            disc_turma = [d for d in disciplinas_objs if d.turma == turma_aluno]
            for disc in disc_turma[:8]:
                for semana in range(1, 5):
                    data_freq = date(2026, 2, 2) + timedelta(weeks=semana * 6)
                    presente = random.random() > 0.1
                    try:
                        Frequencia.objects.get_or_create(
                            aluno=aluno,
                            disciplina=disc,
                            data=data_freq,
                            defaults={'presente': presente, 'justificada': not presente and random.random() > 0.5}
                        )
                    except Exception:
                        pass

        if Nota:
            disc_turma = [d for d in disciplinas_objs if d.turma == turma_aluno]
            for disc in disc_turma[:8]:
                try:
                    Nota.objects.get_or_create(
                        aluno=aluno,
                        disciplina=disc,
                        defaults={
                            'nota1': Decimal(str(round(random.uniform(5, 10), 1))),
                            'nota2': Decimal(str(round(random.uniform(5, 10), 1))),
                            'nota3': Decimal(str(round(random.uniform(5, 10), 1))),
                            'nota4': Decimal(str(round(random.uniform(5, 10), 1))),
                        }
                    )
                except Exception:
                    pass

        Fatura.objects.get_or_create(
            aluno=aluno,
            descricao="Mensalidade Marco 2026",
            defaults={
                'valor': Decimal('350.00'),
                'data_vencimento': date(2026, 3, 10),
                'status': random.choice(['PENDENTE', 'PAGO', 'PAGO']),
            }
        )
        if i % 4 == 0:
            Fatura.objects.get_or_create(
                aluno=aluno,
                descricao="Taxa de Material Didatico (Atrasada)",
                defaults={
                    'valor': Decimal('120.00'),
                    'data_vencimento': date(2026, 1, 15),
                    'status': 'PENDENTE',
                }
            )

    print(f"   [OK] 100 alunos verificados.")

    # ── 11. GRADE DE HORARIOS ────────────────────────────────────────
    print("\n[11/11] Criando Grade de Horarios...")
    dias_semana_map = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
    horarios_manha = ["07:00 - 07:50", "07:50 - 08:40", "08:50 - 09:40", "09:40 - 10:30", "10:40 - 11:30"]

    if GradeHorario:
        for turma in turmas:
            disc_turma = [d for d in disciplinas_objs if d.turma == turma]
            for j, disc in enumerate(disc_turma[:10]):
                try:
                    GradeHorario.objects.get_or_create(
                        turma=turma,
                        disciplina=disc,
                        dia=dias_semana_map[j % len(dias_semana_map)],
                        defaults={'horario': horarios_manha[j % len(horarios_manha)]}
                    )
                except Exception:
                    pass
        print("   [OK] Grade de horarios criada.")
    else:
        print("   ⚠ Modelo GradeHorario nao encontrado. Pulando.")

    # ── RESUMO FINAL ──────────────────────────────────────────────────
    from apps.saude.models import FichaMedica as FM
    print("\n" + "=" * 65)
    print("   POPULACAO CONCLUIDA COM SUCESSO!")
    print("=" * 65)
    print(f"  Gestores:              {Gestor.objects.count()}")
    print(f"  Professores:           {Professor.objects.count()}")
    print(f"  Turmas:                {Turma.objects.count()}")
    print(f"  Disciplinas:           {Disciplina.objects.count()}")
    print(f"  Planejamentos de Aula: {PlanejamentoAula.objects.count()}")
    print(f"  Atividades/Provas:     {AtividadeProfessor.objects.count()}")
    print(f"  Livros (Best Sellers): {Livro.objects.count()}")
    print(f"  Materiais Didaticos:   {MaterialDidatico.objects.count()}")
    print(f"  Alunos (total):        {Aluno.objects.count()}")
    print(f"    |-- Com PCD:          {FM.objects.filter(condicoes_pcd=True).count()}")
    print(f"    |-- PCD + Alergia:    {FM.objects.filter(condicoes_pcd=True).exclude(alergias='Nenhuma conhecida').count()}")
    print(f"    |-- So Alergia:       {FM.objects.filter(condicoes_pcd=False).exclude(alergias='Nenhuma conhecida').exclude(alergias='').count()}")
    print(f"    \-- Sem condicoes:    {FM.objects.filter(condicoes_pcd=False, alergias='Nenhuma conhecida').count()}")
    print(f"  Faturas:               {Fatura.objects.count()}")

    if EventoCalendario:
        print(f"  Eventos no Calendario: {EventoCalendario.objects.count()}")
    if Comunicado:
        print(f"  Comunicados:           {Comunicado.objects.count()}")
    if Frequencia:
        print(f"  Registros Frequencia:  {Frequencia.objects.count()}")
    if Nota:
        print(f"  Registros de Notas:    {Nota.objects.count()}")

    print("-" * 65)
    print("  Credenciais de acesso (senha padrao): admin123")
    print("  Usuarios de exemplo:")
    print("    Alunos:      aluno_0  ate aluno_99")
    print("    Professores: prof_0   ate prof_19")
    print("    Gestores:    gestor_0 ate gestor_4")
    print("=" * 65)


if __name__ == "__main__":
    seed()