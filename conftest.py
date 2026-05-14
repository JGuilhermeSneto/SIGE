import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def use_dummy_cache(settings):
    """Garante que os testes usem cache em memória e Celery síncrono."""
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.AXES_ENABLED = False
