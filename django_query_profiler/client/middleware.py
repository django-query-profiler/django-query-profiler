"""
This module contains the middleware that can be applied to any request, to enable query profiler.
It internally calls context manager, and has the same output as the context manager.  It just adds some response
headers, for the chrome plugin to display
"""
import json
from time import time
from typing import Callable, Union

from django.conf import settings
from django.urls import reverse

import django_query_profiler.client.urls as query_profiler_url
import django_query_profiler.settings as django_query_profiler_settings
from django_query_profiler.chrome_plugin_helpers import (ChromePluginData,
                                                         redis_utils)
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_signature import (QueryProfiledData,
                                                   QueryProfilerLevel)

if not settings.configured:  # For tests
    settings.configure(default_settings=django_query_profiler_settings)


class QueryProfilerMiddleware:

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we have to enable query profiler or not.
        query_profiler_level: Union[QueryProfilerLevel, None] = settings.DJANGO_QUERY_PROFILER_LEVEL_FUNC(request)
        if not query_profiler_level:
            return self.get_response(request)

        start_time: float = time()
        '''
        Lets clear all the storage related to this thread.  This is not strictly needed, but just as a safety measure
        As a side effect, this implies that we *CANNOT* use this middleware twice for a request
        '''
        with QueryProfiler(query_profiler_level, clear_thread_local=True) as query_profiler:
            response = self.get_response(request)

        # Pickling the object, and saving to redis
        query_profiled_data: QueryProfiledData = query_profiler.query_profiled_data
        redis_key: str = redis_utils.store_data(query_profiled_data)

        # Constructing detailed view url
        query_profiled_detail_relative_url: str = reverse(query_profiler_url.GET_QUERY_PROFILED_DATA_NAME,
                                                          args=[redis_key, query_profiler_level.name])
        query_profiled_detail_absolute_url: str = request.build_absolute_uri(query_profiled_detail_relative_url)

        # Setting all headers that the chrome plugin require
        response[ChromePluginData.QUERY_PROFILED_SUMMARY_DATA] = json.dumps(query_profiled_data.summary.as_dict())
        response[ChromePluginData.QUERY_PROFILED_DETAILED_URL] = query_profiled_detail_absolute_url
        response[ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS] = query_profiled_data.time_spent_profiling_in_micros
        response[ChromePluginData.TOTAL_SERVER_TIME_IN_MILLIS] = int((time() - start_time) * 1000)
        response[ChromePluginData.QUERY_PROFILER_LEVEL] = query_profiler_level.name
        return response
