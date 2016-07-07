from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

FORCE_SCRIPT_NAME = '/api'

ALLOWED_HOSTS = ['1.2.3.4']

SITE_URL = 'http://1.2.3.4/'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': '5432'
    }
}
