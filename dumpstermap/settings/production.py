from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

FORCE_SCRIPT_NAME = '/api'

ALLOWED_HOSTS = ['dumpstermap.org']

SITE_URL = 'http://dumpstermap.org/api/'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
    }
}
