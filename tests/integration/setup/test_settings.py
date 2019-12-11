import os

from django_query_profiler.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = (
    'django_query_profiler',
    'tests.integration.setup',
)

DATABASES = {
    'default': {
        'ENGINE': 'django_query_profiler.django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'dummy'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
#
# MIDDLEWARE = [
#     'django_query_profiler.client.middleware.QueryProfilerMiddleware',
# ]
