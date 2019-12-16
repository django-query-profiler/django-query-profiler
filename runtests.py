#!/usr/bin/env python
import os
import sys
from typing import Type

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.integration.setup.test_settings'
    django.setup()
    test_runner_class: Type[DiscoverRunner] = get_runner(settings)
    test_runner_instance: DiscoverRunner = test_runner_class(verbosity=2)
    failures = test_runner_instance.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()
