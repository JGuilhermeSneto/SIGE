from django.db import models
from django.conf import settings
from apps.comum.models.tenant import TenantModel

class BlacklistIP(TenantModel):
    """
    Lista negra de endereços IP bloqueados permanentemente ou temporariamente.
    """
    ip_endereco = models.GenericIPAddressField(unique=True, help_text="Endereço IP a ser bloqueado")
    motivo = models.TextField(help_text="Motivo do bloqueio (ex: Brute Force, Scanner de Vulnerabilidades)")
    data_bloqueio = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField(null=True, blank=True, help_text="Deixe vazio para bloqueio permanente")
    bloqueado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="bloqueios_realizados"
    )

    class Meta:
        verbose_name = "IP Bloqueado"
        verbose_name_plural = "Blacklist de IPs"
        ordering = ["-data_bloqueio"]

    def __str__(self):
        return f"{self.ip_endereco} - {self.motivo[:30]}"

    @property
    def is_active(self):
        from django.utils import timezone
        if self.expira_em and self.expira_em < timezone.now():
            return False
        return True
