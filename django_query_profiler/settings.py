from typing import Union

from django_query_profiler.query_signature import QueryProfilerLevel

# Parameters for configuring redis
DJANGO_QUERY_PROFILER_REDIS_HOST: str = 'localhost'
DJANGO_QUERY_PROFILER_REDIS_PORT: int = 6379
DJANGO_QUERY_PROFILER_REDIS_DB: int = 0
DJANGO_QUERY_PROFILER_REDIS_KEYS_EXPIRY_SECONDS: int = 3600

"""
Parameter that controls if we should eat up the exception if redis or urls.py is not configured
redis & urls.py are required for setting up the detailed view - the view that opens up when clicking on the
link in the chromium plugin that says "Details link"

"""
DJANGO_QUERY_PROFILER_IGNORE_DETAILED_VIEW_EXCEPTION = True
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
