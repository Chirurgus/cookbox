"""
Django settings for cookbox project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured

if 'DEBUG' not in os.environ.keys():
    from dotenv import load_dotenv
    load_dotenv("dev.env")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
# You can generate one with:
# ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: remove localhost for production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")

# Need a signed certificate for these
#SECURE_SSL_REDIRECT = True

#SESSION_COOKIE_SECURE = True

#CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('recipe-list')

# Path for static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
STATIC_URL = "/static_files/"

# Path for Images in the database
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
MEDIA_URL = "/images/"


# Application definition

INSTALLED_APPS = [
    'cookbox_core.apps.CookboxCoreConfig',
    'cookbox_webui.apps.CookboxWebuiConfig',
    'cookbox_recipeui.apps.CookboxRecipeuiConfig',
    'cookbox_glossary.apps.CookboxGlossaryConfig',
    'cookbox_seasons.apps.CookboxSeasonsConfig',
    'cookbox_admin.apps.CookboxAdminConfig',
    'django_superform',
    'nested_admin',
    'imagekit',
    'dal',
    'dal_select2',
    'markdownx',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cookbox_webui.middleware.AuthRequiredMiddleware',
]

ROOT_URLCONF = 'cookbox.urls'

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

WSGI_APPLICATION = 'cookbox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DB_ENGINE = os.environ.get("DB_ENGINE")

if DB_ENGINE == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db_test/db.sqlite3'),
        }
    }
elif DB_ENGINE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE'),
            'USER': os.environ.get('MYSQL_USER'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
            'HOST': os.environ.get('MYSQL_HOST'),
            'PORT': "3306",
        }
    }
else:
    raise ImproperlyConfigured("Specified 'DB_ENGINE' is not supported.")

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging settings
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'django.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

# Maximum number of forms in a POST request
# Every inline form requires about 15 hidden forms
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000
