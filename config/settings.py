import os
import sys
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv
import sentry_sdk
import dj_database_url
from sentry_sdk.integrations.django import DjangoIntegration

# Inicialização do Sentry (Opcional)
SENTRY_DSN = config("SENTRY_DSN", default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = config("SECRET_KEY", default="django-insecure-default-key-change-it")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Apps
INSTALLED_APPS = [
    "daphne",                           # deve vir antes do staticfiles (Channels/ASGI)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.usuarios",
    "apps.academico",
    "apps.calendario",
    "apps.comum",
    "apps.comunicacao",
    "apps.documentos",
    "apps.infraestrutura",
    "apps.saude",
    "apps.biblioteca",
    "apps.dashboards",
    "apps.financeiro",
    "widget_tweaks",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "axes",
    "cloudinary",
    "cloudinary_storage",
    "zxcvbn_password",
    "simple_history",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",
    "apps.seguranca",
    "apps.ti",
    "apps.leads",
    "apps.notifications",
    "django_prometheus",
    "health_check",              # API unificada (v4.x) — usa /health/ endpoint
    "channels",
    "impersonate",
]

# Middleware (Ordem do Prometheus é importante)
MIDDLEWARE = [
    "apps.seguranca.middleware.SecurityShieldMiddleware",
    "apps.ti.middleware.ManutencaoMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "csp.middleware.CSPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "apps.seguranca.middleware.Force2FAMiddleware",
    "apps.seguranca.middleware.SecurityHardeningMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "apps.seguranca.middleware.ManutencaoMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "apps.comum.middleware.tenant_middleware.TenantMiddleware",
    "apps.seguranca.middleware.BlacklistMiddleware",
    "apps.seguranca.middleware.AuditMiddleware",
    "apps.seguranca.middleware.ExceptionMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "apps.usuarios.backends.MatriculaAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.usuarios.context_processors.notificacoes_sige",
            ],
            "libraries": {
                "custom_tags": "apps.comum.templatetags.custom_tags",
                "get_item": "apps.comum.templatetags.get_item",
                "vite_assets": "apps.comum.templatetags.vite_assets",
                "ti_tags": "apps.ti.templatetags.ti_tags",
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Django Channels — Layer para WebSockets
if config("USE_REDIS", default=False, cast=bool):
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [config("REDIS_URL", default="redis://127.0.0.1:6379/0")],
            },
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

# Banco de Dados
TESTING = 'test' in sys.argv or 'pytest' in sys.argv or any('pytest' in arg for arg in sys.argv)
if TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    AXES_ENABLED = False
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
    ]
    # Remove Middlewares que podem causar redirecionamentos ou bloqueios durante testes
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "apps.comum.middleware.tenant_middleware.TenantMiddleware",
    ]
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Se o banco for MySQL (via Aiven), garante que o Django use o motor correto se a URL começar com mysql
if DATABASES["default"].get("ENGINE") == "django.db.backends.mysql":
    DATABASES["default"]["OPTIONS"] = {  # type: ignore[assignment]
        "charset": "utf8mb4",
    }
elif "mysql" in DATABASES["default"].get("ENGINE", ""):
    DATABASES["default"]["ENGINE"] = "django.db.backends.mysql"

# Auth
LOGIN_URL = "two_factor:login"
LOGIN_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "zxcvbn_password.validators.ZXCVBNValidator"},
]

# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Estáticos e Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "apps" / "comum" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise para estáticos em produção
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache (Redis vs Local)
if config("USE_REDIS", default=False, cast=bool):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "sige-local-cache",
        }
    }

# Cloudinary (só ativa se as credenciais estiverem configuradas)
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

USE_CLOUDINARY_STORAGE = all(CLOUDINARY_STORAGE.values())
if USE_CLOUDINARY_STORAGE:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Servir uploads locais quando não há Cloudinary (dev e Render sem CDN)
SERVE_MEDIA_FILES = config(
    "SERVE_MEDIA_FILES", default=not USE_CLOUDINARY_STORAGE, cast=bool
)

# Push Notifications (FCM & APNs)
FCM_SERVER_KEY = config("FCM_SERVER_KEY", default="")
APNS_CERT_PATH = config("APNS_CERT_PATH", default="")

# Tarefas Assíncronas (Celery + RabbitMQ)
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="amqp://guest:guest@localhost:5672//")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="rpc://")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# E-mail
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

# Vite
VITE_DEV_SERVER_URL = config("VITE_DEV_SERVER_URL", default="http://127.0.0.1:5173")

# Segurança e CORS
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=31536000 if not DEBUG else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=not DEBUG, cast=bool)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=not DEBUG, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=not DEBUG, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://127.0.0.1:5173,http://localhost:5173", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="http://127.0.0.1:5173,http://localhost:5173", cast=Csv())

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

for _host in ALLOWED_HOSTS:
    if _host not in ("*", "localhost", "127.0.0.1", "0.0.0.0") and "." in _host:
        _origin = f"https://{_host}"
        if _origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(_origin)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "user": "30/min",
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "SIGE API Documentation",
    "DESCRIPTION": "Documentação da API do SIGE.",
    "VERSION": "1.0.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# IPs que nunca entram na blacklist nem no lockout do Axes
SEGURANCA_IP_WHITELIST = config(
    "SEGURANCA_IP_WHITELIST",
    default="127.0.0.1,::1,192.168.18.14",
    cast=Csv(),
)

# Brute Force Protection (Axes)
AXES_FAILURE_LIMIT = 5 if not DEBUG else 15
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = "core/lockout.html"
AXES_RESET_ON_SUCCESS = True
AXES_IP_WHITELIST = SEGURANCA_IP_WHITELIST

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com", "data:")
CSP_IMG_SRC = ("'self'", "data:", "https:", "https://res.cloudinary.com")
CSP_INCLUDE_NONCE_IN = ["script-src"]

if DEBUG:
    CSP_SCRIPT_SRC += (VITE_DEV_SERVER_URL,)
    CSP_CONNECT_SRC = ("'self'", VITE_DEV_SERVER_URL, "ws://" + VITE_DEV_SERVER_URL.split("//")[1])

# Timeout
SESSION_EXPIRE_SECONDS = 86400 * 3
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# 2FA
TWO_FACTOR_PATCH_ADMIN = True

# Monitoramento Celery (Flower)
FLOWER_URL = config("FLOWER_URL", default="http://localhost:5555")
