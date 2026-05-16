from django.contrib import admin
from .models import PoliticaTi, FeatureFlag, JanelaManutencao, ParametroSistema, AvisoGlobal, LogBackup, AtivoTi, ChamadoTi

@admin.register(AtivoTi)
class AtivoTiAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "patrimonio", "status", "localizacao")
    list_filter = ("categoria", "status")
    search_fields = ("nome", "patrimonio", "numero_serie")

@admin.register(ChamadoTi)
class ChamadoTiAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "solicitante", "prioridade", "status", "data_criacao")
    list_filter = ("prioridade", "status", "data_criacao")
    search_fields = ("titulo", "descricao")
    list_editable = ("status", "prioridade")
    date_hierarchy = "data_criacao"

@admin.register(PoliticaTi)
class PoliticaTiAdmin(admin.ModelAdmin):
    list_display = ("id", "rotulo")

@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "ultima_alteracao")
    list_editable = ("ativo",)
    search_fields = ("nome", "descricao")
    list_filter = ("ativo",)

admin.site.register(JanelaManutencao)
admin.site.register(ParametroSistema)
admin.site.register(AvisoGlobal)
admin.site.register(LogBackup)
