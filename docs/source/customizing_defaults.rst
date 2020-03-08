customizing the defaults
========================

This doc covers how to change the `django-query-profiler` settings to suit your needs.  The attributes that the profiler
expects are in `django_query_profiler/settings.py
<https://github.com/django-query-profiler/django-query-profiler/blob/master/django_query_profiler/settings.py>`_ file

Irrespective of if you are using the chrome plugin, or the context manager, there is one line you would have added
to your application settings.py file, for configuring the profiler::

  from django_query_profiler.settings import *

If you want to change any of the defaults, you can import the file, and then define the same parameter again, but with a
different value

Here are some example of customizations that can be done:

- If redis is running on a different port, this is what you would have to do in the application settings.py::

    from django_query_profiler.settings import *
    DJANGO_QUERY_PROFILER_REDIS_PORT: int = 8080


- If we want to configure the profiler to be run on `certain` api's only.  The default setting is to run it on all api's.
  The way to change the defaults would be do something in the application settings.py::

    from django_query_profiler.settings import *
    from django_query_profiler.query_signature import QueryProfilerLevel

    def DJANGO_QUERY_PROFILER_LEVEL_FUNC(request):
      return QueryProfilerLevel.QUERY_SIGNATURE if request.path_info == '/pizza/order' else None


- A similar example is if you want the profiler to be run only when the request is coming from internal IPs.  Django
  request META contains the ipaddress, and that can be used to filter out only internal IP address where the profiler would
  be enabled


- If we want to do say, log the query profiled data to a log file.  The way to do it would be::

    from django_query_profiler.settings import *
    from django.http.response import HttpResponseBase
    from django.http import HttpRequest
    from django_query_profiler.query_profiler_storage import QueryProfiledData


    def DJANGO_QUERY_PROFILER_POST_PROCESSOR(
        query_profiled_data: QueryProfiledData,
        request: HttpRequest,
        response: HttpResponseBase) -> None:
      logger.info(query_profiled_data)


- If we want to remove a particular module from coming in the stack-trace, that gets shown in the detailed view::

    from django_query_profiler.settings import *

    DJANGO_QUERY_PROFILER_APP_MODULES_TO_EXCLUDE += ('package1', 'package2')


- An extreme example of customizations - one could write a new chrome plugin &/or your own middleware as well.  All
  `QueryProfilerMiddleware` is doing is to call the context manager, and set some headers which the chrome plugin
  interprets and append in its table.

   - Rolling out your own chrome plugin & the middleware, which calls the context manager is definitely doable.
   - The `DJANGO_QUERY_PROFILER_POST_PROCESSOR` function is called with the request, response & QueryProfiledData - before the response is sent back.  It can be used to set additional attributes on the response headers
   - Your application can set other attributes on the response, and your chrome plugin can read those attributes
   - If it is something others can also use, please consider sending a PR :-)
