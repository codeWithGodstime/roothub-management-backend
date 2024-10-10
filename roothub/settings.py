import os
from pathlib import Path
from datetime import timedelta

from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="secret_key123")

DEBUG = config("DEBUG", cast=bool, default=True)
# DEBUG=False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default='localhost').split(",")

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic", # disable Django’s static file handling and allow WhiteNoise to take over
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'drf_spectacular',
    "rest_framework",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # my apps
    "authentication",
    "course"
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Roothub management system',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", #new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'roothub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'roothub.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=config("DATABASE_URL", default=""),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }


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
AUTH_USER_MODEL = "authentication.User"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mailhog'
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

else:  
    EMAIL_BACKEND = config("EMAIL_BACKEND")
    EMAIL_HOST=config("EMAIL_HOST")
    EMAIL_PORT=config("EMAIL_PORT")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS")
    EMAIL_USE_SSL = config("EMAIL_USE_SSL")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")    

DEFAULT_FROM_EMAIL = 'admin@developer.com'

if not DEBUG:
    SECURE_SSL_REDIRECT=True
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
