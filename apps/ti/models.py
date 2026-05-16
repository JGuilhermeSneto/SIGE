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


class AtivoTi(models.Model):
    CATEGORIAS = [
        ('HARDWARE', 'Hardware'),
        ('SOFTWARE', 'Software/Licença'),
        ('REDE', 'Equipamento de Rede'),
        ('PERIFERICO', 'Periférico'),
    ]
    STATUS = [
        ('ATIVO', 'Em Uso'),
        ('MANUTENCAO', 'Em Manutenção'),
        ('ESTOQUE', 'Em Estoque'),
        ('BAIXADO', 'Baixado/Sucata'),
    ]
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    patrimonio = models.CharField(max_length=50, unique=True, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    localizacao = models.CharField(max_length=200, help_text="Ex: Sala de Informática, Secretaria")
    status = models.CharField(max_length=20, choices=STATUS, default='ATIVO')
    data_aquisicao = models.DateField(null=True, blank=True)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ativo de TI"
        verbose_name_plural = "Ativos de TI"

    def __str__(self):
        return f"{self.nome} ({self.patrimonio or 'S/P'})"


class ChamadoTi(models.Model):
    PRIORIDADES = [('BAIXA', 'Baixa'), ('MEDIA', 'Média'), ('ALTA', 'Alta'), ('URGENTE', 'Urgente')]
    STATUS = [
        ('ABERTO', 'Aberto'),
        ('EM_ATENDIMENTO', 'Em Atendimento'),
        ('AGUARDANDO_TERCEIRO', 'Aguardando Terceiro'),
        ('RESOLVIDO', 'Resolvido'),
        ('FECHADO', 'Fechado'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    solicitante = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='chamados_ti_abertos')
    tecnico_responsavel = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados_ti_atribuidos')
    ativo_relacionado = models.ForeignKey(AtivoTi, on_delete=models.SET_NULL, null=True, blank=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES, default='MEDIA')
    status = models.CharField(max_length=20, choices=STATUS, default='ABERTO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)
    solucao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Chamado de TI"
        verbose_name_plural = "Chamados de TI"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"#{self.id} - {self.titulo} ({self.status})"


class ConfiguracaoSeguranca(models.Model):
    """Configurações globais de defesa proativa (SOC)."""
    BLOQUEIO_PAISES_OPCOES = [
        ('NENHUM', 'Nenhum'),
        ('SOMENTE_BR', 'Somente Brasil'),
        ('LISTA_NEGRA', 'Bloquear Lista Negra'),
    ]
    bloqueio_geografico = models.CharField(max_length=20, choices=BLOQUEIO_PAISES_OPCOES, default='NENHUM')
    paises_bloqueados = models.TextField(blank=True, help_text="Códigos ISO separados por vírgula (Ex: US,CN,RU)")
    limite_download_mb_minuto = models.PositiveIntegerField(default=100, help_text="Alerta de exfiltração se ultrapassado")
    alerta_fingerprint_novo = models.BooleanField(default=True, verbose_name="Alertar novo dispositivo")
    honeypot_ativo = models.BooleanField(default=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração SOC"
        verbose_name_plural = "Configurações SOC"


class RegraWAF(models.Model):
    """Regras do Web Application Firewall Customizado."""
    nome = models.CharField(max_length=100)
    padrao_regex = models.CharField(max_length=255, help_text="Regex para detectar ataque (Ex: SELECT|DROP|UNION)")
    acao = models.CharField(max_length=20, choices=[('BLOQUEAR', 'Bloquear IP'), ('LOGAR', 'Apenas Logar')], default='BLOQUEAR')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class CofreSegredo(models.Model):
    """Armazenamento de chaves e credenciais sensíveis."""
    servico = models.CharField(max_length=100, unique=True)
    chave_publica = models.CharField(max_length=255, blank=True)
    valor_criptografado = models.TextField()
    descricao = models.TextField(blank=True)
    ultima_leitura = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Cofre de Segredo"
        verbose_name_plural = "Cofre de Segredos"


class HoneyToken(models.Model):
    """Arquivos armadilha para detectar espionagem."""
    nome_arquivo = models.CharField(max_length=100)
    caminho_fake = models.CharField(max_length=255)
    total_acessos = models.PositiveIntegerField(default=0)
    ultimo_acesso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome_arquivo


class FingerprintDispositivo(models.Model):
    """Assinatura única de navegadores para detecção de invasão."""
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assinatura_hash = models.CharField(max_length=64)
    navegador = models.CharField(max_length=255)
    sistema_operacional = models.CharField(max_length=100)
    confiavel = models.BooleanField(default=False)
    data_visto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'assinatura_hash')
