from django.db import migrations


def run_mysql_modify(sql, reverse_sql=None):
    def inner(apps, schema_editor):
        if schema_editor.connection.vendor == "mysql":
            schema_editor.execute(sql)

    def inner_reverse(apps, schema_editor):
        if schema_editor.connection.vendor == "mysql" and reverse_sql:
            schema_editor.execute(reverse_sql)

    return migrations.RunPython(inner, reverse_code=inner_reverse)


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0006_alter_aluno_data_nascimento_and_more"),
    ]

    operations = [
        run_mysql_modify(
            "ALTER TABLE core_professor MODIFY data_nascimento LONGTEXT;",
            "ALTER TABLE core_professor MODIFY data_nascimento DATE;",
        ),
        run_mysql_modify(
            "ALTER TABLE core_aluno MODIFY data_nascimento LONGTEXT;",
            "ALTER TABLE core_aluno MODIFY data_nascimento DATE;",
        ),
        run_mysql_modify(
            "ALTER TABLE core_gestor MODIFY data_nascimento LONGTEXT;",
            "ALTER TABLE core_gestor MODIFY data_nascimento DATE;",
        ),
        run_mysql_modify(
            "ALTER TABLE core_responsavel MODIFY data_nascimento LONGTEXT;",
            "ALTER TABLE core_responsavel MODIFY data_nascimento DATE;",
        ),
    ]
