'''
This module contains both functiions of setting and getting from redis
Redis is used for storing the pickled query profiled data, and later to retrieve it back
'''
import uuid
import pickle

import redis
from django.conf import settings

from django_query_profiler.query_signature import QueryProfiledData

'''
This is needed just for making the tests happy.  We don't have a settings.py file, but we are using the client's file.
Test cases don't like that we don't have a settings.py file, but we are trying to access settings in code
'''
if not settings.configured:
    settings.configure(
        QUERY_PROFILER_REDIS_HOST='',
        QUERY_PROFILER_REDIS_PORT=1,
        QUERY_PROFILER_REDIS_DB='',
        QUERY_PROFILER_KEYS_EXPIRY_SECONDS=1)

REDIS_INSTANCE = redis.StrictRedis(
    host=settings.QUERY_PROFILER_REDIS_HOST,
    port=settings.QUERY_PROFILER_REDIS_PORT,
    db=settings.QUERY_PROFILER_REDIS_DB)


def store_data(query_profiled_data: QueryProfiledData) -> str:
    pickled_query_profiled_data = pickle.dumps(query_profiled_data)
    redis_key = str(uuid.uuid4().hex)
    ttl_seconds: int = settings.QUERY_PROFILER_KEYS_EXPIRY_SECONDS
    REDIS_INSTANCE.set(name=_get_key(redis_key), value=pickled_query_profiled_data, ex=ttl_seconds)
    return redis_key


def retrieve_data(redis_key: str) -> QueryProfiledData:
    redis_object = REDIS_INSTANCE.get(_get_key(redis_key))
    return pickle.loads(redis_object)


def _get_key(redis_key: str) -> str:
    ''' Trying to create a namespace for django_query_profiler keys.  We could have used redis keyspace as well '''
    redis_key_prefix = 'django_query_profiler_'
    return f'{redis_key_prefix}:{redis_key}'
