"""
Django settings for apistored project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ


env = environ.Env(
    LH_SECRET_KEY=(str, '33kfxlkpvly@&xnz=ke-gs%+9a)w9s=$plwhh-=yo8t08((+#7'),
    LH_DEBUG=(bool, True)
)
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('LH_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('LH_DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'rest_framework',

    'hotels',
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

ROOT_URLCONF = 'apistored.urls'

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

WSGI_APPLICATION = 'apistored.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db('LH_DATABASE_URL',
                      default='postgis://limehome:limehome@127.0.0.1:5432/limehome')
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

REACT_BUILD_PATH = env('LH_REACT_BUILD_PATH',
                       default=os.path.join(BASE_DIR, '..', 'hotelmap', 'build'))

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(REACT_BUILD_PATH, 'static')
]

# HERE MAPS
APP_ID = env('LH_MAPS_APP_ID')
APP_CODE = env('LH_MAPS_APP_CODE')

# CELERY
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['json', 'yaml']
CELERY_BROKER_URL = env('LH_CELERY_BROKER', default="redis://localhost:6379/0")
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 43200,
    'fanout_patterns': True,
    'fanout_prefix': True
}
CELERY_BROKER_CONNECTION_MAX_RETRIES = 3
