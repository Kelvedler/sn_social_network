"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import environ
import logging
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(str(BASE_DIR / '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1'])

USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST', default=False)

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['127.0.0.1'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'main',
    'person'
]

MIDDLEWARE = [
    'main.middleware.Logging',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.UnexpectedError'
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PATH_LOGS = env.str('PATH_LOGS', default=str(BASE_DIR / 'logs'))
if not os.path.exists(PATH_LOGS):
    os.makedirs(PATH_LOGS)

# Levels: DEBUG|INFO|WARNING|ERROR|CRITICAL
APP_LOG_LEVEL = env.str('APP_LOG_LEVEL', default='INFO')
SYSTEM_LOG_LEVEL = env.str('SYSTEM_LOG_LEVEL', default='ERROR')

LOG_FILE_SIZE = 1024 * 1024 * 5  # 5Mb
LOG_BACKUP_COUNT = 5

LOGGING_FORMAT_VERBOSE = '[%(asctime)s: %(levelname)s/%(processName)s] %(name)s - %(message)s'
LOGGING_FORMAT_SIMPLE = '%(asctime)s: %(levelname)s %(message)s'
formatter = logging.Formatter(LOGGING_FORMAT_VERBOSE)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': LOGGING_FORMAT_VERBOSE,
        },
        'simple': {
            'format': LOGGING_FORMAT_SIMPLE,
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': APP_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PATH_LOGS, 'error.log'),
            'maxBytes': LOG_FILE_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'verbose',
        },
        'general_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PATH_LOGS, 'general.log'),
            'maxBytes': LOG_FILE_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'error_file', 'general_file'],
        'level': SYSTEM_LOG_LEVEL,
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': SYSTEM_LOG_LEVEL,
            'propagate': False,
        },
        'main': {
            'handlers': ['console', 'error_file', 'general_file'],
            'level': APP_LOG_LEVEL,
            'propagate': False,
        },
        'person': {
            'handlers': ['console', 'error_file', 'general_file'],
            'level': APP_LOG_LEVEL,
            'propagate': False,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'main.utils.jwt_.JWTAuthentication',
    )
}

JWT = {
    'SECRET': SECRET_KEY,
    'ACCESS_EXPIRATION_DELTA': timedelta(seconds=env.int('JWT_ACCESS_EXPIRATION_DELTA', default=60 * 15)),
    'REFRESH_EXPIRATION_DELTA': timedelta(seconds=env.int('JWT_REFRESH_EXPIRATION_DELTA', default=60 * 60 * 24 * 14))
}
