from django.contrib import admin

from .models import PoliticaTi


@admin.register(PoliticaTi)
class PoliticaTiAdmin(admin.ModelAdmin):
    list_display = ("id", "rotulo")
