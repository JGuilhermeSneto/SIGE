"""
Módulo de modelos da aplicação core.

Define as entidades principais do sistema escolar:
- Turma: agrupamento de alunos por turno e ano letivo.
- Professor: docente vinculado a um User do Django.
- Aluno: estudante vinculado a um User, com dados pessoais e escolares.
- Disciplina: matéria ministrada por um Professor para uma Turma.
- Nota: avaliações bimestrais de um Aluno em uma Disciplina.
- Gestor: administrador escolar (diretor, vice, secretário, coordenador).
- GradeHorario: grade de horários semanais de uma Turma em formato JSON.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

# Obtém o modelo de User ativo no projeto (respeita AUTH_USER_MODEL)
# E5142: nunca importar diretamente de django.contrib.auth.models
User = get_user_model()


# ===================== CONSTANTES =====================

# Siglas de todos os estados brasileiros usadas como opções de UF
UF_CHOICES = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"),
    ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"),
    ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"),
    ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
]

# Turnos disponíveis para uma Turma
TURNO_CHOICES = [
    ("manha", "Manhã"),
    ("tarde", "Tarde"),
    ("noite", "Noite"),
]

# Cargos disponíveis para um Gestor escolar
CARGO_CHOICES = [
    ("diretor", "Diretor"),
    ("vice_diretor", "Vice-Diretor"),
    ("secretario", "Secretário"),
    ("coordenador", "Coordenador"),
]


# ===================== MODELS =====================

class Turma(models.Model):
    """
    Representa uma turma escolar.

    Agrupa alunos de acordo com o turno (manhã/tarde/noite) e o ano letivo.
    """

    # Nome identificador da turma, ex.: "9º Ano A"
    nome = models.CharField(max_length=100)

    # Turno em que a turma estuda; padrão: manhã
    turno = models.CharField(
        max_length=20,
        choices=TURNO_CHOICES,
        default="manha"
    )

    # Ano letivo da turma, ex.: 2024
    ano = models.IntegerField()

    def __str__(self):
        """Retorna representação textual com nome, turno e ano."""
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


class Professor(models.Model):
    """
    Representa um professor cadastrado no sistema.

    Cada Professor é vinculado a exatamente um User do Django (OneToOne),
    que gerencia autenticação e permissões.
    """

    # Vínculo de autenticação: ao deletar o User, o Professor é removido
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor"
    )

    # ===== Dados pessoais =====
    nome_completo = models.CharField(max_length=255)

    # CPF único no sistema; sem validação de formato aqui (feita no form)
    cpf = models.CharField(max_length=14, unique=True)

    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    # ===== Localização =====
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)

    # Campos de endereço completo
    cep = models.CharField(max_length=9, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    # ===== Formação acadêmica =====
    formacao = models.CharField(max_length=255, blank=True)
    especializacao = models.CharField(max_length=255, blank=True)
    area_atuacao = models.CharField(max_length=255, blank=True)

    # ===== Foto de perfil =====
    foto = models.ImageField(
        upload_to="fotos/professores/",
        null=True,
        blank=True
    )

    # ===== Auditoria =====
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Retorna o nome completo do professor."""
        return self.nome_completo


