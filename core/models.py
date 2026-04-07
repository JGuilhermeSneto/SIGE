"""
Módulo de modelos da aplicação core.

Define os modelos principais da aplicação SIGE:
- Pessoas: Gestor, Professor, Aluno (herdam de PessoaBase)
- Turma, Disciplina
- Grade de Horários
- Frequência e Notas

Inclui validações, relacionamentos e propriedades úteis.
"""

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()

# ==========================================================
# CONSTANTES E ENUMERAÇÕES
# ==========================================================

UF_CHOICES = [
    ("AC", "AC"),
    ("AL", "AL"),
    ("AP", "AP"),
    ("AM", "AM"),
    ("BA", "BA"),
    ("CE", "CE"),
    ("DF", "DF"),
    ("ES", "ES"),
    ("GO", "GO"),
    ("MA", "MA"),
    ("MT", "MT"),
    ("MS", "MS"),
    ("MG", "MG"),
    ("PA", "PA"),
    ("PB", "PB"),
    ("PR", "PR"),
    ("PE", "PE"),
    ("PI", "PI"),
    ("RJ", "RJ"),
    ("RN", "RN"),
    ("RS", "RS"),
    ("RO", "RO"),
    ("RR", "RR"),
    ("SC", "SC"),
    ("SP", "SP"),
    ("SE", "SE"),
    ("TO", "TO"),
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
# MODELOS BASE
# ==========================================================


class PessoaBase(models.Model):
    """
    Modelo abstrato para armazenar campos comuns de pessoas:
    - Gestor, Professor e Aluno herdam desta base
    """

    nome_completo = models.CharField(
        max_length=255, help_text="Nome completo da pessoa"
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
        help_text="CPF no formato XXX.XXX.XXX-XX",
    )
    data_nascimento = models.DateField(
        blank=True, null=True, help_text="Data de nascimento"
    )
    telefone = models.CharField(
        max_length=20, blank=True, help_text="Número de telefone"
    )

    # Endereço
    cep = models.CharField(max_length=9, blank=True, help_text="CEP")
    estado = models.CharField(
        max_length=2, choices=UF_CHOICES, blank=True, help_text="Estado (UF)"
    )
    cidade = models.CharField(max_length=100, blank=True, help_text="Cidade")
    bairro = models.CharField(max_length=100, blank=True, help_text="Bairro")
    logradouro = models.CharField(max_length=255, blank=True, help_text="Logradouro")
    numero = models.CharField(max_length=10, blank=True, help_text="Número do endereço")
    complemento = models.CharField(
        max_length=255, blank=True, help_text="Complemento do endereço"
    )

    # Foto de perfil
    foto = models.ImageField(
        upload_to="fotos/pessoas/", blank=True, null=True, help_text="Foto da pessoa"
    )

    # Controle de criação e atualização
    criado_em = models.DateTimeField(auto_now_add=True, help_text="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, help_text="Data da última atualização"
    )

    class Meta:
        abstract = True
        verbose_name = "Pessoa Base"
        verbose_name_plural = "Pessoas Base"


# ==========================================================
# MODELOS ACADÊMICOS
# ==========================================================


class Turma(models.Model):
    """
    Representa uma turma escolar.
    """

    nome = models.CharField(max_length=100, help_text="Nome da turma")
    turno = models.CharField(
        max_length=20, choices=TURNO_CHOICES, help_text="Turno da turma"
    )
    ano = models.IntegerField(help_text="Ano da turma")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


class Disciplina(models.Model):
    """
    Representa uma disciplina de uma turma, associada a um professor.
    """

    nome = models.CharField(max_length=100, help_text="Nome da disciplina")
    professor = models.ForeignKey(
        "Professor",
        on_delete=models.CASCADE,
        related_name="disciplinas",
        help_text="Professor responsável pela disciplina",
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="disciplinas",
        help_text="Turma associada à disciplina",
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return f"{self.nome} - {self.turma.nome}"


# ==========================================================
# GESTÃO ADMINISTRATIVA
# ==========================================================


class Gestor(PessoaBase):
    """
    Representa um gestor escolar (Diretor, Vice-Diretor, Coordenador, Secretário).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="gestor",
        help_text="Usuário vinculado ao gestor",
    )
    cargo = models.CharField(
        max_length=20, choices=CARGO_CHOICES, help_text="Cargo do gestor"
    )

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class Professor(PessoaBase):
    """
    Representa um professor da instituição.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor",
        help_text="Usuário vinculado ao professor",
    )
    formacao = models.CharField(
        max_length=255, blank=True, help_text="Formação acadêmica"
    )
    especializacao = models.CharField(
        max_length=255, blank=True, help_text="Especialização"
    )
    area_atuacao = models.CharField(
        max_length=255, blank=True, help_text="Área de atuação"
    )

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo


class Aluno(PessoaBase):
    """
    Representa um aluno matriculado em uma turma.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="aluno",
        help_text="Usuário vinculado ao aluno",
    )
    naturalidade = models.CharField(
        max_length=100, blank=True, help_text="Cidade de origem"
    )
    responsavel1 = models.CharField(
        max_length=255, blank=True, help_text="Nome do responsável principal"
    )
    responsavel2 = models.CharField(
        max_length=255, blank=True, help_text="Nome do segundo responsável"
    )
    possui_necessidade_especial = models.BooleanField(
        default=False, help_text="Indica se possui necessidade especial"
    )
    descricao_necessidade = models.TextField(
        blank=True, help_text="Descrição da necessidade especial"
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="alunos",
        help_text="Turma do aluno",
    )

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return f"{self.nome_completo} - {self.turma}"


# ==========================================================
# GRADE DE HORÁRIOS
# ==========================================================

# ==========================================================
# GRADE DE HORÁRIOS (CORRETA)
# ==========================================================

class GradeHorario(models.Model):
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="grades"
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name="grades"
    )

    DIA_CHOICES = [
        ("segunda", "Segunda-feira"),
        ("terca", "Terça-feira"),
        ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"),
        ("sexta", "Sexta-feira"),
    ]

    dia = models.CharField(
        max_length=10,
        choices=DIA_CHOICES
    )

    horario = models.CharField(
        max_length=20,
        help_text="Ex: 07:00 - 07:50"
    )

    class Meta:
        verbose_name = "Grade de Horário"
        verbose_name_plural = "Grades de Horários"
        unique_together = ("turma", "dia", "horario")
        ordering = ["horario", "dia"]

    def __str__(self):
        return f"{self.turma} | {self.dia} | {self.horario} | {self.disciplina}"
    
    
    
    
# ==========================================================
# FREQUÊNCIA
# ==========================================================


class Frequencia(models.Model):
    """
    Registra presença do aluno em determinada disciplina e data.
    """

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="frequencias",
        help_text="Aluno registrado na frequência",
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name="frequencias",
        help_text="Disciplina da frequência",
    )
    data = models.DateField(help_text="Data da frequência")
    presente = models.BooleanField(
        default=True, help_text="Presença (True) ou Falta (False)"
    )
    observacao = models.CharField(
        max_length=255, blank=True, help_text="Observações sobre a frequência"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True, help_text="Data de criação do registro"
    )

    class Meta:
        unique_together = ("aluno", "disciplina", "data")
        ordering = ["-data"]
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"

    def __str__(self):
        status = "Presente" if self.presente else "Falta"
        return f"{self.aluno.nome_completo} - {self.disciplina.nome} - {self.data} ({status})"


# ==========================================================
# NOTAS
# ==========================================================


class Nota(models.Model):
    """
    Armazena as notas bimestrais de um aluno por disciplina.
    Possui quatro notas (nota1–nota4) e uma observação opcional.
    """

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="notas",
        help_text="Aluno que recebeu a nota",
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name="notas",
        help_text="Disciplina à qual a nota pertence",
    )

    nota1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota do primeiro bimestre",
    )
    nota2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota do segundo bimestre",
    )
    nota3 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota do terceiro bimestre",
    )
    nota4 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota do quarto bimestre",
    )

    observacao = models.CharField(
        max_length=255, blank=True, help_text="Observações adicionais"
    )
    data_lancamento = models.DateField(
        auto_now_add=True, help_text="Data de lançamento da nota"
    )

    class Meta:
        unique_together = ("aluno", "disciplina")
        ordering = ["aluno", "disciplina"]
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    @property
    def media(self):
        """
        Calcula a média aritmética das notas lançadas.
        Retorna None se nenhuma nota foi lançada.
        """
        valores = [
            v for v in (self.nota1, self.nota2, self.nota3, self.nota4) if v is not None
        ]
        if not valores:
            return None
        return sum(valores) / len(valores)

    def __str__(self):
        media = self.media
        media_str = f"{media:.2f}" if media is not None else "N/A"
        return (
            f"{self.aluno.nome_completo} - {self.disciplina.nome} (média: {media_str})"
        )


# No final do core/models.py
Presenca = Frequencia
