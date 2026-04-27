from django.db import transaction
from ..models.academico import Turma, Disciplina, GradeHorario
from apps.usuarios.models.perfis import Professor

class AcademicoService:
    @staticmethod
    @transaction.atomic
    def criar_turma_com_disciplinas(nome, ano, turno, disciplinas_data=None):
        """
        Cria uma turma e opcionalmente vincula disciplinas iniciais.
        Exemplo de lógica de negócio complexa movida para serviço.
        """
        turma = Turma.objects.create(nome=nome, ano=ano, turno=turno)
        
        if disciplinas_data:
            for d in disciplinas_data:
                Disciplina.objects.create(
                    nome=d['nome'],
                    turma=turma,
                    professor_id=d.get('professor_id'),
                    carga_horaria=d.get('carga_horaria', 40)
                )
        return turma

    @staticmethod
    @transaction.atomic
    def atualizar_grade_horaria(turma, grade_data):
        """
        Atualiza toda a grade horária de uma turma de forma atômica.
        """
        GradeHorario.objects.filter(turma=turma).delete()
        novas_entradas = []
        for entrada in grade_data:
            novas_entradas.append(GradeHorario(
                turma=turma,
                disciplina_id=entrada['disciplina_id'],
                dia=entrada['dia'],
                horario=entrada['horario']
            ))
        GradeHorario.objects.bulk_create(novas_entradas)
        return True

    @staticmethod
    def calcular_situacao_aluno(media_final, frequencia_percentual):
        """
        Define a situação acadêmica do aluno (Lógica de Negócio Centralizada).
        """
        MEDIA_APROVACAO = 7.0
        MEDIA_RECUPERACAO = 5.0
        FREQUENCIA_MINIMA = 75.0

        if frequencia_percentual < FREQUENCIA_MINIMA:
            return {"texto": "Reprovado por Falta", "classe": "badge bg-danger", "aprovado": False}
        
        if media_final >= MEDIA_APROVACAO:
            return {"texto": "Aprovado", "classe": "badge bg-success", "aprovado": True}
        
        if media_final >= MEDIA_RECUPERACAO:
            return {"texto": "Recuperação", "classe": "badge bg-warning text-dark", "aprovado": False}
            
        return {"texto": "Reprovado", "classe": "badge bg-danger", "aprovado": False}
