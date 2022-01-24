from typing import Dict

from django.test import TestCase

from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel, SqlStatement
from tests.integration.fixtures import bulk_create_toppings
from tests.testapp.food.models import Topping


class QueryCountTest(TestCase):

    def test_no_data_profiler_summary(self):
        """ Tests for the case when we don't have any data """

        with QueryProfiler(QueryProfilerLevel.QUERY) as empty_data:
            list(Topping.objects.all())
        summary_dict: Dict = empty_data.query_profiled_data.summary.as_dict()

        self.assertEqual(summary_dict[SqlStatement.SELECT.name], 1)
        self.assertEqual(summary_dict[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_dict[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.DELETE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.TRANSACTIONALS.name], 0)

    def test_bulk_create_toppings(self):
        """ Sql statements when bulk inserting """

        with QueryProfiler(QueryProfilerLevel.QUERY) as qp_bulk_create:
            bulk_create_toppings()
        summary_dict: Dict = qp_bulk_create.query_profiled_data.summary.as_dict()

        self.assertEqual(summary_dict[SqlStatement.SELECT.name], 0)
        self.assertEqual(summary_dict[SqlStatement.INSERT.name], 1)
        self.assertEqual(summary_dict[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.DELETE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.TRANSACTIONALS.name], 0)

    def test_non_bulk_create_toppings(self):
        """ Sql statements when creating without bulk_create"""

        with QueryProfiler(QueryProfilerLevel.QUERY) as qp_create:
            Topping.objects.create(name='olives', is_spicy=False)
            Topping.objects.create(name='pineapple', is_spicy=False)
            Topping.objects.create(name='pepperoni', is_spicy=True)
            Topping.objects.create(name='canadian_bacon', is_spicy=True)
            Topping.objects.create(name='mozzarella', is_spicy=False)
        summary_dict: Dict = qp_create.query_profiled_data.summary.as_dict()

        self.assertEqual(summary_dict[SqlStatement.SELECT.name], 0)
        self.assertEqual(summary_dict[SqlStatement.INSERT.name], 5)
        self.assertEqual(summary_dict[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.DELETE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.TRANSACTIONALS.name], 0)

    def test_delete_toppings(self):
        """ We would delete toppings in two ways and see the count of sql statements """
        bulk_create_toppings()

        with QueryProfiler(QueryProfilerLevel.QUERY) as qp_bulk_delete:
            Topping.objects.all().delete()
        summary_dict: Dict = qp_bulk_delete.query_profiled_data.summary.as_dict()

        # Since topping is also has a many-to-many relationship,  it has to delete the through table
        self.assertEqual(summary_dict[SqlStatement.SELECT.name], 1)
        self.assertEqual(summary_dict[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_dict[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_dict[SqlStatement.DELETE.name], 2)
        self.assertEqual(summary_dict[SqlStatement.TRANSACTIONALS.name], 0)
