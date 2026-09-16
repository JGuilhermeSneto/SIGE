import os
import sys
import django

sys.path.append(r'c:\Users\gu268\Projetos\Django-projetos\SIGE')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME = 'session_hash'")
    rows = cursor.fetchall()
    print("Tables with session_hash:", [row[0] for row in rows])