class Aluno(models.Model):
    """
    Representa um aluno matriculado na escola.

    Vinculado a um User para autenticação e pertencente a uma Turma.
    Suporta registro de necessidades especiais e dados de filiação.
    """

    # Vínculo de autenticação: ao deletar o User, o Aluno é removido
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="aluno"
    )

    # ===== Dados pessoais =====
    nome_completo = models.CharField(max_length=255)

    # CPF com validação de formato via RegexValidator
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")]
    )
    data_nascimento = models.DateField(null=True, blank=True)

    # Cidade de nascimento do aluno
    naturalidade = models.CharField(max_length=100, blank=True)

    # ===== Contato =====
    # E-mail de contato direto (diferente do e-mail de login no User)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    # ===== Filiação =====
    # Nome do primeiro responsável legal (pai, mãe ou responsável)
    filiacao1 = models.CharField(
        "Nome do responsável 1",
        max_length=255,
        blank=True
    )
    # Nome do segundo responsável legal (opcional)
    filiacao2 = models.CharField(
        "Nome do responsável 2",
        max_length=255,
        blank=True
    )

    # ===== Escolar =====
    # Turma à qual o aluno está matriculado; obrigatório
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="alunos"
    )

    # ===== Endereço =====
    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    # ===== Necessidades especiais =====
    # Flag que indica se o aluno possui alguma necessidade especial
    possui_necessidade_especial = models.BooleanField(default=False)

    # Descrição detalhada da necessidade; preenchida quando a flag é True
    descricao_necessidade = models.TextField(blank=True)

    # ===== Outros =====
    foto = models.ImageField(
        upload_to="fotos/alunos/",
        null=True,
        blank=True
    )

    # ===== Auditoria =====
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadados do modelo Aluno."""

        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        # Listagens ordenadas alfabeticamente por padrão
        ordering = ["nome_completo"]

    def __str__(self):
        """Retorna nome do aluno e sua turma."""
        return f"{self.nome_completo} - {self.turma}"


class Disciplina(models.Model):
    """
    Representa uma disciplina ministrada por um Professor em uma Turma.

    A combinação Professor + Turma identifica uma disciplina específica
    no contexto do horário escolar.
    """

    # Nome da disciplina, ex.: "Matemática", "Português"
    nome = models.CharField(max_length=100)

    # Professor responsável por ministrar esta disciplina
    professor = models.ForeignKey(
        "Professor",
        on_delete=models.CASCADE
    )

    # Turma para a qual a disciplina é ministrada
    turma = models.ForeignKey(
        "Turma",
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Retorna nome da disciplina e a turma associada."""
        return f"{self.nome} ({self.turma})"


class Nota(models.Model):
    """
    Registra as notas bimestrais de um Aluno em uma Disciplina.

    Permite até 4 notas (bimestres). A média é calculada
    automaticamente via property, ignorando bimestres sem nota.
    """

    # Aluno avaliado
    aluno = models.ForeignKey("Aluno", on_delete=models.CASCADE)

    # Disciplina avaliada
    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE)

    # Notas dos quatro bimestres; opcionais para lançamento parcial
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    nota3 = models.FloatField(null=True, blank=True)
    nota4 = models.FloatField(null=True, blank=True)

    class Meta:
        """Metadados do modelo Nota."""

        # Garante que cada aluno tenha apenas um registro de notas por disciplina
        unique_together = ("aluno", "disciplina")

    @property
    def media(self):
        """
        Calcula a média aritmética das notas lançadas.

        Ignora bimestres com valor None (ainda não lançados).
        Retorna None se nenhuma nota tiver sido lançada.
        """
        notas = [
            n for n in [self.nota1, self.nota2, self.nota3, self.nota4]
            if n is not None
        ]
        return sum(notas) / len(notas) if notas else None

    def __str__(self):
        """Retorna aluno e disciplina relacionados à nota."""
        return f"{self.aluno} - {self.disciplina}"


class Gestor(models.Model):
    """
    Representa um gestor escolar (diretor, vice-diretor, secretário etc.).

    Vinculado a um User para autenticação, com dados de cargo e localização.
    """

    # Vínculo de autenticação: ao deletar o User, o Gestor é removido
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="gestor"
    )

    # ===== Dados pessoais =====
    nome_completo = models.CharField(max_length=150)

    # CPF com validação de formato via RegexValidator
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")]
    )

    # Cargo exercido pelo gestor na instituição
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)

    # ===== Localização =====
    uf = models.CharField(max_length=2, choices=UF_CHOICES)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    # ===== Foto de perfil =====
    foto = models.ImageField(
        upload_to="fotos/gestores/",
        null=True,
        blank=True
    )

    # ===== Auditoria =====
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadados do modelo Gestor."""

        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"
        # Listagens ordenadas alfabeticamente por padrão
        ordering = ["nome_completo"]

    def __str__(self):
        """Retorna nome completo e cargo legível do gestor."""
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class GradeHorario(models.Model):
    """
    Armazena a grade de horários semanal de uma Turma em formato JSON.

    O campo `dados` é flexível para acomodar diferentes estruturas de
    horário sem necessidade de migrations a cada mudança de layout.
    """

    # Cada turma possui exatamente uma grade de horários
    turma = models.OneToOneField("Turma", on_delete=models.CASCADE)

    # Grade armazenada como dict JSON; estrutura definida pelo front-end/serializer
    dados = models.JSONField(default=dict)

    def __str__(self):
        """Retorna identificação da grade vinculada à turma."""
        return f"Grade Horária - {self.turma}"
    