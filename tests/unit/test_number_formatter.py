from unittest import TestCase

from django_query_profiler.templatetags.number_formatter import commafy


class IntCommafyTest(TestCase):

    def test_None_value(self):
        original_number = None
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '-')

    def test_less_than_thousand(self):
        original_number = 100
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '100')

    def test_more_than_thousand(self):
        original_number = 1001
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '1,001')

    def test_less_than_million(self):
        original_number = 100981
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '100,981')

    def test_more_than_million(self):
        original_number = 1039812
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '1,039,812')


class FloatCommafyTest(TestCase):

    def test_less_than_thousand(self):
        original_number = 100.1
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '100.1')

    def test_more_than_thousand(self):
        original_number = 1001.2
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '1,001.2')

    def test_less_than_million(self):
        original_number = 100981.43
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '100,981.43')

    def test_more_than_million(self):
        original_number = 1039812.02
        formatted_number = commafy(original_number)
        self.assertEqual(formatted_number, '1,039,812.02')
