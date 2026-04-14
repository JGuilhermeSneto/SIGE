"""
Módulo de configuração central do Django (SIGE).

O que é: define INSTALLED_APPS, banco, templates, estáticos, e-mail, REST e CORS.
Valores sensíveis vêm do arquivo ``.env`` via ``python-decouple`` (não versionar segredos).
"""

from pathlib import Path
from decouple import config, Csv

# Diretório raiz do projeto (pasta que contém ``manage.py``).
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Segurança e modo de execução ──
SECRET_KEY = config("SECRET_KEY", default="django-insecure-default-key-change-it")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# ── Apps instalados (Django + SIGE + bibliotecas de terceiros) ──
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
    "widget_tweaks",
    "rest_framework",
    "corsheaders",
]

# ── Pipeline de requisição (ordem importa) ──
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Módulo que contém ``urlpatterns`` principal (rotas do site).
ROOT_URLCONF = "config.urls"

# ── Motor de templates HTML ──
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
            ],
            "libraries": {
                "custom_tags": "apps.comum.templatetags.custom_tags",
                "get_item": "apps.comum.templatetags.get_item",
            },
        },
    },
]

# Entry point WSGI (servidores síncronos).
WSGI_APPLICATION = "config.wsgi.application"

# ── Banco de dados: SQLite por padrão ou MySQL via variáveis DB_* no .env ──
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

# ── Fluxo de login do Django Auth ──
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Locale e fuso ──
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ── Arquivos estáticos (CSS/JS) e uploads (media) ──
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "apps" / "comum" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Envio de e-mail (reset de senha, notificações) ──
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

# ── Vite (dev): URL do ``npm run dev`` para injetar módulos em ``app_vite.html`` ──
VITE_DEV_SERVER_URL = config("VITE_DEV_SERVER_URL", default="http://127.0.0.1:5173")

# ── API REST e CORS (front separado ou integrações) ──
CORS_ALLOW_ALL_ORIGINS = True  # Em produção, restrinja a domínios confiáveis.

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}
