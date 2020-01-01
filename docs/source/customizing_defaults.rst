customizing the defaults
========================

:synopsis: customize the profiler as per your application needs

How to change the `django-query-profiler` settings to suit your needs.  The attributes that the app expects are
in `django_query_profiler/settings.py` file


If you are using the chrome plugin, or the context manager, there is one line you would have added to your application
settings.py file::

  from django_query_profiler.settings import *

If you want to change any of the defaults, you can import the file, and then define the same parameter again, but with a
different value

1. Let's say that the redis is running on a different port, this is what you would have to do in the application
settings.py::

    from django_query_profiler.settings import *
    DJANGO_QUERY_PROFILER_REDIS_PORT: int = 8080

2. To take another example, lets say that you want to configure the profiler to be run on certain API's only.  The default
setting is to run it on all API's.  The way to change the defaults would be do something in the application
settings.py::

    from django_query_profiler.settings import *
    from django_query_profiler.query_signature import QueryProfilerLevel

    def DJANGO_QUERY_PROFILER_LEVEL_FUNC(request):
      return QueryProfilerLevel.QUERY_SIGNATURE if request.path_info == '/pizza/order' else None

3. Another example could be if we want to do say, log the query profiled data to a log file.  The way to do it would be::

    from django_query_profiler.settings import *
    from django.http.response import HttpResponseBase
    from django_query_profiler.query_signature import QueryProfiledData


    def DJANGO_QUERY_PROFILER_QUERY_PROFILED_DATA_POST_PROCESSING(
        query_profiled_data: QueryProfiledData,
        response: HttpResponseBase) -> None:
      logger.info(query_profiled_data)


4. An extreme example of customizations - one could write a new chrome plugin &/or your own middleware as well.  All
`QueryProfilerMiddleware` is doing is to call the context manager, and set some headers which the chrome plugin
interprets and append in its table.

Rolling out your own chrome plugin & the middleware, which calls the context manager is also doable.
If it is something others can also use, please contribute back :-)
