configuration instructions
==========================

:synopsis: configuring django-query-profiler


As chrome plugin
^^^^^^^^^^^^^^^^
The only places where you will need to change in your application are the settings.py and urls.py file.
See this `example github project
<https://github.com/django-query-profiler/django-query-profiler-sample-app/commit/25bfb877a59ac39f107d2dc5b5e75236087ea99d>`_ on how to configure this in your application

**settings.py**::

      from django_query_profiler.settings import *

      INSTALLED_APPS = (
          ...
          'django_query_profiler',
          ...
      )

      MIDDLEWARE = (
          ...
           # Request and all middleware that come after our middleware, would be profiled
          'django_query_profiler.client.middleware.QueryProfilerMiddleware',
          ...
      )

      DATABASES = (
          ...
          # Adding django_query_profiler as a prefix to your ENGINE setting
          # Assuming old ENGINE was "django.db.backends.sqlite3", this would be the new one
          "ENGINE": "django_query_profiler.django.db.backends.sqlite3",
      )

**urls.py**::

      # Add this line to existing urls.py
      path('django_query_profiler/', include('django_query_profiler.client.urls'))


As context manager
^^^^^^^^^^^^^^^^^^

This is helpful if you want to test things out on a command line - it requires only one change to settings.py

**settings.py**::

      from django_query_profiler.settings import *

      DATABASES = (
          ...
          # Adding django_query_profiler as a prefix to your ENGINE setting
          # Assuming old ENGINE was "django.db.backends.sqlite3", this would be the new one
          "ENGINE": "django_query_profiler.django.db.backends.sqlite3",
      )

**your application or on command line**::

      from django_query_profiler.client.context_manager import QueryProfiler
      from django_query_profiler.query_signature import QueryProfilerLevel, QuerySignatureAnalyzeResult

      with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as query_profiler:
        # Your application code
        pizza = Pizza.objects.select_related('toppings').filter(is_vegetarian=False).first()
        str(pizza.toppings_of_best_pizza_serving_restaurants())

      print(query_profiler.query_profiled_data)
      print(query_profiler.query_profiled_data.query_signature_to_query_signature_statistics)

