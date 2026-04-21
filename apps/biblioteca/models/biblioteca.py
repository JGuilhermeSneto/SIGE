from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Professor

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, blank=True, null=True, verbose_name="ISBN")
    ano_publicacao = models.IntegerField(blank=True, null=True)
    editora = models.CharField(max_length=100, blank=True, null=True)
    capa = models.ImageField(upload_to='biblioteca/capas/', blank=True, null=True)
    quantidade_total = models.PositiveIntegerField(default=1)
    
    # Suporte Online/Digital
    arquivo_digital = models.FileField(upload_to='biblioteca/digitais/', blank=True, null=True, verbose_name="Arquivo PDF/Digital")
    url_digital = models.URLField(blank=True, null=True, verbose_name="Link para E-book/Conteúdo Online")
    
    data_cadastro = models.DateTimeField(default=timezone.now, verbose_name="Data de Entrada no Acervo")
    
    # quantidade_disponivel será calculada via property ou campo denormalizado
    
    def __str__(self):
        return self.titulo

    @property
    def exemplares_disponiveis(self):
        # Um livro não está disponível se estiver emprestado OU reservado
        ocupados = self.emprestimos.filter(
            models.Q(status='ATIVO') | models.Q(status='RESERVA'),
            data_devolucao_real__isnull=True
        ).count()
        return max(0, self.quantidade_total - ocupados)

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('DEVOLVIDO', 'Devolvido'),
        ('ATRASADO', 'Atrasado'),
        ('RESERVA', 'Reserva'),
    ]

    ESTADO_CONSERVACAO_CHOICES = [
        ('OTIMO',     'Ótimo / Perfeito'),
        ('RAZOAVEL',  'Razoável / Uso normal'),
        ('DANIFICADO', 'Danificado / Requer reparo'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='emprestimos')
    usuario_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True)
    usuario_professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    
    STATUS_LEITURA_CHOICES = [
        ('NAO_INFORMADO', 'Apenas Devolvido'),
        ('LENDO',         'Estava Lendo'),
        ('FINALIZADO',    'Finalizou a Leitura'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    status_leitura = models.CharField(
        max_length=15,
        choices=STATUS_LEITURA_CHOICES,
        default='NAO_INFORMADO',
        verbose_name='Status de Leitura'
    )
    
    estado_conservacao = models.CharField(
        max_length=10,
        choices=ESTADO_CONSERVACAO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Estado de Conservação na Devolução'
    )

    def __str__(self):
        destinatario = self.usuario_aluno.nome_completo if self.usuario_aluno else self.usuario_professor.nome_completo
        return f"{self.livro.titulo} -> {destinatario}"
