import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.biblioteca.models.biblioteca import Livro
print(f'Total: {Livro.objects.count()}, Com capa: {Livro.objects.exclude(capa="").count()}')
