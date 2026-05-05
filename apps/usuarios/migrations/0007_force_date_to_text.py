from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_aluno_data_nascimento_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE core_professor MODIFY data_nascimento LONGTEXT;",
            reverse_sql="ALTER TABLE core_professor MODIFY data_nascimento DATE;"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE core_aluno MODIFY data_nascimento LONGTEXT;",
            reverse_sql="ALTER TABLE core_aluno MODIFY data_nascimento DATE;"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE core_gestor MODIFY data_nascimento LONGTEXT;",
            reverse_sql="ALTER TABLE core_gestor MODIFY data_nascimento DATE;"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE core_responsavel MODIFY data_nascimento LONGTEXT;",
            reverse_sql="ALTER TABLE core_responsavel MODIFY data_nascimento DATE;"
        ),
    ]
