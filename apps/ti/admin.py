from django.contrib import admin
from .models import PoliticaTi, FeatureFlag


@admin.register(PoliticaTi)
class PoliticaTiAdmin(admin.ModelAdmin):
    list_display = ("id", "rotulo")


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "ultima_alteracao")
    list_editable = ("ativo",)
    search_fields = ("nome", "descricao")
    list_filter = ("ativo",)
