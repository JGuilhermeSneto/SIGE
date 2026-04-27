import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def use_dummy_cache(settings):
    """Garante que os testes usem cache em memória, evitando erros de conexão com o Redis."""
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    # Desativa Celery em modo síncrono para testes
    settings.CELERY_TASK_ALWAYS_EAGER = True
