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
    'default': dj_database_url.config()
}
