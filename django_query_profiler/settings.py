QUERY_PROFILER_ENABLED: bool = True
QUERY_PROFILER_REDIS_HOST: str = 'localhost'
QUERY_PROFILER_REDIS_PORT: int = 6379
QUERY_PROFILER_REDIS_DB: int = 0
QUERY_PROFILER_KEYS_EXPIRY_SECONDS: int = 3600
QUERY_PROFILER_APPS_TO_REMOVE = ('django', 'IPython', 'django_query_profiler', 'test')


def QUERY_PROFILER_TYPE_FUNC(_):
    from django_query_profiler.query_signature import QueryProfilerType
    return QueryProfilerType.QUERY_SIGNATURE
