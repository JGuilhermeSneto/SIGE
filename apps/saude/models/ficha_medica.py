from django.db import models
from apps.usuarios.models.perfis import Aluno
from django.contrib.auth import get_user_model
User = get_user_model()

class FichaMedica(models.Model):
    TIPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name='ficha_medica')
    tipo_sanguineo = models.CharField(max_length=3, choices=TIPO_SANGUINEO_CHOICES, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True, help_text="Liste as alergias separadas por vírgula.")
    medicamentos_continuos = models.TextField(blank=True, null=True)
    condicoes_pcd = models.BooleanField(default=False, verbose_name="Possui deficiência?")
    detalhes_pcd = models.CharField(max_length=255, blank=True, null=True)
    comprovante_pcd = models.FileField(upload_to='saude/pcd/', blank=True, null=True, verbose_name="Comprovante PCD")
    contato_emergencia_nome = models.CharField(max_length=100, blank=True, null=True)
    contato_emergencia_fone = models.CharField(max_length=20, blank=True, null=True)
    observacoes_medicas = models.TextField(blank=True, null=True)
    
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ficha Médica - {self.aluno.nome_completo}"

    class Meta:
        verbose_name = "Ficha Médica"
        verbose_name_plural = "Fichas Médicas"

class RegistroVacina(models.Model):
    ficha = models.ForeignKey(FichaMedica, on_delete=models.CASCADE, related_name='vacinas')
    nome_vacina = models.CharField(max_length=100)
    data_dose = models.DateField()
    lote = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_vacina} - {self.ficha.aluno.nome_completo}"

class AtestadoMedico(models.Model):
    """Representa um atestado médico enviado pelo aluno para justificativa de faltas."""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atestados')
    arquivo = models.FileField(upload_to='saude/atestados/', verbose_name="Arquivo do Atestado")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")
    descricao = models.TextField(blank=True, verbose_name="Observações")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    comentario_gestor = models.TextField(blank=True, verbose_name="Comentário do Gestor")
    
    data_submissao = models.DateTimeField(auto_now_add=True)
    data_analise = models.DateTimeField(null=True, blank=True)
    analisado_por = models.ForeignKey(
        'usuarios.Gestor', on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='atestados_analisados'
    )

    class Meta:
        db_table = 'core_atestadomedico'
        verbose_name = "Atestado Médico"
        verbose_name_plural = "Atestados Médicos"
        ordering = ["-data_submissao"]

    def __str__(self):
        return f"Atestado {self.usuario.get_full_name() or self.usuario.username} ({self.data_inicio} - {self.data_fim})"
