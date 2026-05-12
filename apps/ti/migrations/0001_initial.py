# Generated manually — modelo de permissões da área de TI

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="PoliticaTi",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rotulo", models.CharField(default="default", max_length=64, unique=True)),
            ],
            options={
                "verbose_name": "Política de TI",
                "verbose_name_plural": "Políticas de TI",
                "default_permissions": (),
                "permissions": [
                    ("painel_ti_basico", "Acessar painel da equipe de TI"),
                    ("painel_ti_operacoes", "Acessar operações avançadas de TI"),
                ],
            },
        ),
    ]
