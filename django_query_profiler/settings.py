from django_query_profiler.query_signature import QueryProfilerLevel

DJANGO_QUERY_PROFILER_REDIS_HOST: str = 'localhost'
DJANGO_QUERY_PROFILER_REDIS_PORT: int = 6379
DJANGO_QUERY_PROFILER_REDIS_DB: int = 0
DJANGO_QUERY_PROFILER_KEYS_EXPIRY_SECONDS: int = 3600
DJANGO_QUERY_PROFILER_APPS_TO_REMOVE = ('django', 'IPython', 'django_query_profiler', 'test')


# PEP-8 naming violation because of settings module restriction
def DJANGO_QUERY_PROFILER_TYPE_FUNC(request) -> QueryProfilerLevel:
    # return None to disable
    return QueryProfilerLevel.QUERY_SIGNATURE
