import os

from django_query_profiler.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


INSTALLED_APPS = (
    'django_query_profiler',
    'tests.integration.setup',
)

SECRET_KEY = 'dummy'

DATABASES = {
    'default': {
        'ENGINE': 'django_query_profiler.django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
