from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .base import PessoaBase

User = get_user_model()

CARGO_CHOICES = [
    ("diretor", "Diretor"),
    ("vice_diretor", "Vice-Diretor"),
    ("secretario", "Secretário"),
    ("coordenador", "Coordenador"),
]

class Gestor(PessoaBase):
    """Representa um gestor escolar."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="gestor", help_text="Usuário vinculado ao gestor"
    )
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, help_text="Cargo do gestor")

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"

    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class Professor(PessoaBase):
    """Representa um professor."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professor", help_text="Usuário vinculado ao professor"
    )
    formacao = models.CharField(max_length=255, blank=True, help_text="Formação acadêmica")
    especializacao = models.CharField(max_length=255, blank=True, help_text="Especialização")
    area_atuacao = models.CharField(max_length=255, blank=True, help_text="Área de atuação")

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo


class Aluno(PessoaBase):
    """Representa um aluno."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="aluno", help_text="Usuário vinculado ao aluno"
    )
    naturalidade = models.CharField(max_length=100, blank=True, help_text="Cidade de origem")
    responsavel1 = models.CharField(max_length=255, blank=True, help_text="Nome do responsável principal")
    responsavel2 = models.CharField(max_length=255, blank=True, help_text="Nome do segundo responsável")
    possui_necessidade_especial = models.BooleanField(default=False, help_text="Indica se possui necessidade especial")
    descricao_necessidade = models.TextField(blank=True, help_text="Descrição da necessidade especial")
    turma = models.ForeignKey(
        "academic.Turma" if False else "Turma", # Placeholder logic if split apps, but keeping in same app core for now
        on_delete=models.CASCADE, related_name="alunos", help_text="Turma do aluno"
    )

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return f"{self.nome_completo} - {self.turma}"
