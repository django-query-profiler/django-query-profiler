#### How code is organized
 
  Code is organized into 6 packages, where some packages has their own INTERNALS.md file, to follow 
  along what that package do
  
  This is kind of a brief overview of what each package do (in the order of how they should be read):
   1. query_signature: [This](django_query_profiler/query_signature/INTERNALS.md) package contains the core logic of this
                        profiler.  It has the functions which rest of the packages call - to start/stop the profiler and
                        record when a query is fired
   2. django: [This](django_query_profiler/django/INTERNALS.md) package contains instrumentation for various databases 
               which make django to use our instrumented cursor, which internall calls query_signature to record a query
   3. client: [This](django_query_profiler/client/INTERNALS.md) package contains all the modules which any client of this
               profiler would interact with.  It contains the context manager, middleware etc
   4. chrome_plugin_helpers:  [This](django_query_profiler/chrome_plugin_helpers/INTERNALS.md) contains the helper modules
                               for the chrome plugin
   5. templates: This package contains the templates which are used by chrome_plugin to display the output
   6. tests: This package contains the tests
