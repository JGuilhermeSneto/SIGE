from django.db import models
from django.core.validators import MinValueValidator

class UnidadeEscolar(models.Model):
    """Representa uma unidade física ou campus da escola."""
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, blank=True)
    eh_sede = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Unidade Escolar"
        verbose_name_plural = "Unidades Escolares"

    def __str__(self):
        return self.nome

class CategoriaBem(models.Model):
    """Categorias para itens de patrimônio (ex: Mobiliário, Eletrônicos)."""
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoria de Bem"
        verbose_name_plural = "Categorias de Bens"

    def __str__(self):
        return self.nome

class ItemPatrimonio(models.Model):
    """Itens duráveis da instituição (Inventário)."""
    ESTADO_CHOICES = [
        ('NOVO', 'Novo'),
        ('BOM', 'Bom'),
        ('REGULAR', 'Regular'),
        ('DANIFICADO', 'Danificado'),
        ('INSERVIVEL', 'Inservível'),
    ]
    
    tombamento = models.CharField(max_length=50, unique=True, verbose_name="Número de Patrimônio (Tombamento)")
    nome = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaBem, on_delete=models.PROTECT)
    unidade = models.ForeignKey(UnidadeEscolar, on_delete=models.PROTECT)
    estado_conservacao = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BOM')
    data_aquisicao = models.DateField(null=True, blank=True)
    valor_aquisicao = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'infra_patrimonio'
        verbose_name = "Item de Patrimônio"
        verbose_name_plural = "Itens de Patrimônio"

    def __str__(self):
        return f"[{self.tombamento}] {self.nome}"

class ItemEstoque(models.Model):
    """Itens de consumo (EPIs, Papelaria, Limpeza)."""
    nome = models.CharField(max_length=100)
    unidade_medida = models.CharField(max_length=20, default='unidade', help_text="Ex: Caixa, Pacote, Unidade")
    estoque_minimo = models.IntegerField(default=5)

    class Meta:
        db_table = 'infra_item_estoque'
        verbose_name = "Item de Estoque"
        verbose_name_plural = "Itens de Estoque"

    def __str__(self):
        return self.nome

class SaldoEstoque(models.Model):
    """Armazena o saldo de um item por unidade/campus."""
    item = models.ForeignKey(ItemEstoque, on_delete=models.CASCADE, related_name="saldos")
    unidade = models.ForeignKey(UnidadeEscolar, on_delete=models.CASCADE, related_name="saldos")
    quantidade = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = 'infra_saldo_estoque'
        unique_together = ('item', 'unidade')
        verbose_name = "Saldo em Estoque"
        verbose_name_plural = "Saldos em Estoque"

    def __str__(self):
        return f"{self.item.nome} em {self.unidade.nome}: {self.quantidade}"

class MovimentacaoEstoque(models.Model):
    """Registro de entradas e saídas de materiais."""
    TIPO_CHOICES = [('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')]
    
    item = models.ForeignKey(ItemEstoque, on_delete=models.CASCADE)
    unidade = models.ForeignKey(UnidadeEscolar, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    justificativa = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'infra_movimentacao_estoque'
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
