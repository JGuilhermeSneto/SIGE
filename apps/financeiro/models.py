from django.db import models
from apps.usuarios.models.perfis import Aluno
from django.utils import timezone
from apps.comum.utils.fields import EncryptedURLField, EncryptedCharField
from simple_history.models import HistoricalRecords

class CategoriaFinanceira(models.Model):
    """Categorias de Receitas e Despesas (Ex: Energia, Salários, Mensalidade, Impostos)."""
    TIPO_CHOICES = [('RECEITA', 'Receita'), ('DESPESA', 'Despesa')]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True)

    class Meta:
        db_table = 'fin_categoria'
        verbose_name = "Categoria Financeira"
        verbose_name_plural = "Categorias Financeiras"

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class CentroCusto(models.Model):
    """Departamentos ou áreas que geram custos (Administrativo, Pedagógico, Infraestrutura)."""
    nome = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'fin_centro_custo'
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custo"

    def __str__(self):
        return self.nome

class Fatura(models.Model):
    """Contas a Receber (Principalmente Mensalidades)."""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='faturas')
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    link_pagamento = EncryptedURLField(blank=True, null=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    @property
    def esta_atrasada(self):
        return self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date()

    class Meta:
        db_table = 'fin_fatura'

    def __str__(self):
        return f"Fatura {self.id} - {self.aluno.nome_completo} - {self.status}"

class Lancamento(models.Model):
    """Livro Diário: Todas as entradas e saídas financeiras da escola."""
    tipo = models.CharField(max_length=10, choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')])
    categoria = models.ForeignKey(CategoriaFinanceira, on_delete=models.PROTECT)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True, blank=True)
    
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_pagamento = models.DateField(default=timezone.now)
    descricao = models.CharField(max_length=255)
    
    # Rastreabilidade
    autorizado_por = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="autorizacoes_fin")
    item_patrimonio = models.ForeignKey("infraestrutura.ItemPatrimonio", on_delete=models.SET_NULL, null=True, blank=True)
    fatura_origem = models.ForeignKey(Fatura, on_delete=models.SET_NULL, null=True, blank=True)
    
    comprovante = models.FileField(upload_to='financeiro/comprovantes/', blank=True, null=True)
    
    history = HistoricalRecords()

    class Meta:
        db_table = 'fin_lancamento'
        verbose_name = "Lançamento"
        verbose_name_plural = "Lançamentos"

    def __str__(self):
        return f"[{self.tipo}] {self.descricao} - R$ {self.valor}"

class FolhaPagamento(models.Model):
    """Controle de salários e encargos de funcionários."""
    funcionario = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="folhas_pagamento")
    mes_referencia = models.IntegerField()
    ano_referencia = models.IntegerField()
    
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descontos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impostos_encargos = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="INSS, FGTS, etc.")
    
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'fin_folha_pagamento'
        unique_together = ('funcionario', 'mes_referencia', 'ano_referencia')
        verbose_name = "Folha de Pagamento"
        verbose_name_plural = "Folhas de Pagamento"

    @property
    def salario_liquido(self):
        return (self.salario_base + self.bonus) - (self.descontos + self.impostos_encargos)

class Pagamento(models.Model):
    """Registro detalhado de como uma Fatura foi liquidada."""
    METODO_CHOICES = [
        ('BOLETO', 'Boleto'),
        ('PIX', 'Pix'),
        ('CARTAO', 'Cartão de Crédito'),
        ('DINHEIRO', 'Dinheiro'),
    ]

    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='pagamentos')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(default=timezone.now)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    comprovante = models.FileField(upload_to='financeiro/pagamentos/', blank=True, null=True)
    transacao_id = EncryptedCharField(max_length=500, blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'fin_pagamento_fatura'

    def __str__(self):
        return f"Pagamento {self.id} - Fatura {self.fatura.id}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Sincroniza com o Livro Diário (Lancamento)
        if is_new:
            cat_mensalidade, _ = CategoriaFinanceira.objects.get_or_create(nome="Mensalidade Aluno", tipo="RECEITA")
            Lancamento.objects.create(
                tipo='ENTRADA',
                categoria=cat_mensalidade,
                valor=self.valor_pago,
                data_pagamento=self.data_pagamento.date(),
                descricao=f"Recebimento: {self.fatura.descricao} - {self.fatura.aluno.nome_completo}",
                autorizado_por=self.fatura.aluno.user, # Simplificação para o registro
                fatura_origem=self.fatura
            )

        # Atualiza status da fatura
        total_pago = self.fatura.pagamentos.aggregate(total=models.Sum('valor_pago'))['total'] or 0
        if total_pago >= self.fatura.valor:
            self.fatura.status = 'PAGO'
            self.fatura.save()
