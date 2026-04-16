from django.contrib import admin
from .models.comunicado import Comunicado

@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publico_alvo', 'data_publicacao', 'data_expiracao', 'importancia', 'esta_ativo')
    list_filter = ('publico_alvo', 'importancia', 'data_publicacao')
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_publicacao'
    
    fieldsets = (
        (None, {
            'fields': ('titulo', 'conteudo')
        }),
        ('Configurações de Exibição', {
            'fields': ('publico_alvo', 'importancia', 'data_expiracao')
        }),
        ('Informações de Controle', {
            'fields': ('data_publicacao', 'autor'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.autor and hasattr(request.user, 'gestor'):
            obj.autor = request.user.gestor
        super().save_model(request, obj, form, change)
