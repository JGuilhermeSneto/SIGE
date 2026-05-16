from django.db import models
from django.utils.translation import gettext_lazy as _

class FunnelStage(models.Model):
    name = models.CharField(_("Nome da Etapa"), max_length=100)
    order = models.PositiveIntegerField(_("Ordem"), default=0)
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Etapa do Funil")
        verbose_name_plural = _("Etapas do Funil")
        ordering = ["order"]

    def __str__(self):
        return self.name

class Lead(models.Model):
    SOURCE_CHOICES = [
        ("site", _("Site / Formulário")),
        ("indicacao", _("Indicação")),
        ("redes_sociais", _("Redes Sociais")),
        ("presencial", _("Presencial")),
        ("outro", _("Outro")),
    ]

    name = models.CharField(_("Nome do Interessado"), max_length=255)
    email = models.EmailField(_("E-mail"), blank=True)
    phone = models.CharField(_("Telefone"), max_length=20)
    student_name = models.CharField(_("Nome do Aluno"), max_length=255, blank=True)
    student_grade = models.CharField(_("Série de Interesse"), max_length=100, blank=True)
    source = models.CharField(_("Origem"), max_length=50, choices=SOURCE_CHOICES, default="site")
    stage = models.ForeignKey(FunnelStage, on_delete=models.PROTECT, verbose_name=_("Etapa Atual"), related_name="leads")
    notes = models.TextField(_("Observações"), blank=True)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")

    def __str__(self):
        return f"{self.name} - {self.student_name}"

class LeadInteraction(models.Model):
    TYPE_CHOICES = [
        ("call", _("Ligação")),
        ("whatsapp", _("WhatsApp")),
        ("email", _("E-mail")),
        ("visit", _("Visita Presencial")),
        ("meeting", _("Reunião")),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="interactions")
    type = models.CharField(_("Tipo de Interação"), max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(_("Descrição da Interação"))
    date = models.DateTimeField(_("Data/Hora"), auto_now_add=True)

    class Meta:
        verbose_name = _("Interação com Lead")
        verbose_name_plural = _("Interações com Leads")
