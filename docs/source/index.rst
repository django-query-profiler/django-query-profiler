.. django-query-profiler documentation master file, created by
   sphinx-quickstart on Tue Dec 24 14:23:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-query-profiler's documentation!
=================================================

Django query profiler is a profiler for Django applications, for helping developers answer the question "My Django code or page or API is slow, How do I find out why?"

Below are some of the features of the profiler:

1. Shows code paths making N+1 sql calls:  Shows the sql with stack_trace which is making N+1 calls, along with sql count
2. Shows the proposed solution: If the solution to reduce sql is to simply apply a select_related or a prefetch_related, this is highlighted as a suggestion
3. Shows exact sql duplicates: Count of the queries where (sql, parameters) is exactly the same.  This is the kind of sql where implementing a query cache would help
4. Flame Graph visualisation: Collects all the stack traces together to allow quickly identifying which area(s) of code is producing the load
5. Command line or chrome plugin: The profiler can be called from command line via context manager, or can be invoked via a middleware, and output shown in a chrome plugin
6. Super easy to configure in any application:  The only changes are in settings.py file and in urls.py file

To get up and running quickly, :doc:`install django-query-profiler <installation>`, then read :doc:`configuration <configuration_instructions>`, which describes the steps for configuring the profiler in your application


.. toctree::
   :caption: Installation and configuration
   :maxdepth: 1

   installation
   configuration_instructions
   choosing_profiler_level
   customizing_defaults

.. toctree::
   :caption: For Contributors
   :maxdepth: 1

   how_it_works
   running_tests

.. toctree::
   :caption: Other documentation
   :maxdepth: 1

   chrome_plugin_columns
