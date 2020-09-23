import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    send_default_pii=True
)

DEBUG = False

ALLOWED_HOSTS = ["namukilke.azurewebsites.net", "namu.prodeko.org", "127.0.0.1"]

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "namukilke",
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": "prodeko-postgres.postgres.database.azure.com",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "verify-ca",
            "sslrootcert": os.environ.get("POSTGRESQL_SSL_CA", ""),
        },
    }
}

MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)

STORAGE_KEY = os.getenv("STORAGE_KEY", "keep_this_secret_in_prod")

CDN_URL = "static.prodeko.org"
AZURE_CUSTOM_DOMAIN = CDN_URL
MEDIA_LOCATION = "media"

DEFAULT_FILE_STORAGE = "namukilke.azure_backend.AzureMediaStorage"
MEDIA_URL = f"https://{CDN_URL}/{MEDIA_LOCATION}/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "logfile": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "/home/LogFiles/namukilke.log",
        }
    },
    "loggers": {
        "django": {"handlers": ["logfile"], "level": "ERROR", "propagate": False,}
    },
}
