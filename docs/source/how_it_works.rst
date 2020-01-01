How the profiler works
======================

:synopsis: understanding the internals

Basic Ideas
^^^^^^^^^^^

1. A N+1 query is one which runs the same query for the `N related objects`, one for each N.

  - The best way to know if a `code path` is making N+1 calls is to capture the stack trace & the query, and see if the
    same stack trace & query combination appears again
  - We can consider a (stack trace, query) as an aggregate, and maintain a map of this aggregate to count
  - We should segregate the stack trace into (application, django) stack trace.  An application stack trace is useful
    to be displayed, while a django stack trace is not
  - Can we do anything useful with the django stack trace?  Does it give us any useful insights - if not, we should
    discard it

2. For us to capture stack trace & the query, we have to hook into django to call our data_collector when a query is
executed

  - If we can hook into django to call our data collector when it executes any query, we can also collect other interesting
    properties, like `exact sql duplicates`, `row count`, and `time taken to run a query`
  - If django does not provide any hooks, should we clone & modify django.  Should we monkey-patch?

3. Once we have the above two pieces figured out, we have to start collecting this data when a request happens, and stop
when the request gets finished, ie. figure out the boundaries of profiling

  - A middleware seems like a good boundary, but that would limit us to just requests.
  - A context manager seems like a more generic boundary, and a django middleware can then just call the context manager.

4. Once we have this data, we would like to display the stack trace & the query.  A natural place to do is the browser.

  - A chrome plugin seems like a good place for displaying this data
  - If a middleware sets the data in the headers, ideally a chrome plugin should be able to read that, and display it
    in the plugin


Implementation details
^^^^^^^^^^^^^^^^^^^^^^

1. query_profiler_storage
-------------------------

a. github `link
<https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/query_profiler_storage>`_

b. This package has a `data_storage
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/data_storage.py>`_
module where we define a thread-local which exposes three functions:

  - _`enter_profiler_mode`: Just sets the profiler to on state
  - _`exit_profiler_mode`: Turns off the profiler, and return the profiled data
  - add_query_profiled_data:  If the profiler is on, start collecting data in its thread-local

c. We have defined our data models in the `__init__.py file
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/__init__.py>`_
All the bookkeeping code happens in these models, in the python magic functions like the `__add__` ones.

d. For capturing the stack trace, and segregating them into (application, django) stack trace, we have `stack_tracer
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/stack_tracer.py>`_ module

e. We are trying to use the django stack trace to figure out if the query is happening because of a forward or a reverse
relationship, which helps us to know if this could have been avoided by a `select_related/prefetch_related`.

This is happening in the `query_signature_analyze
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/query_signature_analyze.py>`_ module.
We are trying to analyze django stack trace, and see if we can find some useful known pattern

2. django
---------
a. github `link
<https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/django>`_

b. To get a hook from django when it executes a query, that part is done in the `django
<https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/django>`_ module.
We are using the fact that django provides a way for us to pass a `DATABASE[ENGINE]` in the settings.py file, as a string.

There are many open source projects which use this hook provided by django, to add some features when connecting to databases:

  - `django-postgres-readonly
    <https://github.com/opbeat/django-postgres-readonly>`_
  - `django-postgrespool
    <https://github.com/heroku-python/django-postgrespool>`_
  - `django-sqlserver
    <https://github.com/denisenkom/django-sqlserver>`_
  - `custom database backends
    <https://simpleisbetterthancomplex.com/media/2016/11/db.pdf>`_

All the above packages have the same part about the `ENGINE` setting - the package has a base.py and __init__.py file.
Looks like, this requirement is coming from `django code
<https://github.com/django/django/blob/2.2/django/db/utils.py#L115-L119>`_.

c. Since our package should be useful for all databases that django supports, we have to follow this directory structure for each of the databases.
And to make it easier for developers to
We are going to follow the same structure as above packages, and follow the same package structure as django - so that it is easier to configure.
Just add `django_query_profiler` as prefix.

d. To hook into the django query execution model, all the database in django have a common `CursorWrapper
<https://github.com/django/django/blob/2.2/django/db/backends/utils.py>`_ implementation.  This cursor is the last
point where we have python/django code.  After this layer, the code is handed to the various database drivers

We change the cursorWrapper to our implementation in the module `cursor_wrapper_instrumentation.py
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/django/db/backends/cursor_wrapper_instrumentation.py>`_.
We use a mixin module `database_wrapper_mixin.py
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/django/db/backends/database_wrapper_mixin.py>`_ to do it once for all database, and configure this mixin for each database

In case you are interested to learn about various layers in django, see `this
<https://www.youtube.com/watch?v=tkwZ1jG3XgA>`_ amazing talk by James Bennett.
Watch it even if you don't use the profiler :-)

3. client
---------

a. github `link
<https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/client>`_

b. In the above two modules, we already have all the machinery for the profiler.  The one thing that is remaining is to
set the boundaries of the profiler - by calling the `enter_profiler_mode`_ and `exit_profiler_mode`_ functions.  That is exactly what the context manager does.

c. The middleware module just calls the context manager, and sets the headers which the chrome plugin expects







