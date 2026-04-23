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
