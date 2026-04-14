"""
Tag do Django para carregar ativos do Vite em produção.

O Vite gera um manifesto JSON em ``apps/comum/static/vite/manifest.json``.
Este helper resolve o caminho do asset e garante que o template use a URL de
static correta do Django.
"""

import json
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

MANIFEST_PATH = Path(settings.BASE_DIR) / "apps" / "comum" / "static" / "vite" / "manifest.json"


def load_vite_manifest():
    try:
        with MANIFEST_PATH.open("r", encoding="utf-8") as manifest_file:
            return json.load(manifest_file)
    except FileNotFoundError:
        return {}


def resolve_manifest_entry(entry_name: str):
    manifest = load_vite_manifest()
    return manifest.get(entry_name)


@register.simple_tag(name="vite_asset")
def vite_asset(entry_name: str):
    """Retorna a URL estática do bundle principal do Vite."""
    entry = resolve_manifest_entry(entry_name)
    if not entry:
        return ""
    return static(f"vite/{entry['file']}")


@register.simple_tag(name="vite_css")
def vite_css(entry_name: str):
    """Retorna tags <link> para os arquivos CSS do build do Vite."""
    entry = resolve_manifest_entry(entry_name)
    if not entry or not entry.get("css"):
        return ""

    tags = [f'<link rel="stylesheet" href="{static(f"vite/{css}")}">' for css in entry["css"]]
    return mark_safe("\n".join(tags))


@register.simple_tag(name="vite_js")
def vite_js(entry_name: str):
    """Retorna tag <script> para o bundle JavaScript do Vite."""
    entry = resolve_manifest_entry(entry_name)
    if not entry:
        return ""
    return mark_safe(f'<script type="module" src="{static(f"vite/{entry["file"]}")}"></script>')


@register.simple_tag(name="vite_entry")
def vite_entry(entry_name: str):
    """Retorna os assets Vite corretos para desenvolvimento ou produção."""
    if settings.DEBUG:
        dev_url = getattr(settings, "VITE_DEV_SERVER_URL", "http://127.0.0.1:5173")
        return mark_safe(
            f'<script type="module" src="{dev_url}/@vite/client"></script>\n'
            f'<script type="module" src="{dev_url}/{entry_name}"></script>'
        )

    css_tags = vite_css(entry_name)
    js_tag = vite_js(entry_name)
    return mark_safe("\n".join([tag for tag in [css_tags, js_tag] if tag]))
