"""
O que é: cada perfil herda dados pessoais de ``PessoaBase`` e possui um vínculo
``OneToOneField`` com ``auth.User``; define papéis e permissões.
"""

from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
from apps.comum.models.modelo_base import PessoaBase

User = get_user_model()

CARGO_CHOICES = [
    ("diretor", "Diretor"),
    ("vice_diretor", "Vice-Diretor"),
    ("secretario", "Secretário"),
    ("coordenador", "Coordenador"),
]

from simple_history.models import HistoricalRecords


class Gestor(PessoaBase):
    """Representa um gestor escolar."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="gestor",
        help_text="Usuário vinculado ao gestor",
    )
    cargo = models.CharField(
        max_length=20, choices=CARGO_CHOICES, help_text="Cargo do gestor"
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "core_gestor"
        ordering = ["nome_completo"]
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class Professor(PessoaBase):
    """Representa um professor."""

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

    history = HistoricalRecords()

    class Meta:
        db_table = "core_professor"
        ordering = ["nome_completo"]
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo


class Aluno(PessoaBase):
    """Representa um aluno."""

    STATUS_MATRICULA_CHOICES = [
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),
        ("EVADIDO", "Evadido"),
        ("TRANSFERIDO", "Transferido"),
        ("FORMADO", "Formado"),
    ]

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
    status_matricula = models.CharField(
        max_length=15,
        choices=STATUS_MATRICULA_CHOICES,
        default="ATIVO",
        help_text="Situação atual da matrícula do aluno",
    )
    turma = models.ForeignKey(
        "academico.Turma",
        on_delete=models.CASCADE,
        related_name="alunos",
        help_text="Turma do aluno",
    )
    matricula = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text="Matrícula única do aluno (Padrão: YYYYTTTUUUU)",
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "core_aluno"
        ordering = ["nome_completo"]
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def save(self, *args: Any, **kwargs: Any) -> None:
        # Gerar matrícula se não existir
        if not self.matricula:
            from datetime import datetime

            ano = datetime.now().year
            t_id = self.turma_id if self.turma_id else 0
            u_id = self.user_id if self.user_id else 0

            # A matrícula usa o padrão YYYY (ano) + TTT (id turma) + UUUU (id user)
            self.matricula = f"{ano}{t_id:03d}{u_id:04d}"

        # Sincroniza o username do usuário com a matrícula para o login
        if self.matricula and self.user.username != self.matricula:
            self.user.username = self.matricula
            self.user.save()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nome_completo} ({self.matricula})"


class Responsavel(PessoaBase):
    """Representa o responsável legal pelo aluno."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="responsavel",
        help_text="Usuário vinculado ao responsável",
    )
    parentesco = models.CharField(
        max_length=50, blank=True, help_text="Vínculo com o aluno (Ex: Pai, Mãe, Tutor)"
    )
    alunos = models.ManyToManyField(
        Aluno,
        related_name="responsaveis",
        help_text="Alunos sob responsabilidade deste perfil",
    )

    history = HistoricalRecords()

    # Controle Parental
    controle_parental_ativo = models.BooleanField(
        default=False,
        help_text="Se ativado, o responsável recebe notificações em tempo real e pode restringir acessos.",
    )
    limite_diario_minutos = models.PositiveIntegerField(
        default=0,
        help_text="Tempo máximo de uso do sistema pelo aluno por dia (0 para ilimitado).",
    )

    class Meta:
        db_table = "core_responsavel"
        ordering = ["nome_completo"]
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    def __str__(self) -> str:
        return f"{self.nome_completo} (Responsável)"
