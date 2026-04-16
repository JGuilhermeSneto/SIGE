from django.db import models
from apps.usuarios.models.perfis import Aluno

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
