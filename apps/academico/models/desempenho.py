"""
Modelos de desempenho: frequência, notas, entregas e rubricas de avaliação.

O que é: registra o que o professor lança e o que o sistema usa para situação
final (média + frequência).
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Frequencia(models.Model):
    """Registra presença do aluno."""
    aluno = models.ForeignKey("usuarios.Aluno", on_delete=models.CASCADE, related_name="frequencias")
    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE, related_name="frequencias")
    data = models.DateField(help_text="Data da frequência")
    presente = models.BooleanField(default=True, help_text="Presença (True) ou Falta (False)")
    justificada = models.BooleanField(default=False, help_text="Se a falta foi justificada por atestado")
    atestado = models.ForeignKey(
        "saude.AtestadoMedico", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="frequencias_justificadas"
    )
    observacao = models.CharField(max_length=255, blank=True, help_text="Observações")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_frequencia'
        unique_together = ("aluno", "disciplina", "data")
        ordering = ["-data"]
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"

    def __str__(self):
        status = "Presente" if self.presente else "Falta"
        return f"{self.aluno.nome_completo} - {self.disciplina.nome} - {self.data} ({status})"


class Nota(models.Model):
    """Armazena as notas bimestrais."""
    aluno = models.ForeignKey("usuarios.Aluno", on_delete=models.CASCADE, related_name="notas")
    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE, related_name="notas")

    nota1 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    nota2 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    nota3 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    nota4 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    observacao = models.CharField(max_length=255, blank=True)
    data_lancamento = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'core_nota'
        unique_together = ("aluno", "disciplina")
        ordering = ["aluno", "disciplina"]
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    @property
    def media(self):
        """Calcula a média aritmética."""
        valores = [v for v in (self.nota1, self.nota2, self.nota3, self.nota4) if v is not None]
        if not valores: return None
        return sum(valores) / len(valores)

    def __str__(self):
        media = self.media
        media_str = f"{media:.2f}" if media is not None else "N/A"
        return f"{self.aluno.nome_completo} - {self.disciplina.nome} (média: {media_str})"

class NotaAtividade(models.Model):
    """Armazena as notas individuais calculadas a partir de trabalhos e provas do professor."""
    aluno = models.ForeignKey("usuarios.Aluno", on_delete=models.CASCADE, related_name="notas_atividades")
    atividade = models.ForeignKey("AtividadeProfessor", on_delete=models.CASCADE, related_name="notas_alunos")
    
    valor = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Nota obtida na atividade"
    )
    observacao = models.CharField(max_length=255, blank=True)
    data_lancamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_notaatividade'
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

    usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="notificacoes")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=120)
    mensagem = models.TextField() # Aumentado para suportar detalhes
    url_destino = models.CharField(max_length=255, blank=True)
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_notificacao" # Novo nome de tabela para o sistema unificado
        ordering = ["-criado_em"]
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"

# Mantendo o alias Presenca para compatibilidade
Presenca = Frequencia
