from django.db import models
from django.utils import timezone

class Comunicado(models.Model):
    """Representa um aviso ou comunicado no mural do sistema."""
    
    PUBLICO_CHOICES = [
        ('GLOBAL', 'Global (Todos)'),
        ('ALUNOS', 'Apenas Alunos'),
        ('PROFESSORES', 'Apenas Professores'),
        ('GESTORES', 'Apenas Gestores'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
    data_expiracao = models.DateField(null=True, blank=True, verbose_name="Data de Expiração")
    publico_alvo = models.CharField(
        max_length=20, 
        choices=PUBLICO_CHOICES, 
        default='GLOBAL', 
        verbose_name="Público Alvo"
    )
    autor = models.ForeignKey(
        "usuarios.Gestor", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="comunicados_criados"
    )
    
    importancia = models.CharField(
        max_length=20,
        choices=[('NORMAL', 'Normal'), ('ALTA', 'Alta / Urgente')],
        default='NORMAL'
    )

    class Meta:
        db_table = 'core_comunicado'
        verbose_name = "Comunicado"
        verbose_name_plural = "Comunicados"
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo

    @property
    def esta_ativo(self):
        if self.data_expiracao:
            return self.data_expiracao >= timezone.now().date()
        return True
