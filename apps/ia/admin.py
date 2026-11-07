from django.contrib import admin
from .models import SessaoAssistente, MensagemAssistente, PropostaDecisao


class MensagemAssistenteInline(admin.TabularInline):
    model = MensagemAssistente
    extra = 0
    readonly_fields = ("papel", "conteudo", "contexto_utilizado", "latencia_segundos", "criado_em")
    can_delete = False


@admin.register(SessaoAssistente)
class SessaoAssistenteAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "ativo", "criado_em", "atualizado_em")
    list_filter = ("ativo", "criado_em")
    search_fields = ("titulo", "usuario__username", "usuario__email")
    inlines = [MensagemAssistenteInline]


@admin.register(MensagemAssistente)
class MensagemAssistenteAdmin(admin.ModelAdmin):
    list_display = ("id", "sessao", "papel", "conteudo_resumo", "latencia_segundos", "criado_em")
    list_filter = ("papel", "criado_em")
    search_fields = ("conteudo", "sessao__titulo", "sessao__usuario__username")

    def conteudo_resumo(self, obj):
        return obj.conteudo[:80] + "..." if len(obj.conteudo) > 80 else obj.conteudo
    conteudo_resumo.short_description = "Conteúdo"


@admin.register(PropostaDecisao)
class PropostaDecisaoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "tipo", "status", "decidido_por", "decidido_em", "criado_em")
    list_filter = ("tipo", "status", "criado_em")
    search_fields = ("titulo", "descricao", "justificativa")
    readonly_fields = ("criado_em",)

