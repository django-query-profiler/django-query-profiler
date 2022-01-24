import json
import logging
import re
from typing import Dict
from unittest.mock import patch

import fakeredis
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBase
from django.test import TestCase, override_settings

from django_query_profiler.chrome_plugin_helpers import ChromePluginData, redis_utils
from django_query_profiler.chrome_plugin_helpers.views import get_query_profiled_data
from django_query_profiler.client.middleware import DETAILED_VIEW_EXCEPTION_LINK_TEXT, DETAILED_VIEW_EXCEPTION_URL
from django_query_profiler.query_profiler_storage import QueryProfiledData, QueryProfilerLevel, SqlStatement
from tests.testapp.food.models import Topping

logger = logging.getLogger('testing')


def django_query_profiler_post_processor_that_adds_another_header(
        query_profiled_data: QueryProfiledData,
        request: HttpRequest,
        response: HttpResponseBase) -> None:
    """
    A test function that adds another header to the response, and writes to logs
    """
    response['test_headers'] = 'a new value for my custom chrome plugin'


class QueryProfilerMiddlewareTest(TestCase):

    def setUp(self):
        Topping.objects.create(name="jalapenos", is_spicy=True)
        redis = fakeredis.FakeRedis()
        redis_utils.REDIS_INSTANCE = redis  # Probably a bad way, but it is difficult to understand how to mock this

    def test_headers_with_redis_call_successful(self):
        response: HttpResponse = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_DETAILED_VIEW_LINK_TEXT),
                         QueryProfilerLevel.QUERY_SIGNATURE.name.lower())

        url_pattern = "http://.*/django_query_profiler/.*/" + QueryProfilerLevel.QUERY_SIGNATURE.name
        detailed_url = response.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)

        self.assertEqual(re.match(url_pattern, detailed_url).start(), 0)
        self.assertTrue(response.has_header(ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS))
        self.assertTrue(response.has_header(ChromePluginData.TOTAL_SERVER_TIME_IN_MILLIS))

        summary_data: Dict = json.loads(response.get(ChromePluginData.QUERY_PROFILED_SUMMARY_DATA))
        self.assertEqual(summary_data['exact_query_duplicates'], 4)
        self.assertEqual(summary_data[SqlStatement.SELECT.name], 5)
        self.assertEqual(summary_data[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_data[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_data[SqlStatement.DELETE.name], 0)

    @patch('django_query_profiler.client.middleware.redis_utils')
    @override_settings(DJANGO_QUERY_PROFILER_IGNORE_DETAILED_VIEW_EXCEPTION=False)
    def test_headers_with_redis_throws_exception_ignore_detailed_view_exception_false(self,
                                                                                      mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.side_effect = Exception("redis not setup")
        with self.assertRaises(Exception) as context:
            self.client.get('/')
        self.assertTrue('redis not setup' in str(context.exception))

    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_headers_with_redis_throws_exception_ignore_detailed_view_exception_true(self,
                                                                                     mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.side_effect = Exception("redis not setup")

        response: HttpResponse = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_DETAILED_VIEW_LINK_TEXT),
                         DETAILED_VIEW_EXCEPTION_LINK_TEXT)

        url_pattern = DETAILED_VIEW_EXCEPTION_URL
        detailed_url = response.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertEqual(re.match(url_pattern, detailed_url).start(), 0)
        self.assertTrue(response.has_header(ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS))
        self.assertTrue(response.has_header(ChromePluginData.TOTAL_SERVER_TIME_IN_MILLIS))

        summary_data: Dict = json.loads(response.get(ChromePluginData.QUERY_PROFILED_SUMMARY_DATA))
        self.assertEqual(summary_data['exact_query_duplicates'], 4)
        self.assertEqual(summary_data[SqlStatement.SELECT.name], 5)
        self.assertEqual(summary_data[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_data[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_data[SqlStatement.DELETE.name], 0)

    def test_detailed_view_url_from_header_call_successful_query_signature_level(self):
        response_index_view: HttpResponse = self.client.get('/')
        query_profiler_detailed_view_url: str = response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertTrue(QueryProfilerLevel.QUERY_SIGNATURE.name in query_profiler_detailed_view_url)

        # We want to retrieve the actual param that was passed to the mock
        response_detailed_url: HttpResponse = self.client.get(query_profiler_detailed_view_url)

        self.assertEqual(response_detailed_url.resolver_match.url_name, get_query_profiled_data.__name__)
        self.assertContains(response_detailed_url, "<th>5</th>")  # For select count
        self.assertContains(response_detailed_url, "<th>4</th>")  # For exact query duplicates
        self.assertContains(response_detailed_url, "flamegraphStack")  # For flamegraph

    @override_settings(DJANGO_QUERY_PROFILER_LEVEL_FUNC=lambda _: QueryProfilerLevel.QUERY)
    def test_detailed_view_url_from_header_call_successful_query_level(self):
        response_index_view: HttpResponse = self.client.get('/')
        query_profiler_detailed_view_url: str = response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertTrue(QueryProfilerLevel.QUERY.name in query_profiler_detailed_view_url)

        response_detailed_url: HttpResponse = self.client.get(query_profiler_detailed_view_url)
        self.assertEqual(response_detailed_url.resolver_match.url_name, get_query_profiled_data.__name__)
        self.assertContains(response_detailed_url, "<th>5</th>")  # For select count
        self.assertContains(response_detailed_url, "<th>4</th>")  # For exact query duplicates
        self.assertNotContains(response_detailed_url, "flamegraphStack")  # For flamegraph

    @override_settings(DJANGO_QUERY_PROFILER_LEVEL_FUNC=lambda _: None)
    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_index_view_with_none_profiler_level(self, mock_redis_utils: redis_utils):
        response_index_view: HttpResponse = self.client.get('/')
        self.assertIsNone(response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL))
        self.assertFalse(mock_redis_utils.called)

    @override_settings(
        DJANGO_QUERY_PROFILER_POST_PROCESSOR=django_query_profiler_post_processor_that_adds_another_header)
    def test_query_profiler_post_processor_to_write_to_logs(self):
        response: HttpResponse = self.client.get('/')
        # Test header set by django query profiler middleware and custom post processor function
        self.assertTrue(response.has_header(ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS))
        self.assertTrue(response.has_header('test_headers'))
