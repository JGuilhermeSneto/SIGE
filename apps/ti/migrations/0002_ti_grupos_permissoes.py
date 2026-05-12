from django.db import migrations


def criar_grupos_ti(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ct = ContentType.objects.filter(app_label="ti", model="politicati").first()
    if not ct:
        return
    perms = {p.codename: p for p in Permission.objects.filter(content_type=ct)}
    g_op, _ = Group.objects.get_or_create(name="TI — Operador")
    g_co, _ = Group.objects.get_or_create(name="TI — Coordenação")
    if "painel_ti_basico" in perms:
        g_op.permissions.add(perms["painel_ti_basico"])
        g_co.permissions.add(perms["painel_ti_basico"])
    if "painel_ti_operacoes" in perms:
        g_co.permissions.add(perms["painel_ti_operacoes"])


def remover_grupos_ti(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["TI — Operador", "TI — Coordenação"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("ti", "0001_initial"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar_grupos_ti, remover_grupos_ti),
    ]
