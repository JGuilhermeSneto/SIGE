from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LogErro(models.Model):
    """Armazena exceções e erros fatais ocorridos no site."""

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_excecao = models.CharField(max_length=255)
    mensagem = models.TextField()
    traceback = models.TextField()
    path = models.CharField(max_length=255)
    metodo = models.CharField(max_length=10)
    data_ocorrencia = models.DateTimeField(auto_now_add=True)
    ultima_ocorrencia = models.DateTimeField(auto_now=True)
    ip_endereco = models.GenericIPAddressField(null=True, blank=True)
    resolvido = models.BooleanField(default=False)
    
    # Novos campos para deduplicação
    hash_erro = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    contador = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-ultima_ocorrencia"]
        verbose_name = "Log de Erro"
        verbose_name_plural = "Logs de Erros"

    def __str__(self):
        return f"{self.tipo_excecao} ({self.contador}x): {self.mensagem[:50]}"
