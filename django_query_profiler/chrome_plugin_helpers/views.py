from typing import Dict

from django.shortcuts import render

from django_query_profiler.chrome_plugin_helpers import redis_utils
from django_query_profiler.query_signature import QueryProfiledData, QueryProfilerType

QUERY_PROFILER_TO_TEMPLATE: Dict[str, str] = {
    QueryProfilerType.QUERY_SIGNATURE.name: 'query_signature_profiled_data.html',
    QueryProfilerType.QUERY.name: 'query_profiled_data.html',
}


def get_query_profiled_data(request, redis_key: str, query_profiler_type: str):
    query_profiled_data: QueryProfiledData = redis_utils.retrieve_data(redis_key)
    context = {
        'summary': query_profiled_data.summary,
        'query_signature_to_statistics': query_profiled_data.query_signature_to_query_signature_statistics,
    }
    return render(request, QUERY_PROFILER_TO_TEMPLATE[query_profiler_type], context)
