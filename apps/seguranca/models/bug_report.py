from django.db import models
from django.conf import settings
from apps.comum.models.tenant import TenantModel


class BugReport(TenantModel):
    """
    Relatórios de bugs enviados voluntariamente pelos usuários.
    """

    STATUS_CHOICES = [
        ("NOVO", "Novo"),
        ("ANALISE", "Em Análise"),
        ("CORRIGIDO", "Corrigido"),
        ("REJEITADO", "Rejeitado / Duplicado"),
    ]

    PRIORIDADE_CHOICES = [
        ("BAIXA", "Baixa"),
        ("MEDIA", "Média"),
        ("ALTA", "Alta"),
        ("CRITICA", "Crítica (Showstopper)"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bugs_reportados",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    url_origem = models.CharField(max_length=500, blank=True, null=True)
    screenshot = models.ImageField(upload_to="bugs/screenshots/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NOVO")
    prioridade = models.CharField(
        max_length=20, choices=PRIORIDADE_CHOICES, default="MEDIA"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    # SLA e Gestão
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chamados_atribuidos",
        verbose_name="Técnico Responsável"
    )
    sla_limite = models.DateTimeField(null=True, blank=True, verbose_name="Prazo SLA")

    # Metadados técnicos capturados automaticamente
    browser_info = models.TextField(blank=True, null=True)
    ip_endereco = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Report de Bug"
        verbose_name_plural = "Reports de Bugs"
        ordering = ["-data_criacao"]

    def save(self, *args, **kwargs):
        if not self.sla_limite and self.prioridade:
            from django.utils import timezone
            from datetime import timedelta
            
            prazos = {
                "CRITICA": 4,   # 4 horas
                "ALTA": 24,     # 24 horas
                "MEDIA": 72,    # 72 horas
                "BAIXA": 168,   # 7 dias
            }
            horas = prazos.get(self.prioridade, 72)
            self.sla_limite = timezone.now() + timedelta(hours=horas)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.prioridade}] {self.titulo} - {self.status}"
