from .base import *

DEBUG = False

ALLOWED_HOSTS = ["namu.azurewebsites.net", "namu.prodeko.org", "127.0.0.1"]

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
    }
}


MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

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
