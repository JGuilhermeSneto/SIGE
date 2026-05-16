from django.test import TestCase
from apps.academico.utils.academico import (
    _calcular_situacao_nota,
    _formatar_nota,
    _get_turno_key,
    _get_grade_horario_turma,
    _get_ocupados_por_professor,
)
from apps.academico.models import Turma, Disciplina, GradeHorario
from apps.usuarios.models.perfis import Professor
from django.contrib.auth import get_user_model

User = get_user_model()


class AcademicoUtilsTest(TestCase):
    def test_calcular_situacao_nota(self):
        res = _calcular_situacao_nota(8.0, 80.0)
        self.assertEqual(res["texto"], "Aprovado")
        res = _calcular_situacao_nota(6.0, 80.0)
        self.assertEqual(res["texto"], "Recuperação")
        res = _calcular_situacao_nota(4.0, 80.0)
        self.assertEqual(res["texto"], "Reprovado")
        res = _calcular_situacao_nota(9.0, 70.0)
        self.assertEqual(res["texto"], "Reprovado por Falta")

    def test_formatar_nota(self):
        self.assertEqual(_formatar_nota(8.5)["valor"], "8.5")
        self.assertEqual(_formatar_nota(8.5)["classe"], "text-success fw-bold")
        self.assertEqual(_formatar_nota(6.0)["classe"], "text-warning fw-bold")
        self.assertEqual(_formatar_nota(4.0)["classe"], "text-danger fw-bold")
        self.assertEqual(_formatar_nota(None)["valor"], "-")
        self.assertEqual(_formatar_nota("invalido")["valor"], "-")

    def test_get_turno_key(self):
        self.assertEqual(_get_turno_key("Manhã"), "manha")
        self.assertEqual(_get_turno_key("Tarde"), "tarde")
        self.assertEqual(_get_turno_key(None), "")

    def test_get_grade_horario_turma(self):
        turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)
        disc = Disciplina.objects.create(nome="Matemática", turma=turma)
        GradeHorario.objects.create(
            turma=turma, disciplina=disc, dia="segunda", horario="07:45 às 08:30"
        )

        grade = _get_grade_horario_turma(turma)
        self.assertIsNotNone(grade)
        self.assertEqual(grade["08:00"]["segunda"], "Matemática")

    def test_get_ocupados_por_professor(self):
        user = User.objects.create_user(username="prof1", password="pw")
        prof = Professor.objects.create(
            user=user, nome_completo="Prof", cpf="1", data_nascimento="1980-01-01"
        )
        turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)
        disc = Disciplina.objects.create(nome="Mat", turma=turma, professor=prof)
        GradeHorario.objects.create(
            turma=turma, disciplina=disc, dia="segunda", horario="07:45 às 08:30"
        )

        ocupados = _get_ocupados_por_professor(prof.id, 2024)
        # 08:00 é o primeiro horário da manhã em constantes.py
        # Vamos verificar se "segunda-0" está no set
        self.assertTrue(any("segunda" in o for o in ocupados))
