
from django.contrib.auth.models import User
from django.db import models
# ===================== IMPORTS (TODOS NO TOPO) =====================

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# ===================== CONSTANTES COMPARTILHADAS =====================

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


# ===================== TURMA =====================



class Turma(models.Model):
    TURNO_CHOICES = [
        ("manha", "Manhã"),
        ("tarde", "Tarde"),
        ("noite", "Noite"),
    ]

    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, default="manha")
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()} " f"({self.ano})"


from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Professor(models.Model):
    # ------------------ UFs ------------------
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

    # ------------------ RELAÇÃO COM USUÁRIO ------------------

# ===================== PROFESSOR =====================


class Professor(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professor"
    )

    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)

    formacao = models.CharField(max_length=255, blank=True)
    especializacao = models.CharField(max_length=255, blank=True)
    area_atuacao = models.CharField(max_length=255, blank=True)

    foto = models.ImageField(upload_to="fotos/professores/", null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Professor"
        verbose_name_plural = "Professores"


        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo



from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# ===================== ALUNO =====================



class Aluno(models.Model):
    NATURALIDADE_CHOICES = [
        ("brasileiro", "Brasileiro(a)"),
        ("estrangeiro", "Estrangeiro(a)"),
    ]

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

    # ------------------ RELAÇÃO COM USUÁRIO ------------------
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")

    # ------------------ DADOS PESSOAIS ------------------

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")


    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField()

    naturalidade = models.CharField(
        max_length=20,
        choices=NATURALIDADE_CHOICES,
        default="brasileiro",
    )

    filiacao_1 = models.CharField(max_length=255)
    filiacao_2 = models.CharField(max_length=255, blank=True)


    # ------------------ NECESSIDADES ESPECIAIS ------------------
    necessidade_especial = models.BooleanField(
        default=False, verbose_name="Possui necessidade especial?"
    )
    descricao_necessidade = models.TextField(
        blank=True, verbose_name="Descrição da necessidade especial"
    )

    necessidade_especial = models.BooleanField(default=False)
    descricao_necessidade = models.TextField(blank=True)


    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)


    # ------------------ ALOCAÇÃO ------------------
    turma = models.ForeignKey("Turma", on_delete=models.CASCADE, related_name="alunos")

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")


    foto = models.ImageField(upload_to="fotos/alunos/", null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

        ordering = ["nome_completo"]

    def __str__(self):
        return f"{self.nome_completo} - {self.turma}"



# ------------------ DISCIPLINA ------------------

# ===================== DISCIPLINA =====================



class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.turma})"


# ===================== NOTA =====================


class Nota(models.Model):
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
        notas = [
            n for n in [self.nota1, self.nota2, self.nota3, self.nota4] if n is not None
        ]
        return sum(notas) / len(notas) if notas else None

    def __str__(self):
        return f"{self.aluno} - {self.disciplina}"



# ------------------ GESTOR ------------------
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# ===================== GESTOR =====================



class Gestor(models.Model):
    CARGO_CHOICES = [
        ("diretor", "Diretor"),
        ("vice_diretor", "Vice-Diretor"),
        ("secretario", "Secretário"),
        ("coordenador", "Coordenador"),
    ]


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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gestor")


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gestor")


    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES) # type: ignore

    cep = models.CharField(max_length=9)
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

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


# ===================== GRADE HORÁRIA =====================


class GradeHorario(models.Model):
    turma = models.OneToOneField(Turma, on_delete=models.CASCADE)
    dados = models.JSONField(default=dict)

    def __str__(self):
        return f"Grade Horária - {self.turma}"
