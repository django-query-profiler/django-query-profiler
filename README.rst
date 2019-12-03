======================
 Django Query Profiler
======================

This project implements a query profiler for django projects. It integrates with any django project, and show all the queries that an application makes.

It highlights all the code paths which make N+1 calls, and also provide recommendation to developers on how to fix code


Getting Started
===============

TODO(Yash) Add a description copying from blog and the image.


Requirements
============

This works with any version of django running on python >= 3.6


Getting It
==========

1. Simplest way to install is to use pip, and installing chrome extension by:

    i.  $ pip install django-query-profiler
    ii. You can get the chrome plugin by installing it from here: https://www.google.com

2. If you want to install it from source:

    i. grab the git repository from GitHub and run setup.py::

        $ git clone git://github.com/django-query-profiler/django-query-profiler.git
        $ cd django-query-profiler
        $ python setup.py install

    ii. You can get the chrome extension by following these steps::

       git clone git://github.com/django-query-profiler/django-query-profiler-chrome-plugin.git
       Open chrome://extensions in any chromium based browser,
          - check Developer mode,
          - click on load unpacked.
          - Select the cloned package above

Installing It
=============

To enable `django_query_profiler` in your project you need to make a couple of changes in the application 
settings.py and urls.py files::

1. settings.py::
        
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
 2. urls.py: Add this line to the urls.py file of the application
        
        path('django_query_profiler/', include('django_query_profiler.client.urls'))

Using It
========

There are two ways to use this package.  One is to use chromium extension, and second is to use the command line:


