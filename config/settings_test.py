from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# Desativa Axe para testes se estiver causando lentidão
AXES_ENABLED = False

# Usa cache em memória
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery síncrono
CELERY_TASK_ALWAYS_EAGER = True
