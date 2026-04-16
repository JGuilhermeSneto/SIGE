from django.contrib import admin
from .models import (
    UnidadeEscolar, CategoriaBem, ItemPatrimonio, 
    ItemEstoque, SaldoEstoque, MovimentacaoEstoque
)

@admin.register(UnidadeEscolar)
class UnidadeEscolarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'eh_sede', 'endereco')

@admin.register(CategoriaBem)
class CategoriaBemAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(ItemPatrimonio)
class ItemPatrimonioAdmin(admin.ModelAdmin):
    list_display = ('tombamento', 'nome', 'categoria', 'unidade', 'estado_conservacao', 'data_aquisicao')
    list_filter = ('categoria', 'unidade', 'estado_conservacao')
    search_fields = ('tombamento', 'nome')

class SaldoEstoqueInline(admin.TabularInline):
    model = SaldoEstoque
    extra = 0
    readonly_fields = ('quantidade',)
    can_delete = False

@admin.register(ItemEstoque)
class ItemEstoqueAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade_medida', 'estoque_minimo')
    inlines = [SaldoEstoqueInline]

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('item', 'unidade', 'tipo', 'quantidade', 'data')
    list_filter = ('tipo', 'unidade', 'data')
    
    def save_model(self, request, obj, form, change):
        # Lógica de atualização automática de saldo
        saldo, created = SaldoEstoque.objects.get_or_create(
            item=obj.item, 
            unidade=obj.unidade
        )
        if obj.tipo == 'ENTRADA':
            saldo.quantidade += obj.quantidade
        else:
            saldo.quantidade -= obj.quantidade
        saldo.save()
        super().save_model(request, obj, form, change)
