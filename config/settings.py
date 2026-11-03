"""
Django settings for Copier Business ERP.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- env ----------
def _env(name, default=""):
    return os.environ.get(name, default)

# Allow loading from a .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

SECRET_KEY = _env("SECRET_KEY", "django-insecure-copier-erp-dev-key-change-me")
DEBUG = _env("DEBUG", "True").lower() in ("1", "true", "yes")
# On PaaS (HostKB, Railway, etc.) ALLOWED_HOSTS must include the app's hostname.
# Using "*" works for testing; tighten in real production.
ALLOWED_HOSTS = [h.strip() for h in _env("ALLOWED_HOSTS", "*").split(",") if h.strip()]

# ---------- applications ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    "django_ledger",
    "rest_framework",

    "accounts",
    "audit",
    "notifications",
    "companies",
    "customers",
    "suppliers",
    "products",
    "purchases",
    "inventory",
    "stock_issues",
    "stock_returns",
    "sales",
    "invoicing",
    "crm",
    "requirements_app",
    "payments",
    "accounting",
    "gst",
    "expenses",
    "reports",
    "imports_exports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accounts.middleware.AuditMiddleware",
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
                "accounts.context_processors.user_role_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------- database ----------
# 1) If DATABASE_URL is set (PostgreSQL add-on), use it.
# 2) Else if /tmp is writable (typical on PaaS), put SQLite there.
# 3) Else fall back to BASE_DIR (dev).
DATABASE_URL = _env("DATABASE_URL", "")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    # Pick a writable path. /data is sometimes a mounted volume on PaaS,
    # otherwise /tmp is always writable on Linux containers.
    candidates = [
        Path("/data"),
        Path("/tmp"),
        BASE_DIR,
    ]
    db_dir = next((p for p in candidates if p.exists() and os.access(p, os.W_OK)), BASE_DIR)
    db_path = db_dir / "copier_erp.sqlite3"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(db_path),
        }
    }
    print(f"[settings] Using SQLite at: {db_path}")

# ---------- auth ----------
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 6}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- i18n ----------
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------- static / media ----------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- file uploads ----------
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

# ---------- django-ledger ----------
DJANGO_LEDGER = {"DEFAULT_CURRENCY": "INR"}
DJANGO_LEDGER_USE_DEPRECATED_BEHAVIOR = False

# ---------- REST framework ----------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ---------- app-specific ----------
LOW_STOCK_THRESHOLD_DEFAULT = 10
SESSION_COOKIE_AGE = 60 * 60 * 8

# Allow the HostKB public URL for CSRF
CSRF_TRUSTED_ORIGINS = []
hostkb_origin = _env("HOSTKB_ORIGIN", "")
if hostkb_origin:
    CSRF_TRUSTED_ORIGINS.append(hostkb_origin)

# ---------- production hardening ----------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# WhiteNoise for static files in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------- PaaS deployment hardening ----------
# Ensure runserver doesn't try to use autoreload (in case gunicorn isn't picked up)
RELOAD_INTERACTIVE = False

# Log to stdout (HostKB captures it)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
