"""
Modelos de desempenho: frequência, notas, entregas e rubricas de avaliação.

O que é: registra o que o professor lança e o que o sistema usa para situação
final (média + frequência).
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords


class Frequencia(models.Model):
    """Registra presença do aluno."""

    aluno = models.ForeignKey(
        "usuarios.Aluno", on_delete=models.CASCADE, related_name="frequencias"
    )
    disciplina = models.ForeignKey(
        "Disciplina", on_delete=models.CASCADE, related_name="frequencias"
    )
    data = models.DateField(help_text="Data da frequência")
    presente = models.BooleanField(
        default=True, help_text="Presença (True) ou Falta (False)"
    )
    justificada = models.BooleanField(
        default=False, help_text="Se a falta foi justificada por atestado"
    )
    atestado = models.ForeignKey(
        "saude.AtestadoMedico",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="frequencias_justificadas",
    )
    observacao = models.CharField(max_length=255, blank=True, help_text="Observações")
    criado_em = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "core_frequencia"
        unique_together = ("aluno", "disciplina", "data")
        ordering = ["-data"]
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"

    def __str__(self):
        status = "Presente" if self.presente else "Falta"
        return f"{self.aluno.nome_completo} - {self.disciplina.nome} - {self.data} ({status})"


class Nota(models.Model):
    """Armazena as notas bimestrais."""

    aluno = models.ForeignKey(
        "usuarios.Aluno", on_delete=models.CASCADE, related_name="notas"
    )
    disciplina = models.ForeignKey(
        "Disciplina", on_delete=models.CASCADE, related_name="notas"
    )

    nota1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    nota2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    nota3 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    nota4 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    observacao = models.CharField(max_length=255, blank=True)
    data_lancamento = models.DateField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "core_nota"
        unique_together = ("aluno", "disciplina")
        ordering = ["aluno", "disciplina"]
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    @property
    def media(self):
        """Calcula a média aritmética."""
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


class NotaAtividade(models.Model):
    """Armazena as notas individuais calculadas a partir de trabalhos e provas do professor."""

    aluno = models.ForeignKey(
        "usuarios.Aluno", on_delete=models.CASCADE, related_name="notas_atividades"
    )
    atividade = models.ForeignKey(
        "AtividadeProfessor", on_delete=models.CASCADE, related_name="notas_alunos"
    )

    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota obtida na atividade",
    )
    observacao = models.CharField(max_length=255, blank=True)
    data_lancamento = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "core_notaatividade"
        unique_together = ("aluno", "atividade")
        ordering = ["aluno", "atividade"]
        verbose_name = "Nota de Atividade"
        verbose_name_plural = "Notas de Atividades"

    def __str__(self):
        return f"{self.aluno} - {self.atividade.titulo}: {self.valor if self.valor is not None else 'N/A'}"


class Notificacao(models.Model):
    """Notificações unificadas exibidas para todos os usuários (Alunos, Professores, Gestores) no painel."""

    TIPO_CHOICES = [
        # Acadêmico (Alunos)
        ("NOTA", "Nota lançada"),
        ("CHAMADA", "Chamada Realizada"),
        ("CORRECAO", "Atividade Corrigida"),
        ("GABARITO", "Gabarito Disponível"),
        # Gestão (Professores)
        ("ENTREGA", "Nova Entrega de Atividade"),
        # Saúde/Administrativo (Gestores)
        ("ATESTADO", "Novo Atestado Enviado"),
        # Geral
        ("SISTEMA", "Mensagem do Sistema"),
        ("MENSAGEM", "Nova Mensagem"),
    ]

    usuario = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="notificacoes"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=120)
    mensagem = models.TextField()  # Aumentado para suportar detalhes
    url_destino = models.CharField(max_length=255, blank=True)
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_notificacao"  # Novo nome de tabela para o sistema unificado
        ordering = ["-criado_em"]
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"


# Mantendo o alias Presenca para compatibilidade
Presenca = Frequencia


class RubricaAvaliacao(models.Model):
    """Permite avaliações baseadas em competências e critérios qualitativos."""
    nome = models.CharField(max_length=100, help_text="Ex: Trabalho em Equipe, Clareza Textual")
    descricao = models.TextField(blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    aluno = models.ForeignKey("usuarios.Aluno", on_delete=models.CASCADE, related_name="avaliacoes_rubricas")
    nota = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    data_avaliacao = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "core_rubrica_avaliacao"
        verbose_name = "Avaliação por Rubrica"
        verbose_name_plural = "Avaliações por Rubricas"


class QuestaoBanco(models.Model):
    """Banco de questões para geração de provas (Questões reutilizáveis)."""
    NIVEIS = [('FACIL', 'Fácil'), ('MEDIO', 'Médio'), ('DIFICIL', 'Difícil')]
    TIPOS = [('MULTIPLA_ESCOLHA', 'Múltipla Escolha'), ('DISSERTATIVA', 'Dissertativa')]

    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE, related_name="banco_questoes")
    enunciado = models.TextField()
    nivel = models.CharField(max_length=10, choices=NIVEIS, default='MEDIO')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='MULTIPLA_ESCOLHA')
    tags = models.CharField(max_length=255, blank=True, help_text="Tags para busca (ex: Trigonometria, Revolução Francesa)")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_questao_banco"
        verbose_name = "Questão do Banco"
        verbose_name_plural = "Banco de Questões"

    def __str__(self):
        return f"{self.disciplina} - {self.nivel} - {self.enunciado[:50]}..."


class AlternativaBanco(models.Model):
    """Alternativas para questões de múltipla escolha do banco."""
    questao = models.ForeignKey(QuestaoBanco, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.TextField()
    correta = models.BooleanField(default=False)

    class Meta:
        db_table = "core_alternativa_banco"


class ProvaGerada(models.Model):
    """Registro de provas geradas dinamicamente para alunos."""
    titulo = models.CharField(max_length=200)
    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE)
    turma = models.ForeignKey("Turma", on_delete=models.CASCADE)
    questoes = models.ManyToManyField(QuestaoBanco, related_name="provas_geradas")
    data_geracao = models.DateTimeField(auto_now_add=True)
    slug_acesso = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = "core_prova_gerada"
        verbose_name = "Prova Gerada"
        verbose_name_plural = "Provas Geradas"


class RiscoEvasao(models.Model):
    """Armazena o score de risco de evasão calculado por IA."""
    aluno = models.OneToOneField("usuarios.Aluno", on_delete=models.CASCADE, related_name="risco_evasao")
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score de 0 a 100 (Quanto maior, maior o risco)")
    fatores = models.TextField(blank=True, help_text="Explicação dos fatores (ex: Baixa frequência, notas em queda)")
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_risco_evasao"
        verbose_name = "Risco de Evasão"
        verbose_name_plural = "Riscos de Evasão"

    def __str__(self):
        return f"{self.aluno} - Score: {self.score}"


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=RiscoEvasao)
def alerta_risco_critico(sender, instance, created, **kwargs):
    """Dispara notificação se o risco for crítico (> 80)."""
    if instance.score >= 80:
        # Notificar Coordenadores/Gestores (exemplo: todos os superusuários)
        gestores = User.objects.filter(is_superuser=True)
        for gestor in gestores:
            Notificacao.objects.create(
                usuario=gestor,
                tipo="SISTEMA",
                titulo="ALERTA CRÍTICO: Risco de Evasão",
                mensagem=f"O aluno {instance.aluno.nome_completo} atingiu um score de risco de {instance.score}%. Fatores: {instance.fatores}",
                url_destino=f"/admin/academico/riscoevasao/{instance.id}/change/"
            )
