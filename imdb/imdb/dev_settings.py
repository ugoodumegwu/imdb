from .common_settings import *


DEBUG = True
SECRET_KEY = 'some secret'

INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES['default'].update({
    'NAME': 'mymdb',
    'USER': 'mymdb',
    'PASSWORD': 'development',
    'HOST': 'localhost',
    'PORT': '5432',
})

CACHES = {
    'default': {
    'BACKEND' : 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'default-locmemcache',
    'TIMEOUT': 5,
}}

# django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]