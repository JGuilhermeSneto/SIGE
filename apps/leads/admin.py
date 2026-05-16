from django.contrib import admin
from .models import Lead, FunnelStage, LeadInteraction

@admin.register(FunnelStage)
class FunnelStageAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)

class InteractionInline(admin.TabularInline):
    model = LeadInteraction
    extra = 1

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "student_name", "stage", "source", "created_at")
    list_filter = ("stage", "source", "created_at")
    search_fields = ("name", "student_name", "email", "phone")
    inlines = [InteractionInline]
