from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_force_date_to_text'),
    ]

    operations = [
        # Tabelas Principais (Reforço)
        migrations.RunSQL("ALTER TABLE core_professor MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE core_aluno MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE core_gestor MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE core_responsavel MODIFY data_nascimento LONGTEXT;"),
        
        # Tabelas Históricas
        migrations.RunSQL("ALTER TABLE usuarios_historicalprofessor MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE usuarios_historicalaluno MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE usuarios_historicalgestor MODIFY data_nascimento LONGTEXT;"),
        migrations.RunSQL("ALTER TABLE usuarios_historicalresponsavel MODIFY data_nascimento LONGTEXT;"),
    ]
