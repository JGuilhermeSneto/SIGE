from django.db import models

class PoliticaTi(models.Model):
    rotulo = models.CharField(max_length=100)
    conteudo = models.TextField(default="")

    def __str__(self):
        return self.rotulo

class FeatureFlag(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Identificador (slug)")
    descricao = models.TextField(blank=True, verbose_name="Para que serve?")
    ativo = models.BooleanField(default=True, verbose_name="Está ativo?")
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feature Flag"
        verbose_name_plural = "Feature Flags"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome}"

class JanelaManutencao(models.Model):
    titulo = models.CharField(max_length=200)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    bloquear_acesso = models.BooleanField(default=True)
    aviso_banner = models.BooleanField(default=True)
    concluida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Janela de Manutenção"
        verbose_name_plural = "Janelas de Manutenção"
        ordering = ['-inicio']

    def __str__(self):
        return f"{self.titulo} ({self.inicio.strftime('%d/%m %H:%M')})"

class ParametroSistema(models.Model):
    chave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descricao = models.TextField(blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Parâmetro do Sistema"
        verbose_name_plural = "Parâmetros do Sistema"

    def __str__(self):
        return self.chave

class AvisoGlobal(models.Model):
    TIPOS = [('INFO', 'Informativo'), ('ALERTA', 'Alerta'), ('CRITICO', 'Crítico')]
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPOS, default='INFO')
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Aviso Global"
        verbose_name_plural = "Avisos Globais"

    def __str__(self):
        return self.titulo


class LogBackup(models.Model):
    STATUS = [('SUCESSO', 'Sucesso'), ('FALHA', 'Falha'), ('EM_CURSO', 'Em Curso')]
    arquivo = models.CharField(max_length=255)
    tamanho_bytes = models.BigIntegerField(default=0)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='EM_CURSO')
    storage_path = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Log de Backup"
        verbose_name_plural = "Logs de Backups"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Backup {self.data_inicio.strftime('%d/%m/%Y %H:%M')} - {self.status}"
