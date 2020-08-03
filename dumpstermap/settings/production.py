import dj_database_url

from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dumpstermap.org',
                 'dumpstermap.vercel.app',
                 'dumpstermap.herokuapp.com']

STATIC_URL = '/static/'

DATABASES = {
    # Retrieve database settings from env variable DATABASE_URL
    'default': dj_database_url.config(engine='django.contrib.gis.db.backends.postgis')
}
