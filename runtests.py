#!/usr/bin/env python
import os
import sys
from typing import Type

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner


def run_tests():
    """
    This is the main function that calls all the tests.  It expects that the DJANGO_SETTINGS_MODULE would be set
    by the caller of this function.  If nothing's set, we expect it to be run on sqlite
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.testapp.sqlite_settings')
    django.setup()

    test_runner_class: Type[DiscoverRunner] = get_runner(settings)
    test_runner_instance: DiscoverRunner = test_runner_class(verbosity=2)

    sys.exit(bool(test_runner_instance.run_tests(["tests"])))


if __name__ == "__main__":
    run_tests()
