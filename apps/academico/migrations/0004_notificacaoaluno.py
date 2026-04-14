from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academico", "0003_atividadeprofessor_gabarito_liberacao"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificacaoAluno",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("NOTA", "Nota lançada"), ("CHAMADA", "Chamada"), ("CORRECAO", "Correção"), ("GABARITO", "Gabarito")], max_length=20)),
                ("titulo", models.CharField(max_length=120)),
                ("mensagem", models.CharField(max_length=255)),
                ("url_destino", models.CharField(blank=True, max_length=255)),
                ("lida", models.BooleanField(default=False)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("aluno", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="notificacoes", to="usuarios.aluno")),
            ],
            options={
                "verbose_name": "Notificação do aluno",
                "verbose_name_plural": "Notificações dos alunos",
                "db_table": "core_notificacaoaluno",
                "ordering": ["-criado_em"],
            },
        ),
    ]
