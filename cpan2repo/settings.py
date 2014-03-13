"""
Django settings for cpan2repo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '699as_fk@jwqm-1ixt#hy)mhh76+5+x@r2m&&&^rs_^hb)(p@9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

LOGIN_REDIRECT_URL = "/"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'djcelery',
    'bootstrap3',
    'south',
    'cpan2repo',
    'webui',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cpan2repo.urls'

WSGI_APPLICATION = 'cpan2repo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': '',
       'USER': '',
       'PASSWORD': '',
       'HOST': '',
       'PORT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# Celery
BROKER_URL = 'amqp://guest:guest@localhost:5672/cpan2repo'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ENABLE_UTC = True

# Builder
CPANM_PATH = "/usr/local/bin/cpanm"
TMP_BUILD_DIR = "/home/agent/cpan2repo/build"
CHECK_CORE_MODULE_PATH = "/usr/local/bin/check_core_module.pl"
FISHEYE_LINK = None

try:
    from cpan2repo.local_settings import *
except ImportError:
    pass
