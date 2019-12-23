#!/usr/bin/env python
import os
import sys
from typing import Type, Union

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner

ARGS_TO_SETTINGS_FILE = {
    'sqlite': 'tests.testapp.sqlite_settings',
    'mysql': 'tests.testapp.mysql_settings',
    'postgres': 'tests.testapp.postgres_settings',
    'test': 'tests.testapp.sqlite_settings',
}

DJANGO_SETTINGS_MODULE = 'DJANGO_SETTINGS_MODULE'


def _unit_tests(test_runner_instance: DiscoverRunner) -> int:
    failure_count = test_runner_instance.run_tests(['tests/unit'])
    return failure_count


def _integration_test(test_runner_instance: DiscoverRunner) -> int:
    failure_count = test_runner_instance.run_tests(['tests/integration'])
    return failure_count


def run_tests():
    """
    This is the main function that calls all the tests - though passing params here is a bit tricky. This function is
    also configured in setup.py/setup.cfg, so that is another way to call all the tests.  Two points about it:

    1. We should know what settings file we should use.  If the DJANGO_SETTINGS_MODULE is populated, we are going
        to use that.  Any parameter passed after this is set are not used
    2. Python setup.py test does not support any passed parameters, so the only way to change which settings file to
        use, is to set DJANGO_SETTINGS_MODULE
        The value of sys.argv[1] == test here.

    Based on the above two points, these are the valid ways of calling tests:

    1. ./runtests.py:  Since nothing about settings is passed, we pick up sqlite
    2. DJANGO_SETTINGS_MODULE=settings_file ./runtests.py
    3. ./runtests.py {sqlite, test, mysql, postgres}:  This is added for calling it from travisCI/tox, because it was
        not straightforward to call via setting the DJANGO_SETTINGS_MODULE
    4. python setup.py test:  We assume sqlite
    5. DJANGO_SETTINGS_MODULE=settings_file python setup.py test
    """

    is_os_environ_set = DJANGO_SETTINGS_MODULE in os.environ
    if not is_os_environ_set:
        db_name: str = sys.argv[1] if len(sys.argv) > 1 else 'sqlite'
        settings_file: str = ARGS_TO_SETTINGS_FILE[db_name]
        os.environ[DJANGO_SETTINGS_MODULE] = settings_file
    django.setup()

    test_runner_class: Type[DiscoverRunner] = get_runner(settings)
    test_runner_instance: DiscoverRunner = test_runner_class(verbosity=2)

    integration_test_failure_count = _integration_test(test_runner_instance)
    unit_test_failure_count = _unit_tests(test_runner_instance)
    sys.exit(integration_test_failure_count + unit_test_failure_count)


if __name__ == "__main__":
    run_tests()
