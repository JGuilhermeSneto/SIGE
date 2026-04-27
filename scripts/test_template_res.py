import os
import django
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    t = get_template('financeiro/listar_faturas.html')
    print("SUCCESS: Template found at", t.origin.name)
except Exception as e:
    print("FAILURE:", e)
