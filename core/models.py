"""
Models do app core.

Contém os modelos: Turma, Professor, Aluno, Disciplina, Nota, Gestor e GradeHorario.
"""

# ===================== IMPORTS =====================
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# ===================== CONSTANTES =====================
UF_CHOICES = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"),
    ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"),
    ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"),
    ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
]

TURNO_CHOICES = [("manha", "Manhã"), ("tarde", "Tarde"), ("noite", "Noite")]

CARGO_CHOICES = [
    ("diretor", "Diretor"),
    ("vice_diretor", "Vice-Diretor"),
    ("secretario", "Secretário"),
    ("coordenador", "Coordenador"),
]

# ===================== MODELS =====================

class Turma(models.Model):
    """Modelo para turmas escolares."""
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, default="manha")
    ano = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"  # noqa: E1101


class Professor(models.Model):
    """Modelo para professores."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor")
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True,
                           validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")])
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to="fotos/professores/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["nome_completo"]

    def __str__(self) -> str:
        return self.nome_completo


class Aluno(models.Model):
    """Modelo para alunos."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True,
                           validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")])
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to="fotos/alunos/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["nome_completo"]

    def __str__(self) -> str:
        return f"{self.nome_completo} - {self.turma}"


class Disciplina(models.Model):
    """Modelo para disciplinas."""
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.nome} ({self.turma})"


class Nota(models.Model):
    """Modelo para notas de alunos em disciplinas."""
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    nota3 = models.FloatField(null=True, blank=True)
    nota4 = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("aluno", "disciplina")

    @property
    def media(self):
        notas = [n for n in [self.nota1, self.nota2, self.nota3, self.nota4] if n is not None]
        return sum(notas) / len(notas) if notas else None

    def __str__(self) -> str:
        return f"{self.aluno} - {self.disciplina}"


class Gestor(models.Model):
    """Modelo para gestores escolares."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gestor")
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True,
                           validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")])
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    uf = models.CharField(max_length=2, choices=UF_CHOICES)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="fotos/gestores/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"
        ordering = ["nome_completo"]

    def __str__(self) -> str:
        return f"{self.nome_completo} ({self.get_cargo_display()})"  # noqa: E1101


class GradeHorario(models.Model):
    """Modelo para grade horária de uma turma."""
    turma = models.OneToOneField(Turma, on_delete=models.CASCADE)
    dados = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"Grade Horária - {self.turma}"
    