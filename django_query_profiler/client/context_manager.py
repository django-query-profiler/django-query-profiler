"""
All the logic of the query profiler resides in the QueryProfilerThreadLocalStorage module.  This context manager
simply delegates the call to that module
"""
from functools import wraps
from typing import Union

from django_query_profiler.query_signature import QueryProfiledData, QueryProfilerLevel
from django_query_profiler.query_signature.data_storage import query_profiler_thread_local_storage


class QueryProfiler:

    def __init__(self, query_profiler_level: QueryProfilerLevel, clear_thread_local: bool = False):
        if clear_thread_local:
            query_profiler_thread_local_storage.reset()

        self.query_profiled_data: Union[QueryProfiledData, None] = None
        self.query_profiler_level: QueryProfilerLevel = query_profiler_level

    def __enter__(self):
        query_profiler_thread_local_storage.enter_profiler_mode(self.query_profiler_level)
        return self

    def __exit__(self, *_) -> None:
        self.query_profiled_data = query_profiler_thread_local_storage.exit_profiler_mode()

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            with self:
                output = func(*args, **kwargs)
            print(self.query_profiled_data.summary)
            return output
        return decorator
