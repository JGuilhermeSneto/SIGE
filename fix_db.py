import os
import sys
import django

sys.path.append(r'c:\Users\gu268\Projetos\Django-projetos\SIGE')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        cursor.execute("ALTER TABLE axes_accesslog DROP COLUMN session_hash")
        print("Dropped session_hash from axes_accesslog")
    except Exception as e:
        print("Error dropping column:", e)
        
    try:
        cursor.execute("ALTER TABLE axes_accessattempt DROP COLUMN session_hash")
        print("Dropped session_hash from axes_accessattempt")
    except Exception as e:
        print("Error dropping column from accessattempt:", e)
