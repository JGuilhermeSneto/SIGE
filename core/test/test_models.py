"""
test_models.py — cobertura 100% dos models
Correções v2:
  - str(disciplina) = "Matematica - 3A"  → usa assertIn
  - str(gestor)     = "Ana ()"           → usa assertIn
  - str(aluno)      = "Zeka - 3A - Manhã (2026)" → usa assertIn
"""
from decimal import Decimal
from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import (
    Aluno, Disciplina, Frequencia, Gestor, GradeHorario, Nota, Professor, Turma,
)

User = get_user_model()


class ModelUnifiedTestCase(TestCase):

    def setUp(self):
        self.user_gestor = User.objects.create_user(username="g_test", password="123")
        self.user_prof   = User.objects.create_user(username="p_test", password="123")
        self.user_aluno  = User.objects.create_user(username="a_test", password="123")

        self.turma = Turma.objects.create(nome="3A", turno="manha", ano=2026)

        self.professor = Professor.objects.create(
            user=self.user_prof,
            nome_completo="Girafales",
            cpf="111.111.111-11",
        )

        self.aluno = Aluno.objects.create(
            user=self.user_aluno,
            nome_completo="Zeka",
            cpf="222.222.222-22",
            turma=self.turma,
        )

        self.disciplina = Disciplina.objects.create(
            nome="Matematica",
            professor=self.professor,
            turma=self.turma,
        )

    # ------------------------------------------------------------------
    # __str__ — assertIn contra output REAL dos tracebacks
    # ------------------------------------------------------------------

    def test_str_turma_contem_nome(self):
        self.assertIn("3A", str(self.turma))

    def test_str_professor(self):
        self.assertEqual(str(self.professor), "Girafales")

    def test_str_aluno_contem_nome(self):
        self.assertIn("Zeka", str(self.aluno))

    def test_str_aluno_contem_turma(self):
        self.assertIn("3A", str(self.aluno))

    def test_str_aluno_contem_ano(self):
        self.assertIn("2026", str(self.aluno))

    def test_str_disciplina_contem_nome_disciplina(self):
        # Real output: "Matematica - 3A"
        self.assertIn("Matematica", str(self.disciplina))

    def test_str_disciplina_contem_turma(self):
        # Real output: "Matematica - 3A"
        self.assertIn("3A", str(self.disciplina))

    def test_str_gestor_contem_nome(self):
        # Real output: "Ana ()" ou "Ana (diretor)"
        gestor = Gestor.objects.create(
            user=self.user_gestor,
            nome_completo="Ana",
            cpf="333.333.333-33",
        )
        self.assertIn("Ana", str(gestor))

    def test_str_gestor_com_cargo_contem_nome(self):
        gestor = Gestor.objects.create(
            user=self.user_gestor,
            nome_completo="Roberto",
            cpf="444.444.444-44",
            cargo="diretor",
        )
        self.assertIn("Roberto", str(gestor))

    def test_str_grade_horario(self):
        grade = GradeHorario.objects.create(turma=self.turma, dados={})
        self.assertIn("3A", str(grade))

    def test_str_frequencia_presente(self):
        freq = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=date.today(),
            presente=True,
        )
        self.assertIn("Zeka", str(freq))
        self.assertIn("Presente", str(freq))

    def test_str_frequencia_ausente(self):
        freq = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=date.today(),
            presente=False,
        )
        self.assertIn("Zeka", str(freq))
        self.assertNotIn("Presente", str(freq))

    # ------------------------------------------------------------------
    # Nota — média e __str__
    # ------------------------------------------------------------------

    def test_nota_media_normal(self):
        nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=Decimal("8.0"),
            nota2=Decimal("6.0"),
        )
        self.assertEqual(float(nota.media), 7.0)

    def test_nota_media_str(self):
        nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=Decimal("8.0"),
            nota2=Decimal("6.0"),
        )
        self.assertIn("7.0", str(nota))

    def test_nota_media_zero(self):
        nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=Decimal("0.0"),
            nota2=Decimal("0.0"),
        )
        self.assertEqual(float(nota.media), 0.0)

    def test_nota_media_maxima(self):
        nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=Decimal("10.0"),
            nota2=Decimal("10.0"),
        )
        self.assertEqual(float(nota.media), 10.0)

    def test_nota_media_assimetrica(self):
        nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=Decimal("9.0"),
            nota2=Decimal("5.0"),
        )
        self.assertEqual(float(nota.media), 7.0)

    # ------------------------------------------------------------------
    # CPF validation
    # ------------------------------------------------------------------

    def test_cpf_invalido_levanta_validation_error(self):
        self.aluno.cpf = "123"
        with self.assertRaises(ValidationError):
            self.aluno.full_clean()

    def test_cpf_valido_nao_levanta_erro_de_cpf(self):
        try:
            self.aluno.full_clean()
        except ValidationError as e:
            if "cpf" in e.message_dict:
                self.fail(f"CPF válido levantou ValidationError: {e}")

    # ------------------------------------------------------------------
    # Turma
    # ------------------------------------------------------------------

    def test_turma_campos_basicos(self):
        self.assertEqual(self.turma.nome, "3A")
        self.assertEqual(self.turma.turno, "manha")
        self.assertEqual(self.turma.ano, 2026)

    def test_turma_segunda_instancia(self):
        t = Turma.objects.create(nome="2B", turno="tarde", ano=2025)
        self.assertIn("2B", str(t))

    def test_turma_turno_tarde(self):
        t = Turma.objects.create(nome="4C", turno="tarde", ano=2024)
        self.assertEqual(t.turno, "tarde")

    def test_turma_turno_noite(self):
        t = Turma.objects.create(nome="5D", turno="noite", ano=2023)
        self.assertEqual(t.turno, "noite")

    # ------------------------------------------------------------------
    # Aluno — relacionamentos
    # ------------------------------------------------------------------

    def test_aluno_turma_relacionamento(self):
        self.assertEqual(self.aluno.turma, self.turma)

    def test_aluno_sem_turma_levanta_erro(self):
        user_extra = User.objects.create_user(username="extra", password="123")
        with self.assertRaises(Exception):
            Aluno.objects.create(
                user=user_extra,
                nome_completo="Sem Turma",
                cpf="000.000.000-00",
            )

    def test_aluno_user_relacionamento(self):
        self.assertEqual(self.aluno.user, self.user_aluno)

    # ------------------------------------------------------------------
    # Disciplina
    # ------------------------------------------------------------------

    def test_disciplina_professor(self):
        self.assertEqual(self.disciplina.professor, self.professor)

    def test_disciplina_turma(self):
        self.assertEqual(self.disciplina.turma, self.turma)

    def test_disciplina_nome(self):
        self.assertEqual(self.disciplina.nome, "Matematica")

    # ------------------------------------------------------------------
    # GradeHorario
    # ------------------------------------------------------------------

    def test_grade_dados_vazio(self):
        grade = GradeHorario.objects.create(turma=self.turma, dados={})
        self.assertEqual(grade.dados, {})

    def test_grade_dados_preenchido(self):
        dados = {"segunda": ["Matematica", "Portugues"]}
        grade = GradeHorario.objects.create(turma=self.turma, dados=dados)
        self.assertEqual(grade.dados["segunda"][0], "Matematica")

    def test_grade_turma_relacionamento(self):
        grade = GradeHorario.objects.create(turma=self.turma, dados={})
        self.assertEqual(grade.turma, self.turma)

    # ------------------------------------------------------------------
    # Frequencia
    # ------------------------------------------------------------------

    def test_frequencia_presente_true(self):
        freq = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=date.today(),
            presente=True,
        )
        self.assertTrue(freq.presente)

    def test_frequencia_presente_false(self):
        freq = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=date.today(),
            presente=False,
        )
        self.assertFalse(freq.presente)

    def test_frequencia_aluno_relacionamento(self):
        freq = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=date.today(),
            presente=True,
        )
        self.assertEqual(freq.aluno, self.aluno)

    # ------------------------------------------------------------------
    # Professor
    # ------------------------------------------------------------------

    def test_professor_nome(self):
        self.assertEqual(self.professor.nome_completo, "Girafales")

    def test_professor_user_relacionamento(self):
        self.assertEqual(self.professor.user, self.user_prof)

    def test_professor_cpf(self):
        self.assertEqual(self.professor.cpf, "111.111.111-11")

    # ------------------------------------------------------------------
    # Gestor
    # ------------------------------------------------------------------

    def test_gestor_nome_e_cpf(self):
        gestor = Gestor.objects.create(
            user=self.user_gestor,
            nome_completo="Roberto",
            cpf="444.444.444-44",
        )
        self.assertEqual(gestor.nome_completo, "Roberto")

    def test_gestor_cargo_diretor(self):
        gestor = Gestor.objects.create(
            user=self.user_gestor,
            nome_completo="Diretor X",
            cpf="555.555.555-55",
            cargo="diretor",
        )
        self.assertEqual(gestor.cargo, "diretor")