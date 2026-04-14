from django.db import models

class EventoCalendario(models.Model):
    """Representa um dia no calendário acadêmico com seu respectivo status."""
    
    TIPO_CHOICES = [
        ('DI_LETIVO', 'Dia Letivo'),
        ('FERIADO', 'Feriado'),
        ('PROVA', 'Semana de Prova'),
        ('SABADO_LETIVO', 'Sábado Letivo'),
        ('RECESSO', 'Recesso / Férias'),
        ('FIM_SEMANA', 'Final de Semana'),
    ]

    data = models.DateField(unique=True, help_text="Data do evento")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='DI_LETIVO')
    descricao = models.CharField(max_length=255, blank=True, help_text="Descrição (ex: Feriado Local, Nome da Prova)")
    aula_suspensa = models.BooleanField(default=False, help_text="Indica se as aulas estão suspensas neste dia")

    class Meta:
        db_table = 'core_eventocalendario'
        verbose_name = "Evento de Calendário"
        verbose_name_plural = "Eventos de Calendário"
        ordering = ['data']

    def __str__(self):
        return f"{self.data} - {self.get_tipo_display()}"
