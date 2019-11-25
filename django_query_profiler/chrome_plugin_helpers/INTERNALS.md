This package contains all the files required for enabling the chrome plugin.  It contains all the "helper" classes
which the client does not have to configure, but are required by the middleware/chrome plugin

1. redis_utils.py is for saving & retrieving [QueryProfiledData](../query_signature/__init__.py) the data from middleware
2. views.py define the view that gets invoked from the url that we add to chrome plugin.  The output is a html that
    displays the output of the profiled data
