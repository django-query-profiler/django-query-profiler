import os

from django_query_profiler.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


INSTALLED_APPS = (
    'django_query_profiler',
    'tests.testapp',
)

SECRET_KEY = 'dummy'

DATABASES = {
    'default': {
        'ENGINE': 'django_query_profiler.django.db.backends.mysql',
        'NAME': 'travis_ci_test',
        'USER': 'travis',
    }
}
