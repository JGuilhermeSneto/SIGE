import os
import sys
import django

sys.path.append(r'c:\Users\gu268\Projetos\Django-projetos\SIGE')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DESCRIBE axes_accesslog")
    rows = cursor.fetchall()
    print("Columns in axes_accesslog:")
    for row in rows:
        print(row)
