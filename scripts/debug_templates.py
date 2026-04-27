import os
import django
from django.conf import settings
from django.template import engines

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

engine = engines['django']
print("Template DIRS:", engine.engine.dirs)
print("App Directories:")
for loader in engine.engine.template_loaders:
    if hasattr(loader, 'get_dirs'):
        for d in loader.get_dirs():
            print(f" - {d}")
