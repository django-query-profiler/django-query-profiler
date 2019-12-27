from typing import Union

from django_query_profiler.query_signature import QueryProfilerLevel

DJANGO_QUERY_PROFILER_REDIS_HOST: str = 'localhost'
DJANGO_QUERY_PROFILER_REDIS_PORT: int = 6379
DJANGO_QUERY_PROFILER_REDIS_DB: int = 0
DJANGO_QUERY_PROFILER_IGNORE_DETAILED_VIEW_EXCEPTION = True
DJANGO_QUERY_PROFILER_KEYS_EXPIRY_SECONDS: int = 3600
# NB: Not having django.contrib here
DJANGO_QUERY_PROFILER_APPS_MODULES_TO_REMOVE = ('django.apps', 'django.bin', 'django.conf', 'django.core',
                                                'django.db', 'django.dispatch', 'django.forms', 'django.http',
                                                'django.template', 'django.templatetags', 'django.utils',
                                                'IPython', 'django_query_profiler', 'test', 'socketserver', 'threading')


# settings module restriction for all variables to be uppercase - including functions
# noinspection PyPep8Naming
def DJANGO_QUERY_PROFILER_LEVEL_FUNC(request) -> Union[QueryProfilerLevel, None]:
    # return None to disable
    return QueryProfilerLevel.QUERY_SIGNATURE
