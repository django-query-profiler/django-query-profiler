.. django-query-profiler documentation master file, created by
   sphinx-quickstart on Tue Dec 24 14:23:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-query-profiler's documentation!
=================================================

Django query profiler is a sql profiler for the Django framework.  It allows easy integration with any
django project, and show all the queries that an django application makes.

It detects all the code paths that are making N+1 calls, and provide a recommendation to the developers, on how the code
could be fixed.

Getting Started
===============

TODO(Yash) Add a description copying from the blog and the image.

Installing It
=============

1. Simplest way to get the profiler is to use pip, and installing chromium extension from chrome store:

  i. Python package::

      $ pip install django-query-profiler

  ii. Chromium extension::

        https://www.google.com

You can verify that the application is available on your PYTHONPATH by opening a python interpreter and entering the following commands::

  >>> import django_query_profiler
  >>> django_extensions.VERSION

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

Configuring in your application
===============================

Please follow this link :doc:`configuration_instructions`. Enjoy.


Contents
========

.. toctree::
   :maxdepth: 3

   configuration_instructions



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
