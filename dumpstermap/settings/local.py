# Put any machine-specific settings in local.py

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dumpstermap_django',
        'USER': 'moritz',
        'PASSWORD': 'JTjyLh2tEqgGF7lFJ707',
        'HOST': 'localhost'
    }
}