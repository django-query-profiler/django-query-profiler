from django.db.models import Prefetch
from django.test import TestCase

from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel, QuerySignatureAnalyzeResult
from tests.integration.fixtures import bulk_create_toppings_pizzas_restaurants
from tests.testapp.food.models import Pizza, Restaurant


def run_twice_with_debug_toggled(test_func):
    """
    This decorator runs the same test twice - one with DEBUG=True, and one with DEBUG=False
    We want to do that because Django has two cursorWrapper - CursorWrapper and CursorDebugWrapper, and it
    chooses the one based on the settings DEBUG attribute
    """
    def wrapper(*args, **kwargs):
        self: TestCase = args[0]
        for debug in (True, False):
            with self.subTest():
                with self.settings(DEBUG=debug):
                    return test_func(*args, **kwargs)
    return wrapper


class QueryProfilerCodeSuggestions(TestCase):

    def setUp(self):
        bulk_create_toppings_pizzas_restaurants()

    @run_twice_with_debug_toggled
    def test_missing_prefetch(self):

        pizzas = Pizza.objects.all()
        # Pizzas __str__ references toppings, which we have not prefetched
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_without_prefetch:
            for pizza in pizzas:
                str(pizza)  # We can also print it

        query_signature_to_query_signature_statistics = \
            qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        # The first query would be for pizzas, and second one would be the call to toppings
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True
            elif query_signature_statistics.frequency == 3:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)
                checked_for_table_toppings = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)

    @run_twice_with_debug_toggled
    def test_after_applying_prefetch(self):

        pizzas = Pizza.objects.prefetch_related('toppings').all()
        # Pizzas __str__ references toppings, which we have now prefetched
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_with_prefetch:
            for pizza in pizzas:
                str(pizza)  # We can also print it

        query_signature_to_query_signature_statistics = \
            qp_pizzas_with_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        frequencies = {query_signature_statistics.frequency for query_signature_statistics in
                       query_signature_to_query_signature_statistics.values()}
        query_signature_analysis = {query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()}
        self.assertSetEqual(frequencies, {1})
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.UNKNOWN,
                                                       QuerySignatureAnalyzeResult.PREFETCHED_RELATED})

    @run_twice_with_debug_toggled
    def test_spicy_toppings_db_filtering(self):
        """ Test to verify that no amount of prefetching would help if we do db filtering"""

        # STEP 1: Without any prefetching
        pizzas = Pizza.objects.all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_without_prefetch:
            for pizza in pizzas:
                pizza.spicy_toppings_db_filtering()

        query_signature_to_query_signature_statistics = \
            qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True
            elif query_signature_statistics.frequency == 3:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)
                checked_for_table_toppings = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)

        # STEP 2:  Lets try prefetching
        pizzas = Pizza.objects.prefetch_related('toppings').all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_wit_prefetch:
            for pizza in pizzas:
                pizza.spicy_toppings_db_filtering()

        query_signature_to_query_signature_statistics = \
            qp_pizzas_wit_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        # Number of queries have increased by 1, since we did prefetching which could not be used
        self.assertEqual(len(query_signature_to_query_signature_statistics), 3)
        frequencies = [query_signature_statistics.frequency for query_signature_statistics in
                       query_signature_to_query_signature_statistics.values()]
        query_signature_analysis = {query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()}

        self.assertListEqual(frequencies, [1, 1, 3])
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.FILTER,
                                                       QuerySignatureAnalyzeResult.PREFETCHED_RELATED,
                                                       QuerySignatureAnalyzeResult.UNKNOWN})

    @run_twice_with_debug_toggled
    def test_spicy_toppings_python_filtering(self):
        """ Test to verify that if filtering is done in python, we have a chance to optimize """

        # STEP 1: Without any prefetching
        pizzas = Pizza.objects.all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_without_prefetch:
            for pizza in pizzas:
                pizza.spicy_toppings_python_filtering()

        query_signature_to_query_signature_statistics = \
            qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True
            elif query_signature_statistics.frequency == 3:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)
                checked_for_table_toppings = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)

        # STEP 2:  Lets try prefetching
        pizzas = Pizza.objects.prefetch_related('toppings').all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_pizzas_wit_prefetch:
            for pizza in pizzas:
                pizza.spicy_toppings_python_filtering()

        query_signature_to_query_signature_statistics = \
            qp_pizzas_wit_prefetch.query_profiled_data.query_signature_to_query_signature_statistics

        # Number of queries have increased by 1, since we did prefetching which could not be used
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        frequencies = [query_signature_statistics.frequency for query_signature_statistics in
                       query_signature_to_query_signature_statistics.values()]
        query_signature_analysis = {query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()}

        self.assertListEqual(frequencies, [1, 1])
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.UNKNOWN,
                                                       QuerySignatureAnalyzeResult.PREFETCHED_RELATED})

    @run_twice_with_debug_toggled
    def test_missing_select_related(self):
        """
        This function tests various select_related and prefetch_related on the function
        food.models.py#toppings_of_best_pizza_serving_restaurants
        """

        # STEP 1:  No select_related/prefetch_related
        pizza = Pizza.objects.first()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_no_prefetch_select_related:
            str(pizza.toppings_of_best_pizza_serving_restaurants())

        query_signature_to_query_signature_statistics = \
            qp_no_prefetch_select_related.query_profiled_data.query_signature_to_query_signature_statistics

        query_signature_analysis = [query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()]

        # We are missing prefetch to restaurants, which in turn is missing select_related to best_pizza, and then
        # prefetch to toppings
        expected_query_signature_analysis = [
            QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED,
            QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED,
            QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)

        # STEP 2:  Missing just the select_related to best_pizza and prefetch to toppings
        pizza = Pizza.objects.prefetch_related('restaurants').first()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_no_select_related:
            str(pizza.toppings_of_best_pizza_serving_restaurants())

        query_signature_to_query_signature_statistics = \
            qp_no_select_related.query_profiled_data.query_signature_to_query_signature_statistics

        query_signature_analysis = [query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()]
        # We have prefetch to restaurants, but restaurant is missing select_related to best_pizza, and then
        # prefetch to toppings
        expected_query_signature_analysis = [
            QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED,
            QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)

        # STEP 3:  Adding the select_related to best_pizza but still missing prefetch to toppings
        pizza = Pizza.objects.prefetch_related(
            Prefetch('restaurants', queryset=Restaurant.objects.select_related('best_pizza'))
        ).first()

        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp_no_select_related:
            str(pizza.toppings_of_best_pizza_serving_restaurants())

        query_signature_to_query_signature_statistics = \
            qp_no_select_related.query_profiled_data.query_signature_to_query_signature_statistics

        query_signature_analysis = [query_signature.analysis for query_signature in
                                    query_signature_to_query_signature_statistics.keys()]
        # We have prefetch to restaurants, but restaurant is missing select_related to best_pizza, and then
        # prefetch to toppings
        expected_query_signature_analysis = [QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)

        # STEP 4: Now Adding the prefetch_related to toppings as well
        # FIXME(Yash)  How to do prefetch on the best_pizza
