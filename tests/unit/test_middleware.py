import json
import re
from typing import Dict
from unittest.mock import patch

from django.http import HttpResponse
from django.test import TestCase, override_settings
from tests.testapp.models import Topping

from django_query_profiler.chrome_plugin_helpers import ChromePluginData, redis_utils
from django_query_profiler.client.middleware import DETAILED_VIEW_EXCEPTION_LINK_TEXT, DETAILED_VIEW_EXCEPTION_URL
from django_query_profiler.query_signature import QueryProfilerLevel, SqlStatement


class QueryProfilerMiddlewareTest(TestCase):

    def setUp(self):
        Topping.objects.create(name="jalapenos", is_spicy=True)

    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_headers_with_redis_call_successful(self, mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.return_value = 'mock'

        response: HttpResponse = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_DETAILED_VIEW_LINK_TEXT),
                         QueryProfilerLevel.QUERY_SIGNATURE.name.lower())

        url_pattern = "http://.*/django_query_profiler/mock/" + QueryProfilerLevel.QUERY_SIGNATURE.name
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
