This package contains all the modules that anyone who uses django_query_profiler would use.  This is the only module
which would be imported, by the clients

There are two ways to use the query profiler:
1. Using the context manager/decorator around blocks of code which you want to profile.  This is defined in 
    [context_manager](context_manager.py)
2. Using middleware, if you want to profile the api/request.  This approach is more suited when used in conjunction with
    the chrome plugin.  This is defined in [middleware](middleware.py)
    - For using middleware, we upload the data to redis, and expose an endpoint for accessing the data.  The url
      is used as a column in every row of chrome plugin's table.  Clients have to include this [url](urls.py) in their 
      urlpatterns

