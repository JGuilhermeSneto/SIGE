from django.db import models

class Instituicao(models.Model):
    """
    O 'Tenant' principal do sistema. Representa uma escola ou rede de ensino.
    """
    nome = models.CharField(max_length=255, help_text="Nome da Instituição")
    cnpj = models.CharField(max_length=18, unique=True, help_text="CNPJ da Instituição")
    slug = models.SlugField(unique=True, help_text="Identificador único para URL (ex: escola-padrao)")
    
    logo = models.ImageField(upload_to="instituicao/logos/", blank=True, null=True)
    
    # Configurações de plano/limites (Escalabilidade)
    ativo = models.BooleanField(default=True)
    max_alunos = models.PositiveIntegerField(default=500, help_text="Limite de alunos para este contrato")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.nome

class TenantModel(models.Model):
    """
    Mixin abstrato que deve ser herdado por quase todos os modelos do sistema.
    Garante que cada registro pertença a uma instituição específica.
    """
    instituicao = models.ForeignKey(
        'comum.Instituicao', 
        on_delete=models.CASCADE, 
        related_name="%(class)s_related",
        null=True, blank=True,
        db_index=True,
        help_text="Instituição à qual este registro pertence"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not hasattr(self, 'instituicao') or self.instituicao is None:
            from apps.comum.middleware.tenant_middleware import get_current_tenant
            tenant = get_current_tenant()
            if tenant:
                self.instituicao = tenant
        super().save(*args, **kwargs)
