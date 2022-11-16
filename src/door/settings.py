import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR.joinpath("templates")
STATIC_DIR = BASE_DIR.joinpath("static")
MEDIA_DIR = BASE_DIR.joinpath("media")

# Django Configuration
ON_PRODUCTION = os.getenv("ON_PRODUCTION") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
# Database configuration
DJANGO_DB_ENGINE = os.getenv("DB_ENGINE", "postgresql")
DJANGO_DB_NAME = os.getenv("DB_NAME")
DJANGO_DB_USER = os.getenv("DB_USER")
DJANGO_DB_PASSWORD = os.getenv("DB_PASSWORD")
DJANGO_DB_HOST = os.getenv("DB_HOST")
ZK_IP = os.getenv("ZK_IP")
ZK_PASSWORD = os.getenv("ZK_PASSWORD")
WEBCAM_USER = os.getenv("WEBCAM_USER")
WEBCAM_IP = os.getenv("WEBCAM_IP")
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
# Celery Configuration Options
CELERY_BROKER_URL = os.getenv("RABBIT_URL", os.getenv("REDIS_URL"))
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "ml",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "door.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


ASGI_APPLICATION = "door.asgi.application"

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


if ON_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": f"django.db.backends.{DJANGO_DB_ENGINE}",
            "NAME": DJANGO_DB_NAME,
            "USER": DJANGO_DB_USER,
            "PASSWORD": DJANGO_DB_PASSWORD,
            "HOST": DJANGO_DB_HOST,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.joinpath("staticfiles")
STATICFILES_DIRS = ["static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
