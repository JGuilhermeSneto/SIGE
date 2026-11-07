from django.conf import settings
from django.db import models


class SessaoAssistente(models.Model):
    """
    Representa uma sessão de diálogo entre o gestor escolar e o assistente ELISE IA.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessoes_ia",
        verbose_name="Usuário Gestor"
    )
    titulo = models.CharField("Título da Sessão", max_length=255, default="Nova Consulta de Gestão")
    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Sessão do Assistente"
        verbose_name_plural = "Sessões do Assistente"
        ordering = ["-atualizado_em"]

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"


class MensagemAssistente(models.Model):
    """
    Mensagens trocadas dentro de uma sessão, registrando a pergunta do gestor,
    o contexto determinístico fornecido e a resposta fundamentada da IA.
    """
    PAPEL_CHOICES = (
        ("user", "Usuário"),
        ("assistant", "Assistente ELISE IA"),
        ("system", "Sistema"),
    )

    sessao = models.ForeignKey(
        SessaoAssistente,
        on_delete=models.CASCADE,
        related_name="mensagens",
        verbose_name="Sessão"
    )
    papel = models.CharField("Papel", max_length=20, choices=PAPEL_CHOICES)
    conteudo = models.TextField("Conteúdo da Mensagem")
    contexto_utilizado = models.TextField(
        "Contexto Utilizado",
        blank=True,
        null=True,
        help_text="Resumo determinístico dos dados do ELISE injetados no prompt da LLM."
    )
    latencia_segundos = models.FloatField(
        "Latência de Inferência (s)",
        null=True,
        blank=True,
        help_text="Tempo medido em segundos para geração da resposta pela LLM."
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem do Assistente"
        verbose_name_plural = "Mensagens do Assistente"
        ordering = ["criado_em"]

    def __str__(self):
        return f"[{self.papel}] {self.conteudo[:50]}... ({self.sessao.usuario})"


class PropostaDecisao(models.Model):
    """
    Objeto formal de Apoio à Decisão (DSS) gerado pela IA com Human-in-the-Loop.
    Apresenta um diagnóstico e sugestão justificada (Direito à Explicação / LGPD),
    mas aguarda aprovação manual explícita do gestor antes de qualquer alteração no sistema.
    """
    TIPO_CHOICES = (
        ("ENTURMACAO", "Enturmação e Balanceamento Pedagógico"),
        ("INFRAESTRUTURA", "Infraestrutura e Ocupação de Salas"),
        ("FINANCEIRO", "Sustentabilidade Financeira e Inadimplência"),
        ("GERAL", "Apoio Geral à Tomada de Decisão"),
    )

    STATUS_CHOICES = (
        ("PENDENTE", "Pendente de Avaliação"),
        ("APROVADA", "Aprovada pelo Gestor"),
        ("REJEITADA", "Rejeitada pelo Gestor"),
    )

    sessao = models.ForeignKey(
        SessaoAssistente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="propostas",
        verbose_name="Sessão de Origem"
    )
    tipo = models.CharField(
        "Tipo de Proposta",
        max_length=30,
        choices=TIPO_CHOICES,
        default="GERAL"
    )
    titulo = models.CharField("Título da Proposta", max_length=255)
    descricao = models.TextField("Descrição do Cenário")
    justificativa = models.TextField(
        "Justificativa (Direito à Explicação - LGPD)",
        help_text="Critérios e números do ELISE em que a sugestão foi embasada."
    )
    dados_proposta = models.JSONField(
        "Dados Estruturados",
        default=dict,
        blank=True,
        help_text="Estrutura JSON com o estado antes/depois ou parâmetros a serem aplicados se aprovado."
    )
    status = models.CharField(
        "Status da Decisão",
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDENTE"
    )
    decidido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="propostas_decididas",
        verbose_name="Decidido por"
    )
    decidido_em = models.DateTimeField("Data da Decisão", null=True, blank=True)
    observacao_gestor = models.TextField("Observações do Gestor", blank=True, null=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Proposta de Decisão (DSS)"
        verbose_name_plural = "Propostas de Decisão (DSS)"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.titulo}"
