import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = [r[0] for r in cur.fetchall()]
print(f"Total de tabelas no SQLite: {len(tables)}\n")

target = [
    ('core_professor', 'Professores'),
    ('core_aluno', 'Alunos'),
    ('core_gestor', 'Gestores'),
    ('core_turma', 'Turmas'),
    ('core_disciplina', 'Disciplinas'),
    ('core_gradehorario', 'Grade Horária'),
    ('biblioteca_livro', 'Livros (Acervo)'),
    ('biblioteca_emprestimo', 'Empréstimos'),
    ('infraestrutura_unidadeescolar', 'Unidades Escolares'),
    ('infra_ambiente', 'Salas/Ambientes'),
    ('infra_patrimonio', 'Patrimônio'),
    ('fin_fatura', 'Faturas Financeiras'),
    ('ia_sessaoassistente', 'Sessões ELISE IA'),
    ('ia_mensagemassistente', 'Mensagens ELISE IA'),
    ('ia_propostadecisao', 'Propostas Decisão (HITL)'),
]

for t, label in target:
    if t in tables:
        cur.execute(f"SELECT count(*) FROM {t};")
        c = cur.fetchone()[0]
        print(f"  {t} ({label}): {c} registros")
    else:
        print(f"  {t} ({label}): NAO EXISTE")

conn.close()
