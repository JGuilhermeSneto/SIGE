"""
Módulo de modelos da aplicação core.

Este arquivo define todas as entidades centrais do Sistema de Gestão Escolar,
incluindo usuários acadêmicos, organização escolar, avaliações, frequência
e administração institucional.

Todos os modelos aqui definidos representam tabelas no banco de dados
e seguem os princípios de normalização e clareza semântica.
"""

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

# Obtém dinamicamente o modelo de usuário configurado no projeto
# (permite compatibilidade com User customizado)
from django.contrib.auth import get_user_model

# Utilizado para validações de campos, como CPF
from django.core.validators import RegexValidator

# Módulo base para definição de modelos ORM do Django
from django.db import models

# Referência ao modelo de usuário ativo no projeto
User = get_user_model()


# ==========================================================
# CONSTANTES E ENUMERAÇÕES
# ==========================================================

# Lista de Unidades Federativas utilizadas em campos de endereço
UF_CHOICES = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"),
    ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"),
    ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"),
    ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"),
    ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
]

# Turnos possíveis para turmas escolares
TURNO_CHOICES = [
    ("manha", "Manhã"),
    ("tarde", "Tarde"),
    ("noite", "Noite"),
]

# Cargos administrativos disponíveis para gestores
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
    """
    Representa uma turma escolar.

    Uma turma agrupa alunos, disciplinas e horários,
    sendo identificada por nome, turno e ano letivo.
    """

    # Nome identificador da turma (ex: 1º Ano A)
    nome = models.CharField(max_length=100)

    # Turno em que a turma funciona
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)

    # Ano letivo de referência
    ano = models.IntegerField()

    def __str__(self):
        """
        Retorna uma representação textual da turma,
        utilizada em selects, admin e logs.
        """
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


class Professor(models.Model):
    """
    Representa um professor da instituição de ensino.

    Este modelo armazena dados pessoais, endereço,
    formação acadêmica e vínculo com o usuário do sistema.
    """

    # ======================================================
    # VÍNCULO COM USUÁRIO DO SISTEMA
    # ======================================================
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professor"
    )

    # ======================================================
    # DADOS PESSOAIS
    # ======================================================
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
    )
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)

    # ======================================================
    # ENDEREÇO
    # ======================================================
    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=255, blank=True)

    # ======================================================
    # FORMAÇÃO ACADÊMICA
    # ======================================================
    formacao = models.CharField(max_length=255, blank=True)
    especializacao = models.CharField(max_length=255, blank=True)
    area_atuacao = models.CharField(max_length=255, blank=True)

    # ======================================================
    # FOTO
    # ======================================================
    foto = models.ImageField(upload_to="fotos/professores/", blank=True, null=True)

    # ======================================================
    # AUDITORIA
    # ======================================================
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo


class Aluno(models.Model):
    """
    Representa um aluno matriculado na instituição de ensino.

    Este modelo armazena dados pessoais, endereço, responsáveis,
    informações educacionais especiais e vínculo com o sistema.
    """

    # ======================================================
    # VÍNCULO COM USUÁRIO DO SISTEMA
    # ======================================================
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")

    # ======================================================
    # DADOS PESSOAIS
    # ======================================================
    nome_completo = models.CharField(max_length=255, verbose_name="Nome completo")
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
        verbose_name="CPF",
    )
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de nascimento")
    naturalidade = models.CharField(max_length=100, blank=True, verbose_name="Naturalidade")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")

    # ======================================================
    # RESPONSÁVEIS
    # ======================================================
    responsavel1 = models.CharField(max_length=255, blank=True, verbose_name="Responsável 1")
    responsavel2 = models.CharField(max_length=255, blank=True, verbose_name="Responsável 2")

    # ======================================================
    # ENDEREÇO
    # ======================================================
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, verbose_name="UF")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    logradouro = models.CharField(max_length=255, blank=True, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=255, blank=True, verbose_name="Complemento")

    # ======================================================
    # NECESSIDADES EDUCACIONAIS ESPECIAIS
    # ======================================================
    possui_necessidade_especial = models.BooleanField(default=False, verbose_name="Possui necessidade especial")
    descricao_necessidade = models.TextField(blank=True, verbose_name="Descrição da necessidade especial")

    # ======================================================
    # VÍNCULO ACADÊMICO
    # ======================================================
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")

    # ======================================================
    # FOTO
    # ======================================================
    foto = models.ImageField(upload_to="fotos/alunos/", blank=True, null=True, verbose_name="Foto")

    # ======================================================
    # AUDITORIA
    # ======================================================
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["nome_completo"]

    def __str__(self):
        return f"{self.nome_completo} - {self.turma}"


class Disciplina(models.Model):
    """
    Representa uma disciplina ministrada em uma turma.
    """

    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.turma})"


class Nota(models.Model):
    """
    Registra as notas de um aluno em uma disciplina.
    """

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    nota1 = models.FloatField(blank=True, null=True)
    nota2 = models.FloatField(blank=True, null=True)
    nota3 = models.FloatField(blank=True, null=True)
    nota4 = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ("aluno", "disciplina")

    @property
    def media(self):
        notas = [n for n in [self.nota1, self.nota2, self.nota3, self.nota4] if n is not None]
        return sum(notas) / len(notas) if notas else None


# ==========================================================
# MODELOS ADMINISTRATIVOS
# ==========================================================

class Gestor(models.Model):
    """
    Representa um gestor escolar da instituição.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gestor")
    nome_completo = models.CharField(max_length=150, verbose_name="Nome completo")
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
        verbose_name="CPF",
    )
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de nascimento")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")

    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    uf = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, verbose_name="UF")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, verbose_name="Cargo")
    foto = models.ImageField(upload_to="fotos/gestores/", blank=True, null=True, verbose_name="Foto")

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"
        ordering = ["nome_completo"]

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class GradeHorario(models.Model):
    """
    Armazena a grade de horários semanal de uma turma.
    """

    turma = models.OneToOneField(Turma, on_delete=models.CASCADE)
    dados = models.JSONField(default=dict)

    def __str__(self):
        return f"Grade Horária - {self.turma}"


# ==========================================================
# FREQUÊNCIA
# ==========================================================

class FrequenciaManager(models.Manager):
    """
    Manager customizado para facilitar consultas relacionadas à frequência.
    """

    def presentes(self):
        return self.filter(presente=True)

    def ausentes(self):
        return self.filter(presente=False)


class Frequencia(models.Model):
    """
    Registra a presença ou ausência de um aluno em uma disciplina em determinada data.
    """

    objects = FrequenciaManager()

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencias")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="frequencias")
    data = models.DateField()
    presente = models.BooleanField(default=True)
    justificativa = models.TextField(blank=True)

    class Meta:
        unique_together = ("aluno", "disciplina", "data")
        ordering = ["-data"]

    def __str__(self):
        situacao = "Presente" if self.presente else "Ausente"
        return f"{self.aluno.nome_completo} | {self.disciplina.nome} | {self.data} | {situacao}"