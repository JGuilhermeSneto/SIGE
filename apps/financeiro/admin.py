from django.contrib import admin
from .models import Fatura, Pagamento

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    readonly_fields = ('data_pagamento',)

@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'valor', 'data_vencimento', 'status', 'esta_atrasada')
    list_filter = ('status', 'data_vencimento')
    search_fields = ('aluno__nome_completo', 'descricao')
    inlines = [PagamentoInline]
    actions = ['marcar_como_pago']

    def marcar_como_pago(self, request, queryset):
        queryset.update(status='PAGO')
    marcar_como_pago.short_description = "Marcar faturas selecionadas como pagas"

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fatura', 'valor_pago', 'data_pagamento', 'metodo')
    list_filter = ('metodo', 'data_pagamento')
    search_fields = ('fatura__aluno__nome_completo', 'transacao_id')
