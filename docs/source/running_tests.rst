running tests
=============

Running test is as simple as running this command::

  python setup.py test

This would run the tests against a sqlite database

If your application has a mysql/postgresql/oracle test settings, you can pass the settings file and run this to use
your settings file::

  DJANGO_SETTINGS_MODULE=<your test settings> python setup.py test


If you want to run tests against the full matrix of python version supported and django version supported, run::

  tox

