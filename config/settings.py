import os
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv
import sentry_sdk
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

# Apps
INSTALLED_APPS = [
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
    "django_prometheus",
]

# Middleware (Ordem do Prometheus é importante)
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "apps.comum.middleware.tenant_middleware.TenantMiddleware",
    "apps.comum.middleware.audit_middleware.AuditMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
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
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Banco de Dados
DB_ENGINE = config("DB_ENGINE", default="django.db.backends.sqlite3")

if DB_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="3306"),
        }
    }

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

# Cloudinary
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

if not DEBUG:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
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

# Brute Force Protection (Axes)
AXES_FAILURE_LIMIT = 5 if not DEBUG else 15
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = "core/lockout.html"
AXES_RESET_ON_SUCCESS = True

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_INCLUDE_NONCE_IN = ["script-src"]

if DEBUG:
    CSP_SCRIPT_SRC += (VITE_DEV_SERVER_URL,)
    CSP_CONNECT_SRC = ("'self'", VITE_DEV_SERVER_URL, "ws://" + VITE_DEV_SERVER_URL.split("//")[1])

# Timeout
SESSION_EXPIRE_SECONDS = 86400 * 3
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# 2FA
TWO_FACTOR_PATCH_ADMIN = True
