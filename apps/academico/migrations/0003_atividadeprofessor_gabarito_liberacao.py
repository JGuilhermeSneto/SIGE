from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academico", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="atividadeprofessor",
            name="gabarito_liberado",
            field=models.BooleanField(
                default=False,
                help_text="Permite liberar gabarito manualmente antes do prazo.",
            ),
        ),
        migrations.AddField(
            model_name="atividadeprofessor",
            name="gabarito_liberado_em",
            field=models.DateTimeField(
                blank=True,
                help_text="Data/hora da liberação manual do gabarito.",
                null=True,
            ),
        ),
    ]
