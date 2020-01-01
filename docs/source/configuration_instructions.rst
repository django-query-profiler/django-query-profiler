configuration instructions
==========================

:synopsis: configuring django-query-profiler in your project


as chrome plugin
^^^^^^^^^^^^^^^^
The only places where we will need to change are the settings.py and urls.py file.

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


See this `PR
<https://github.com/django-query-profiler/django-query-profiler-sample-app/pull/1>`_ on how to configure this in your application,
and how the plugin is going to look like after your configuration


as chrome plugin without detailed view
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We use redis to store the `detailed view`, that gets shown when clicking on the "Details Link" in the chrome extension
If redis is not available, we would not be able to see the detailed view, but we can still see the summary view.

In that scenario, the only change would be in the application's settings.py.  We don't need to add
`django_query_profiler` to INSTALLED_APPS, and we don't need to add detailed view url to urls.py


**settings.py**::

  from django_query_profiler.settings import *

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


See this `PR
<https://github.com/django-query-profiler/django-query-profiler-sample-app/pull/2>`_ on how to configure this in your application,
and how the plugin is going to look like after your configuration

as context manager
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

