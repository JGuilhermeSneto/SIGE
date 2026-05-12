from django.db import models


class PoliticaTi(models.Model):
    """
    Registro técnico usado para expor permissões nomeadas da área de TI.

    Não é obrigatório criar linhas nesta tabela; o objetivo é registrar
    ``Meta.permissions`` no sistema de auth do Django.
    """

    rotulo = models.CharField(max_length=64, default="default", unique=True)

    class Meta:
        verbose_name = "Política de TI"
        verbose_name_plural = "Políticas de TI"
        default_permissions = ()
        permissions = [
            ("painel_ti_basico", "Acessar painel da equipe de TI"),
            ("painel_ti_operacoes", "Acessar operações avançadas de TI"),
        ]

    def __str__(self) -> str:
        return self.rotulo
