"""
All the logic of the query profiler resides in the QueryProfilerThreadLocalStorage module.  This context manager
simply delegates the call to that module
"""
from typing import Optional

from django_query_profiler.query_signature import QueryProfiledData, QueryProfilerLevel
from django_query_profiler.query_signature.data_storage import query_profiler_thread_local_storage


class QueryProfiler:

    def __init__(self, query_profiler_level: QueryProfilerLevel, clear_thread_local: bool = False):
        if clear_thread_local:
            query_profiler_thread_local_storage.reset()

        self.query_profiled_data: Optional[QueryProfiledData] = None
        self.query_profiler_level: QueryProfilerLevel = query_profiler_level

    def __enter__(self) -> 'QueryProfiler':
        query_profiler_thread_local_storage.enter_profiler_mode(self.query_profiler_level)
        return self

    def __exit__(self, *_) -> None:
        self.query_profiled_data = query_profiler_thread_local_storage.exit_profiler_mode()
