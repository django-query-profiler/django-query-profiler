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

To get up and running quickly, :doc:`install django-query-profiler <installation>`, then read :doc:`configuration <configuration_instructions>`, which describes the steps for configuring the profiler in your application


.. toctree::
   :caption: Installation and configuration
   :maxdepth: 1

   installation
   configuration_instructions
   customizing_defaults
   choosing_profiler_level

.. toctree::
   :caption: For Contributors
   :maxdepth: 1

   how_it_works
   running_tests

.. toctree::
   :caption: Other documentation
   :maxdepth: 1

   chromium_plugin_columns
