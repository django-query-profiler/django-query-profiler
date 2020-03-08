running tests
=============

Running test is as simple as running this command::

  python setup.py test

This would run the tests against a sqlite database

If your application has a mysql/postgresql/oracle test settings, you can pass the settings file and run this to use
your settings file::

  DJANGO_SETTINGS_MODULE=<your test settings> python setup.py test

As an example, see tox file to see how we are passing this environment variable to run tests for mysql/postgres/sqlite

If you want to run tests against the full matrix of python version supported and django version supported, for all the drivers supported by Django, run::

  tox


This is how we are also running tests on travisCI - so that all changes to the project are tested for all the above combinations
