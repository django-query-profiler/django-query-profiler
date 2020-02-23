from collections import Counter
from unittest import TestCase

from django_query_profiler.query_profiler_storage import (
    QueryProfiledData, QueryProfiledSummaryData, QuerySignature, QuerySignatureStatistics, SqlStatement,
    StackTraceElement
)


class QuerySignatureStatisticsTest(TestCase):
    """ Tests for checking if "QuerySignatureStatistics" class is additive or not, and to verify if its correct """

    def test_query_signature_statistics_addition(self):
        query_signature_statistics_1 = QuerySignatureStatistics(
            frequency=1,
            query_execution_time_in_micros=11,
            db_row_count=111,)
        query_signature_statistics_2 = QuerySignatureStatistics(
            frequency=2,
            query_execution_time_in_micros=12,
            db_row_count=112, )

        query_signature_combined = query_signature_statistics_1 + query_signature_statistics_2
        self.assertEqual(query_signature_combined.frequency, 1 + 2)
        self.assertEqual(query_signature_combined.query_execution_time_in_micros, 11 + 12)
        self.assertEqual(query_signature_combined.db_row_count, 111 + 112)


class QueryProfiledDataTest(TestCase):
    """
    Tests for checking if "QueryProfiledData" class has the correct code for calculating summary, and if it is additive
    """

    query_without_params = "SELECT * FROM table WHERE id=%s"
    params = "1"
    django_stack_trace = [
        StackTraceElement('django.db', 'find', None),
        StackTraceElement('django.models', 'get', None),
        StackTraceElement('django.core', 'wsgi', None),
    ]
    app_stack_trace = [
        StackTraceElement('mysite.food', 'find_restaurant', 14),
        StackTraceElement('mysite.food', 'find_restaurant', 15),
        StackTraceElement('mysite.restaurant', 'get_restaurant', 15), ]
    target_db = 'master'

    query_signature_1 = QuerySignature(
        query_without_params=query_without_params,
        app_stack_trace=tuple(app_stack_trace),
        django_stack_trace=tuple(django_stack_trace),
        target_db=target_db)
    query_signature_statistics_1 = QuerySignatureStatistics(
        frequency=1,
        query_execution_time_in_micros=11,
        db_row_count=111, )

    query_signature_2 = QuerySignature(
        query_without_params=query_without_params,
        app_stack_trace=tuple(app_stack_trace[1:]),
        django_stack_trace=tuple(django_stack_trace[1:]),
        target_db=target_db)
    query_signature_statistics_2 = QuerySignatureStatistics(
        frequency=2,
        query_execution_time_in_micros=12,
        db_row_count=112)

    def test_query_profiled_data_summary(self):
        query_profiled_data = QueryProfiledData(
            query_signature_to_query_signature_statistics={
                self.query_signature_1: self.query_signature_statistics_1,
                self.query_signature_2: self.query_signature_statistics_2},
            _query_params_db_hash_counter=Counter(_Some_Hash_=3))
        query_profiled_summary_data = query_profiled_data.summary

        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 3}),
            exact_query_duplicates=3,
            total_query_execution_time_in_micros=11+12,
            total_db_row_count=111+112,
            potential_n_plus1_query_count=2)

        self.assertEqual(query_profiled_summary_data, expected_query_profiled_summary_data)
        self.assertIsNotNone(str(expected_query_profiled_summary_data))  # No exception thrown is the test here
        self.assertIsNotNone(str(self.query_signature_1))  # No exception thrown is the test here

    def test_query_profiled_data_addition_no_overlapping(self):
        """ Query signatures are unique in both query profiled data """
        query_profiled_data_1 = QueryProfiledData(
            query_signature_to_query_signature_statistics={self.query_signature_1: self.query_signature_statistics_1},
            _query_params_db_hash_counter=Counter(_Some_Hash_=1))

        query_profiled_data_2 = QueryProfiledData(
            query_signature_to_query_signature_statistics={self.query_signature_2: self.query_signature_statistics_2},
            _query_params_db_hash_counter=Counter(_Some_Hash_=2))

        combined_query_profiled_data = query_profiled_data_1 + query_profiled_data_2
        expected_query_profiled_data = QueryProfiledData(
            query_signature_to_query_signature_statistics={
                self.query_signature_1: self.query_signature_statistics_1,
                self.query_signature_2: self.query_signature_statistics_2},
            _query_params_db_hash_counter=Counter(_Some_Hash_=3))

        self.assertEqual(combined_query_profiled_data, expected_query_profiled_data)
        self.assertEqual(sum([query_profiled_data_1, query_profiled_data_2]), expected_query_profiled_data)

    def test_query_profiled_data_addition_overlapping(self):
        """ Query signature is shared between both query profiled data  """
        query_profiled_data_1 = QueryProfiledData(
            query_signature_to_query_signature_statistics={self.query_signature_1: self.query_signature_statistics_1},
            _query_params_db_hash_counter=Counter(_Some_Hash_=1))

        query_profiled_data_2 = QueryProfiledData(
            query_signature_to_query_signature_statistics={self.query_signature_1: self.query_signature_statistics_2},
            _query_params_db_hash_counter=Counter(_Some_Hash_=2))

        combined_query_profiled_data = query_profiled_data_1 + query_profiled_data_2
        expected_query_profiled_data = QueryProfiledData(
            query_signature_to_query_signature_statistics={
                self.query_signature_1: self.query_signature_statistics_1 + self.query_signature_statistics_2},
            _query_params_db_hash_counter=Counter(_Some_Hash_=3))

        self.assertEqual(combined_query_profiled_data, expected_query_profiled_data)
        self.assertEqual(sum([query_profiled_data_1, query_profiled_data_2]), expected_query_profiled_data)
