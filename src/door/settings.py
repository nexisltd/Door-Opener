import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR.joinpath('static')
MEDIA_DIR = BASE_DIR.joinpath('media')


if os.getenv('SECRET_KEY'):
    ON_PRODUCTION = os.environ.get('ON_PRODUCTION') == "True"
    DJANGO_SECRET_KEY = os.environ.get('SECRET_KEY')
    DJANGO_DEBUG = os.environ.get('DEBUG') == "True"
    ZK_IP = os.environ.get('ZK_IP')
    ZK_PASSWORD = os.environ.get('ZK_PASSWORD')
    WEBCAM_USER = os.environ.get('WEBCAM_USER')
    WEBCAM_IP = os.environ.get('WEBCAM_IP')
    WEBCAM_PASSWORD = os.environ.get('WEBCAM_PASSWORD')
    WEBCAM_PORT = os.environ.get('WEBCAM_PORT')


else:
    env = environ.Env(
        DEBUG=(bool, False)
    )

    environ.Env.read_env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    ON_PRODUCTION = env('ON_PRODUCTION') == "True"
    DJANGO_SECRET_KEY = env('SECRET_KEY')
    DJANGO_DEBUG = env('DEBUG') == "True"
    ZK_IP = env('ZK_IP')
    ZK_PASSWORD = env('ZK_PASSWORD')
    WEBCAM_USER = env('WEBCAM_USER')
    WEBCAM_IP = env('WEBCAM_IP')
    WEBCAM_PASSWORD = env('WEBCAM_PASSWORD')
    WEBCAM_PORT = env('WEBCAM_PORT')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_DEBUG


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]

ASGI_APPLICATION = "door.asgi.application"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'door.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'door.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
# STATICFILES_DIRS = [STATIC_DIR]
STATICFILES_DIRS = ['static']

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
