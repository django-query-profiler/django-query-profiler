how the profiler works
======================

Basic Ideas
^^^^^^^^^^^

1. A N+1 query is one which runs the same query (with different params) for the `N related objects` - one for each N - in a loop

  - The best way to know if a `code path` is making N+1 calls is to capture the stack trace & the query, and see if the
    same stack trace & query combination appears again.
  - We can consider a (stack trace, query) as an aggregate, and maintain a map of this aggregate to count
  - We should segregate the stack trace into (application, django) stack trace.  An application stack trace is useful
    to be displayed, while a django stack trace is not
  - Can we do anything useful with the django stack trace?  Does it give us any useful insights - if not, we should
    discard it (Surprise: It does :-) )
  - Where do we store this data?  Maybe a thread-local?  Lets call this `data collector` module

2. For us to capture stack trace & the query, we have to hook into django to call our `data collector` when a query is executed

  - If we can hook into django to call our data collector when it executes any query, we can also collect other interesting
    properties, like `exact sql duplicates`, `row count`, and `time taken to run a query`
  - Does Django has hooks for us to execute some function when a query is executed?

3. Once we have the above two pieces figured out, we have to start collecting this data when a request happens, and stop when the request gets finished, ie. figure out the boundaries of profiling

  - A middleware seems like a good boundary, but that would limit us to just requests.
  - A context manager seems like a more generic boundary, and a django middleware can then just call the context manager.

4. Once we have this data, where should the data be displayed about the stack trace & the query

  - If it was called as part of context manager, user would know what to do with the data
  - If it was called as part of a request, chrome plugin seems like a good place for displaying this data.  Middleware can set the data in the headers,
    ideally a chrome plugin should be able to read that, and display it in the plugin



Implementation details
^^^^^^^^^^^^^^^^^^^^^^
This part is divided by the package that answers the four question/idea discussed above


1. query_profiler_storage
-------------------------

  - github `link
    <https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/query_profiler_storage>`__

  - This package has a `data_collector
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/data_collector.py>`__
    module where we define a thread-local which exposes three functions:

    - _`enter_profiler_mode`: Just sets the profiler to on state
    - _`exit_profiler_mode`: Turns off the profiler, and return the profiled data that has been collected since the start of enclosing start block
    - add_query_profiled_data:  If the profiler is on, start collecting data in its thread-local

  - We have defined our data models in the `__init__.py file
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/__init__.py>`__.
    All the bookkeeping code happens in these models, in the python magic functions like the `__add__` ones.

  - For capturing the stack trace, and segregating them into (application, django) stack trace, we have `stack_tracer
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/stack_tracer.py>`__ module

  - We are trying to use the django stack trace to figure out if the query is happening because of a forward or a reverse
    relationship, which helps us to know if this could have been avoided by a `select_related/prefetch_related`.

    This is happening in the `django_stack_trace_analyze
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/query_profiler_storage/django_stack_trace_analyze.py>`__ module.
    We are trying to analyze django stack trace, and see if we can find some useful known pattern

2. django
---------
  - github `link
    <https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/django>`__

  - To get a hook from django when it executes a query, that part is done in the `django
    <https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/django>`__ module.
    We are using the fact that django provides a way for us to pass a `DATABASE[ENGINE]` in the settings.py file, as a string.

    There are many open source projects which use this hook provided by django, to add some features when connecting to databases:

    - `django-postgres-readonly
      <https://github.com/opbeat/django-postgres-readonly>`__
    - `django-postgrespool
      <https://github.com/heroku-python/django-postgrespool>`__
    - `django-sqlserver
      <https://github.com/denisenkom/django-sqlserver>`__
    - `custom database backends
      <https://simpleisbetterthancomplex.com/media/2016/11/db.pdf>`__

    All the above packages have the same part about the `ENGINE` setting - the package has a base.py and __init__.py file.
    Looks like, this requirement is coming from `django code
    <https://github.com/django/django/blob/2.2/django/db/utils.py#L115-L119>`__.

  - To hook into the django query execution model, all the database in django have a common `CursorWrapper
    <https://github.com/django/django/blob/2.2/django/db/backends/utils.py>`__ implementation.  This cursor is the last
    point where we have python/django code.  After this layer, the code is handed to the various database drivers

    We change the cursorWrapper to our implementation in the module `cursor_wrapper_instrumentation.py
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/django/db/backends/cursor_wrapper_instrumentation.py>`__.
    We use a mixin module `database_wrapper_mixin.py
    <https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/django/db/backends/database_wrapper_mixin.py>`__ to do it once for all database, and configure this mixin for each database

    In case you are interested to learn about various layers in django, see `this
    <https://www.youtube.com/watch?v=tkwZ1jG3XgA>`__ amazing talk by James Bennett.  Watch it even if you don't use the profiler :-)

3. client
---------

  - github `link
    <https://github.com/django-query-profiler/django-query-profiler/tree/master/django_query_profiler/client>`__

  - In the above two modules, we already have all the machinery for the profiler.  The one thing that is remaining is to
    set the boundaries of the profiler - by calling the `enter_profiler_mode`_ and `exit_profiler_mode`_ functions.  That is exactly what the context manager does.

  - The middleware module just calls the context manager, and sets the headers which the chrome plugin expects


4. chrome plugin
----------------

  - github `link
    <https://github.com/django-query-profiler/django-query-profiler-chrome-plugin>`__

  - This is a different project in the repo.  All it does, is see if the headers in the request have the headers which the django query profiler sets.
    If it has, it parses the response, and add it to table in its devtools panel
