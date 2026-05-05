from django.db import migrations

def run_mysql_modify(sql, reverse_sql=None):
    def inner(apps, schema_editor):
        if schema_editor.connection.vendor == 'mysql':
            schema_editor.execute(sql)
    
    def inner_reverse(apps, schema_editor):
        if schema_editor.connection.vendor == 'mysql' and reverse_sql:
            schema_editor.execute(reverse_sql)
            
    return migrations.RunPython(inner, reverse_code=inner_reverse)

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_force_date_to_text'),
    ]

    operations = [
        # Tabelas Principais (Reforço)
        run_mysql_modify("ALTER TABLE core_professor MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE core_aluno MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE core_gestor MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE core_responsavel MODIFY data_nascimento LONGTEXT;"),
        
        # Tabelas Históricas
        run_mysql_modify("ALTER TABLE usuarios_historicalprofessor MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE usuarios_historicalaluno MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE usuarios_historicalgestor MODIFY data_nascimento LONGTEXT;"),
        run_mysql_modify("ALTER TABLE usuarios_historicalresponsavel MODIFY data_nascimento LONGTEXT;"),
    ]
