"""
Django settings for cookbox project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from django.urls import reverse_lazy

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRETS_FOLDER = os.path.join(BASE_DIR, 'secrets')

# Create the secrets folder it it does not exist
if not os.path.isdir(SECRETS_FOLDER):
    os.mkdir(SECRETS_FOLDER)

def load_or_generate_secret_key():
    secret_file = os.path.join(SECRETS_FOLDER, 'SECRET_KEY')
    if not os.path.isfile(secret_file):
        import random
        secret_key = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
        with open(os.path.join(SECRETS_FOLDER, 'SECRET_KEY'), 'xt') as f:
            f.write(secret_key)
        return secret_key
    else:
        return read_secret('SECRET_KEY')

def read_secret(secret):
    secret_file = os.path.join(SECRETS_FOLDER, secret)
    if (os.path.isfile(secret_file)):
        with open(secret_file) as f:
            return f.read().strip('\n')
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("Secrets folder does not contain: " + secret)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = load_or_generate_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.path.isfile(os.path.join(SECRETS_FOLDER, 'PRODUCTION'))

# SECURITY WARNING: remove localhost for production
ALLOWED_HOSTS = ['localhost', '10.0.2.2'] if DEBUG else [ read_secret('HOST') ]

#SECURE_SSL_REDIRECT = not DEBUG 

#SESSION_COOKIE_SECURE = not DEBUG

#CSRF_COOKIE_SECURE = not DEBUG

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

# Path for Images in the datbase
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
MEDIA_URL = "/images/"


# Application definition

INSTALLED_APPS = [
    'cookbox_core.apps.CookboxCoreConfig',
    'cookbox_webui.apps.CookboxWebuiConfig',
    'cookbox_admin.apps.CookboxAdminConfig',
    'cookbox_rest.apps.CookboxRestConfig',
    'django_filters',
    'nested_admin',
    'rest_framework',
    'imagekit',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
} if DEBUG else {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(SECRETS_FOLDER, 'my.cnf'),
        }
    }
}



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


