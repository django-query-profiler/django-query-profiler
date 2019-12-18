#!/usr/bin/env python
import os
import sys
from typing import Type

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner

ARGS_TO_SETTINGS_FILE = {
    'sqlite': 'tests.testapp.sqlite_settings',
    'mysql': 'tests.testapp.mysql_settings',
    'postgres': 'tests.testapp.postgres_settings'
}


def _unit_tests(test_runner_instance: DiscoverRunner) -> int:
    failure_count = test_runner_instance.run_tests(['tests/unit'])
    return failure_count


def _integration_test(test_runner_instance: DiscoverRunner) -> int:
    failure_count = test_runner_instance.run_tests(['tests/integration'])
    return failure_count


def run_tests():
    db_name: str = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != 'test' else 'sqlite'
    settings_file: str = ARGS_TO_SETTINGS_FILE[db_name]
    print('==' * 80)
    print(db_name)
    print(settings_file)
    print('==' * 80)

    os.environ['DJANGO_SETTINGS_MODULE'] = settings_file
    django.setup()
    test_runner_class: Type[DiscoverRunner] = get_runner(settings)
    test_runner_instance: DiscoverRunner = test_runner_class(verbosity=2)

    integration_test_failure_count = _integration_test(test_runner_instance)
    unit_test_failure_count = _unit_tests(test_runner_instance)
    sys.exit(integration_test_failure_count + unit_test_failure_count)


if __name__ == "__main__":
    run_tests()
