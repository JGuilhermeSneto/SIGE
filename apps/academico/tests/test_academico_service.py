from django.test import TestCase
from apps.academico.models.academico import Turma, Disciplina, GradeHorario
from apps.academico.services.academico_service import AcademicoService
from apps.usuarios.models.perfis import Professor
from django.contrib.auth import get_user_model

User = get_user_model()

class AcademicoServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="prof1", password="password")
        self.professor = Professor.objects.create(
            user=self.user, nome_completo="Professor 1", cpf="123.456.789-00", data_nascimento="1980-01-01"
        )

    def test_criar_turma_com_disciplinas(self):
        disciplinas_data = [
            {'nome': 'Matemática', 'professor_id': self.professor.id, 'carga_horaria': 60},
            {'nome': 'Português', 'carga_horaria': 40},
        ]
        turma = AcademicoService.criar_turma_com_disciplinas(
            nome="2A", ano=2024, turno="manha", disciplinas_data=disciplinas_data
        )
        
        self.assertEqual(Turma.objects.count(), 1)
        self.assertEqual(Disciplina.objects.filter(turma=turma).count(), 2)
        self.assertEqual(Disciplina.objects.get(nome='Matemática').professor, self.professor)

    def test_atualizar_grade_horaria(self):
        turma = Turma.objects.create(nome="2A", ano=2024, turno="manha")
        disc = Disciplina.objects.create(nome="Matemática", turma=turma, carga_horaria=60)
        
        grade_data = [
            {'disciplina_id': disc.id, 'dia': 'SEG', 'horario': '08:00'},
            {'disciplina_id': disc.id, 'dia': 'TER', 'horario': '09:00'},
        ]
        
        result = AcademicoService.atualizar_grade_horaria(turma, grade_data)
        self.assertTrue(result)
        self.assertEqual(GradeHorario.objects.filter(turma=turma).count(), 2)

    def test_calcular_situacao_aluno(self):
        # Aprovado
        self.assertEqual(AcademicoService.calcular_situacao_aluno(7.5, 80)['texto'], "Aprovado")
        # Recuperação
        self.assertEqual(AcademicoService.calcular_situacao_aluno(6.0, 80)['texto'], "Recuperação")
        # Reprovado por média
        self.assertEqual(AcademicoService.calcular_situacao_aluno(4.0, 80)['texto'], "Reprovado")
        # Reprovado por falta
        self.assertEqual(AcademicoService.calcular_situacao_aluno(9.0, 70)['texto'], "Reprovado por Falta")
