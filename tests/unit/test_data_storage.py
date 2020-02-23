from collections import Counter
from typing import Any
from unittest import TestCase

from django_query_profiler.query_profiler_storage import QueryProfiledSummaryData, QueryProfilerLevel, SqlStatement
from django_query_profiler.query_profiler_storage.data_collector import data_collector_thread_local_storage


class DataStorageTest(TestCase):
    """
    Tests for checking if nesting in context manager works as expected.  Every nested block should return ONLY
    the data that happened since the start of the block.  These tests are for verifying this.
    In a way, this test is to make sure that the stack implementation of "data_collector_thread_local_storage" works
    as it should
    """

    query_without_params = "SELECT 1 FROM table where id=%s"
    target_db = 'master'
    query_execution_time_in_micros = 1
    db_row_count = 12

    def setUp(self):
        data_collector_thread_local_storage.reset()

    def test_no_profiler_mode_on(self):
        self._add_query_to_storage(1)
        self._assert_empty_storage()

    def test_enter_and_exit_with_no_queries(self):
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        self.assertDictEqual(query_profiled_data.query_signature_to_query_signature_statistics, {})
        self.assertCountEqual(query_profiled_data._query_params_db_hash_counter, Counter())

    def test_one_query(self):
        """ When we have just one query executed"""
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage([1, 2, 3])
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        # Storage should be empty now
        self._assert_empty_storage()

        # Verifying what was stored by just comparing the summary object
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 1}),
            exact_query_duplicates=0,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros,
            total_db_row_count=self.db_row_count,
            potential_n_plus1_query_count=0)
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)

        summary_data_expected_dict = {
            "exact_query_duplicates": 0, "total_query_execution_time_in_micros": 1, "total_db_row_count": 12,
            "potential_n_plus1_query_count": 0, "SELECT": 1, "INSERT": 0, "UPDATE": 0, "DELETE": 0,
            "TRANSACTIONALS": 0, "OTHER": 0}
        self.assertDictEqual(query_profiled_data.summary.as_dict(), summary_data_expected_dict)

    def test_two_query_signatures(self):
        """ We have two queries each with different query signatures """
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))
        self._add_query_to_storage((1,))
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        # Storage should be empty now
        self._assert_empty_storage()

        # Verifying what was stored by just comparing the summary object
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 2}),
            exact_query_duplicates=2,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 2,
            total_db_row_count=self.db_row_count * 2,
            potential_n_plus1_query_count=2)  # Since query signature is different
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)

        # Verifying number of query_signatures in profiled data
        self.assertEqual(len(query_profiled_data.query_signature_to_query_signature_statistics), 1)

    def test_two_queries_same_query_signature(self):
        """ We  have two queries, and both of them have the same query signature.  We do this by using a loop"""
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        for _ in range(2):
            self._add_query_to_storage((1,))
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        # Storage should be empty now
        self._assert_empty_storage()

        # Verifying what was stored by just comparing the summary object
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 2}),
            exact_query_duplicates=2,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 2,
            total_db_row_count=self.db_row_count * 2,
            potential_n_plus1_query_count=2)  # Since query signature is same
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)

        # Verifying number of query_signatures in profiled data
        self.assertEqual(len(query_profiled_data.query_signature_to_query_signature_statistics), 1)

    def test_simple_nested_entry_exit_calls(self):
        """  This is a simulation when it is called from a context manager.  The exit function should return ONLY the
            query profiled data for calls that happened from innermost start

            This is the order of entry-exit in the context manager:
            enter
                1 query
                enter
                    2 queries
                exit -- This should return 2 queries data
            exit -- This should return all queries data

        """
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))
        self._add_query_to_storage((1,))

        # First exit testing
        first_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)

        # Size of list does not decrease, and stack should contain only first enter index
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 2)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 2}),
            exact_query_duplicates=2,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 2,
            total_db_row_count=self.db_row_count * 2,
            potential_n_plus1_query_count=2)  # Since query signature is different
        self.assertEqual(first_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

        # Second exit testing.  This should return *ALL* the queries data
        second_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()  # Storage must be empty now
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 3}),
            exact_query_duplicates=3,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 3,
            total_db_row_count=self.db_row_count * 3,
            potential_n_plus1_query_count=3)
        self.assertEqual(second_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

    def test_complex_nested_entry_exit_calls(self):
        """
        This is the order of entry-exit in the context manager:
        entry
            1 sql
            entry
                1 sql
                entry
                    0 sql
                exit --> should return 0 queries data

                entry
                    1 sql
                exit --> should return 1 queries data
            exit --> should return 2 queries data
        exit --> should return all queries data

        """

        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)

        # Before first exit
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 3)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1, 2])

        # First exit.
        first_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        # Size of list does not decrease, and stack should contain only first enter index
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 3)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter(),
            exact_query_duplicates=0,
            total_query_execution_time_in_micros=0,
            total_db_row_count=0,
            potential_n_plus1_query_count=0)
        self.assertEqual(first_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1,))

        # Before second exit
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1, 3])

        # Second exit
        second_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        # Size of list does not decrease, and stack should contain only first enter index
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 1}),
            exact_query_duplicates=0,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros,
            total_db_row_count=self.db_row_count,
            potential_n_plus1_query_count=0)
        self.assertEqual(second_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

        # Before third exit
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])

        # Third exit
        third_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        # Size of list does not decrease, and stack should contain only first enter index
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 2}),
            exact_query_duplicates=2,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 2,
            total_db_row_count=self.db_row_count * 2,
            potential_n_plus1_query_count=2)
        self.assertEqual(third_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

        # Before fourth exit
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])

        # Fourth exit
        fourth_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertFalse(data_collector_thread_local_storage._query_profiler_enabled)
        # Size of list does not decrease, and stack should contain only first enter index
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 0)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(
            sql_statement_type_counter=Counter({SqlStatement.SELECT: 3}),
            exact_query_duplicates=3,
            total_query_execution_time_in_micros=self.query_execution_time_in_micros * 3,
            total_db_row_count=self.db_row_count * 3,
            potential_n_plus1_query_count=3)
        self.assertEqual(fourth_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

    def _assert_empty_storage(self) -> None:
        """ This is a helper function for checking if thread local storage is all empty or not"""
        self.assertFalse(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertListEqual(data_collector_thread_local_storage._query_profiled_data_list, [])
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [])

    def _add_query_to_storage(self, params: Any) -> None:
        """
        This function adds one query to the thread local storage.  Note that the stack trace is calculated
        by the function data_collector_thread_local_storage#add_query_profiler_data, and hence if we are
        calling this function from different line numbers - they would have a different stack trace
        """
        data_collector_thread_local_storage.add_query_profiler_data(
            query_without_params=self.query_without_params,
            params=params,
            target_db=self.target_db,
            query_execution_time_in_micros=self.query_execution_time_in_micros,
            db_row_count=self.db_row_count
        )
