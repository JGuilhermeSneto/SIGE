from django.db import models
from apps.usuarios.models.perfis import Aluno
from django.utils import timezone

class Fatura(models.Model):
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
    link_pagamento = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fatura {self.id} - {self.aluno.nome_completo} - {self.status}"

    @property
    def esta_atrasada(self):
        return self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date()

class Pagamento(models.Model):
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
    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True)
    transacao_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pagamento {self.id} - Fatura {self.fatura.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ao registrar um pagamento total, marca a fatura como paga
        if self.fatura.pagamentos.aggregate(total=models.Sum('valor_pago'))['total'] >= self.fatura.valor:
            self.fatura.status = 'PAGO'
            self.fatura.save()
