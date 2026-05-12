from django.db import models
from apps.comum.models.tenant import TenantModel


class ConfiguracaoSeguranca(TenantModel):
    """
    Configurações globais de segurança e estado do sistema.
    """

    manutencao_ativa = models.BooleanField(
        default=False, verbose_name="Modo Manutenção Ativo"
    )
    mensagem_manutencao = models.TextField(
        default="O sistema está passando por uma manutenção programada para melhorias. Voltaremos em breve!",
        verbose_name="Mensagem de Manutenção",
    )
    permite_login_gestor = models.BooleanField(
        default=True,
        verbose_name="Permitir Login de Gestores em Manutenção",
        help_text="Se desativado, apenas Superusuários poderão acessar.",
    )

    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração de Segurança"
        verbose_name_plural = "Configurações de Segurança"

    def __str__(self):
        status = "ATIVO" if self.manutencao_ativa else "INATIVO"
        return f"Modo Manutenção: {status}"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
