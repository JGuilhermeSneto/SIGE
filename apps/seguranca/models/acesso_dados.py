from django.db import models
from django.conf import settings

class AcessoDadosSensiveis(models.Model):
    """Log de conformidade LGPD para acesso a dados sensíveis."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Usuário que acessou"
    )
    recurso = models.CharField(max_length=255, verbose_name="Recurso acessado (ex: Aluno #123)")
    tipo_dado = models.CharField(max_length=100, verbose_name="Tipo de dado (ex: CPF, Financeiro)")
    data_acesso = models.DateTimeField(auto_now_add=True)
    ip_origem = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Acesso a Dados Sensíveis"
        verbose_name_plural = "Acessos a Dados Sensíveis"
        ordering = ['-data_acesso']

    def __str__(self):
        return f"{self.usuario} acessou {self.recurso} em {self.data_acesso}"
