======================
Django Query Profiler
======================

.. image:: https://img.shields.io/pypi/l/django.svg
   :target: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/LICENSE

.. image:: https://travis-ci.com/django-query-profiler/django-query-profiler.svg?branch=master
    :target: https://travis-ci.com/django-query-profiler/django-query-profiler

.. image:: https://codecov.io/gh/django-query-profiler/django-query-profiler/branch/master/graph/badge.svg?token=1Cv7WsOi2W
  :target: https://codecov.io/gh/django-query-profiler/django-query-profiler

.. image:: https://readthedocs.org/projects/django-query-profiler/badge/?version=latest
  :target: https://django-query-profiler.readthedocs.io/en/latest/index.html


This project implements a query profiler for django projects. It tries to answer the question
"My Django page or API is slow, How do I find out why?".  It highlights all code paths that make N+1 calls to the
database, and also provide recommendation to developers on how N+1 can be fixed

This image shows the profiler in action:

.. image:: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/docs/_static/django_query_profiler_in_action.gif


Getting Started
===============

The simplest way to getting started is to install the django query profiler from pip, and get the chrome plugin from
chrome web store.

Python package::

  pip install django-query-profiler

Chrome Plugin:
  `chrome webstore <https://chrome.google.com/webstore/devconsole/24f090a4-0ba1-4744-b291-1c723f6b1e5d/abdcoolndccdlolelmkdobbcbcjnmblh/edit/package?hl=en>`_

These steps are explained in detail in the `docs <https://django-query-profiler.readthedocs.io/en/latest/installation.html>`__

The next step is to configure in your application by making changes to settings.py and urls.py file.
These steps are explained in detail in the `docs <https://django-query-profiler.readthedocs.io/en/latest/configuration_instructions.html>`__

Requirements
============

This works with any version of django >= 2.0, and running on python >= 3.6

Documentation
=============

Full documentation is available at `readthedocs <https://django-query-profiler.readthedocs.io/en/latest/index.html>`__

For contributors
================

The django query profiler is released under the BSD license, like Django itself.

If you like it, please consider contributing!  How the code is organized, and how the profiler works is documented in the `docs <https://django-query-profiler.readthedocs.io/en/latest/how_it_works.html>`__
