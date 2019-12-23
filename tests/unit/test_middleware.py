import json
import re
from typing import Dict

from django.http import HttpResponse
from django.test import TestCase

from django_query_profiler.chrome_plugin_helpers import ChromePluginData
from django_query_profiler.query_signature import QueryProfilerLevel, SqlStatement
from tests.testapp.models import Topping


class QueryProfilerMiddlewareTest(TestCase):

    def setUp(self):
        Topping.objects.create(name="jalapenos", is_spicy=True)

    def test_headers(self):
        # Create an instance of a GET request.
        response: HttpResponse = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_LEVEL), QueryProfilerLevel.QUERY_SIGNATURE.name)

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

