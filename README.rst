======================
Django Query Profiler
======================

.. image:: https://img.shields.io/pypi/l/django.svg
   :target: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/LICENSE?token=AN2LDYBKJNBDZZC3ZCNAJHK56RD2I

.. image:: https://travis-ci.com/django-query-profiler/django-query-profiler.svg?token=fxUKyqwxKVZEiBwbsjxt&branch=master
    :target: https://travis-ci.com/django-query-profiler/django-query-profiler



This project implements a query profiler for django projects. It integrates with any django project, and show all the
queries that an application makes.

It highlights all the code paths which make N+1 calls, and also provide recommendation to developers on how to fix code

There are two levels of the profiler, and the application can dynamically choose the level::

  1. QUERY_SIGNATURE:  This mode groups the queries by (app_stack_trace, normalized_query), and show the code paths
    that are making N+1 sql calls.  It also captures the django_stack_trace, and uses predefined rules to figure out
    if this code path is missing a select_related or a prefetch_related.  This way, it also gives recommendation to
    developers on if & how their N+1 code can be fixed
    This mode adds more overhead to the api.
  2. QUERY:  This mode groups the query by (normalized_query).  We don't capture the stack_trace, so this level is the
    'lighter' version.  It adds much less overhead.

There are two ways to use the profiler.  The output is exactly same, just that the workflow is different::

  1. Chromium plugin:  This mode is well suited when debugging a UI application
  2. Context manager:  This is more suited when you are trying to reason about the number of calls a function or a block
    of code makes.

Getting Started
===============

TODO(Yash) Add a description copying from the blog and the image.


Requirements
============

This works with any version of django running on python >= 3.6


Getting It
==========

1. Simplest way to install is to use pip, and installing chromium extension from chrome store:

  i. Python package::

      $ pip install django-query-profiler

  ii. Chrome extension::

        https://www.google.com

2. If you want to install it from source:

  i. grab the git repository from GitHub and run setup.py::

     $ git clone git://github.com/django-query-profiler/django-query-profiler.git
     $ cd django-query-profiler
     $ python setup.py install

  ii. You can get the chromium extension by following these steps::

       git clone git://github.com/django-query-profiler/django-query-profiler-chrome-plugin.git
       Open chrome://extensions in any chromium based browser,
         - check Developer mode,
         - click on load unpacked.
         - Select the cloned package above

Installing It
=============

To enable `django_query_profiler` in your project you need to make a couple of changes in the application
settings.py and urls.py files:

1. **settings.py**::

    from django_query_profiler.settings import *

    INSTALLED_APPS = (
        ...
        'django_query_profiler',
        ...
    )

    MIDDLEWARE = (
        'django_query_profiler.client.middleware.QueryProfilerMiddleware',
        ...
    )

    DATABASES = (
        ...
        # Adding django_query_profiler as a prefix to your ENGINE setting
        # Assuming old ENGINE was "django.db.backends.sqlite3", this would be the new one
        "ENGINE": "django_query_profiler.django.db.backends.sqlite3",
    )

2. **urls.py**::

      path('django_query_profiler/', include('django_query_profiler.client.urls'))

Using It
========

There are two ways to use this package.  One is to use chromium extension, and second is to use the command line.

  1. For using the chromium plugin, please refer to the gif image above.
  2. For using the command line, TODO(Yash)

Profiler Overhead
=================

The output of the profiler shows the overhead that is added because of using this profiler.

There are two levels of the profiler, and both of them have different overheads.  This is based on our experience of
using this profiler in production::

  1. When the level of the profiler is set to `query_signature`, the profiler adds almost 1 millisecond per 7 queries.
     This overhead happens because we have to capture the stack-trace whenever django executes a query, and to normalize
     the query by using a regex
  2. When the level of the profiler is set to `query`, the profiler adds almost 1 millisecond per 25 queries.  This
     overhead is because of regex for normalizing the query (for grouping all the queries together)

The idea to have two levels of the profiler is to allow for the user to decide on how much profiler cost

For contributors
================

The Django Debug Toolbar is released under the BSD license, like Django itself. If you like it, please consider contributing!
We have written about the inner workings of the package, and how code is organized in the
:doc: INTERNALS.md file
