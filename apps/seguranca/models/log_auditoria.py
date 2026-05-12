from django.db import models
from django.conf import settings
from apps.comum.models.tenant import TenantModel


class LogAuditoria(TenantModel):
    """
    Registra acessos a áreas sensíveis e ações críticas para conformidade LGPD.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="logs_auditoria",
    )
    path = models.CharField(max_length=500, help_text="Caminho/URL acessada")
    metodo = models.CharField(max_length=10, default="GET")
    ip_endereco = models.GenericIPAddressField(help_text="Endereço IP do usuário")
    user_agent = models.TextField(
        blank=True, null=True, help_text="Informações do navegador/dispositivo"
    )
    descricao = models.TextField(
        blank=True, null=True, help_text="Descrição detalhada da ação"
    )
    data_evento = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ["-data_evento"]

    def __str__(self):
        return f"{self.usuario} - {self.path} - {self.data_evento}"
