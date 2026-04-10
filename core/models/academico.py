from django.db import models
from .base import TURNO_CHOICES

class Turma(models.Model):
    """Representa uma turma escolar."""
    nome = models.CharField(max_length=100, help_text="Nome da turma")
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, help_text="Turno da turma")
    ano = models.IntegerField(help_text="Ano da turma")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


class Disciplina(models.Model):
    """Representa uma disciplina."""
    nome = models.CharField(max_length=100, help_text="Nome da disciplina")
    professor = models.ForeignKey(
        "Professor", on_delete=models.CASCADE, related_name="disciplinas", help_text="Professor responsável"
    )
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, related_name="disciplinas", help_text="Turma associada"
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return f"{self.nome} - {self.turma.nome}"


class GradeHorario(models.Model):
    """Representa a grade horária de uma turma."""
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="grades")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="grades")

    DIA_CHOICES = [
        ("segunda", "Segunda-feira"), ("terca", "Terça-feira"), ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"), ("sexta", "Sexta-feira"),
    ]
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    horario = models.CharField(max_length=20, help_text="Ex: 07:00 - 07:50")

    class Meta:
        verbose_name = "Grade de Horário"
        verbose_name_plural = "Grades de Horários"
        unique_together = ("turma", "dia", "horario")
        ordering = ["horario", "dia"]

    def __str__(self):
        return f"{self.turma} | {self.dia} | {self.horario} | {self.disciplina}"
