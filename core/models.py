"""
Módulo de modelos da aplicação core.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


# ==========================================================
# CONSTANTES E ENUMERAÇÕES
# ==========================================================

UF_CHOICES = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"),
    ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"),
    ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"),
    ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
]

TURNO_CHOICES = [
    ("manha", "Manhã"),
    ("tarde", "Tarde"),
    ("noite", "Noite"),
]

CARGO_CHOICES = [
    ("diretor", "Diretor"),
    ("vice_diretor", "Vice-Diretor"),
    ("secretario", "Secretário"),
    ("coordenador", "Coordenador"),
]


# ==========================================================
# MODELOS ACADÊMICOS
# ==========================================================


class Turma(models.Model):
    """Representa uma turma escolar."""

    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)
    ano = models.IntegerField()

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


# ==========================================================
# GESTÃO ADMINISTRATIVA
# ==========================================================


class Gestor(models.Model):
    """Representa um gestor escolar (diretor, coordenador, etc.)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gestor")
    nome_completo = models.CharField(max_length=255)

    cpf = models.CharField(
        max_length=14,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )

    # FIX: campo ausente no model original — adicionado
    data_nascimento = models.DateField(blank=True, null=True)

    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    telefone = models.CharField(max_length=20, blank=True)

    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    foto = models.ImageField(upload_to="fotos/gestores/", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class Professor(models.Model):
    """Representa um professor da instituição."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professor"
    )
    nome_completo = models.CharField(max_length=255)

    cpf = models.CharField(
        max_length=14,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )

    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)

    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    formacao = models.CharField(max_length=255, blank=True)
    especializacao = models.CharField(max_length=255, blank=True)
    area_atuacao = models.CharField(max_length=255, blank=True)

    foto = models.ImageField(upload_to="fotos/professores/", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo


class Aluno(models.Model):
    """Representa um aluno matriculado."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    nome_completo = models.CharField(max_length=255)

    cpf = models.CharField(
        max_length=14,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )

    data_nascimento = models.DateField(blank=True, null=True)
    naturalidade = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    responsavel1 = models.CharField(max_length=255, blank=True)
    responsavel2 = models.CharField(max_length=255, blank=True)

    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    possui_necessidade_especial = models.BooleanField(default=False)
    descricao_necessidade = models.TextField(blank=True)

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")

    foto = models.ImageField(upload_to="fotos/alunos/", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return f"{self.nome_completo} - {self.turma}"


class Disciplina(models.Model):
    """Representa uma disciplina escolar."""

    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="disciplinas"
    )
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, related_name="disciplinas"
    )

    def __str__(self):
        return f"{self.nome} - {self.turma.nome}"


# ==========================================================
# GRADE DE HORÁRIOS
# ==========================================================


class GradeHorario(models.Model):
    """Grade de horários de uma turma."""

    DIAS_SEMANA = [
        ("segunda", "Segunda-feira"),
        ("terca", "Terça-feira"),
        ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"),
        ("sexta", "Sexta-feira"),
    ]

    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, related_name="grade_horarios"
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grade_horarios",
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grade_horarios",
    )

    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA, default="segunda")
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fim = models.TimeField(null=True, blank=True)
    observacao = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["turma", "dia_semana", "horario_inicio"],
                name="unique_horario_turma",
            )
        ]
        ordering = ["turma", "dia_semana", "horario_inicio"]
        verbose_name = "Horário"
        verbose_name_plural = "Grade de Horários"

    def clean(self):
        if self.disciplina and self.turma:
            if self.disciplina.turma != self.turma:
                raise ValidationError("A disciplina não pertence à turma informada.")
        if self.professor and self.disciplina:
            if self.professor != self.disciplina.professor:
                raise ValidationError("O professor não corresponde à disciplina.")
        if self.horario_inicio and self.horario_fim:
            if self.horario_fim <= self.horario_inicio:
                raise ValidationError("O horário de término deve ser após o início.")

    def __str__(self):
        return f"{self.turma} - {self.get_dia_semana_display()} - {self.horario_inicio}"


# ==========================================================
# FREQUÊNCIA
# ==========================================================


class Frequencia(models.Model):
    """Registra a presença do aluno em determinada disciplina e data."""

    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="frequencias"
    )
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="frequencias"
    )
    data = models.DateField()
    presente = models.BooleanField(default=True)

    # FIX: campo correto é "observacao", não "justificativa"
    observacao = models.CharField(max_length=255, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aluno", "disciplina", "data")
        ordering = ["-data"]

    def __str__(self):
        status = "Presente" if self.presente else "Falta"
        return f"{self.aluno} - {self.disciplina} - {self.data} ({status})"


# ==========================================================
# NOTAS
# ==========================================================


class Nota(models.Model):
    """
    Armazena as notas bimestrais (nota1–nota4) de um aluno por disciplina.

    FIX: modelo original tinha `valor` + `bimestre` (uma linha por bimestre),
    mas as views esperavam nota1–nota4 numa única linha por (aluno, disciplina).
    Modelo atualizado para ser consistente com as views e com o painel do aluno.
    """

    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="notas"
    )
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="notas"
    )

    # FIX: campos nota1–nota4 (um por bimestre) com null permitido para lançamento parcial
    nota1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota4 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    observacao = models.CharField(max_length=255, blank=True)
    data_lancamento = models.DateField(auto_now_add=True)

    class Meta:
        # FIX: unique por (aluno, disciplina) — uma linha por par, não por bimestre
        unique_together = ("aluno", "disciplina")
        ordering = ["aluno", "disciplina"]
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    @property
    def media(self):
        """Calcula a média aritmética das notas lançadas. Retorna None se nenhuma foi lançada."""
        valores = [v for v in (self.nota1, self.nota2, self.nota3, self.nota4) if v is not None]
        if not valores:
            return None
        return sum(valores) / len(valores)

    def __str__(self):
        return f"{self.aluno} - {self.disciplina} (média: {self.media})"