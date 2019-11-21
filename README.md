
## About the project

This project implements a query profiler for django projects, using a concept called Query Signature.  This project 
helps django projects to not only profile queries, but also provides recommendation on how a developer can optimize code 
to avoid N+1 queries

The biggest performance problem with any ORM solution is N+1 queries, and (like all good ORM solutions) django provides
tools for developers to avoid these code paths. Django provides documentation & examples to use these optimization 
techniques correctly, and it is left upto developers to use these tools the right way

There are no tools in django that help identify which code paths are N+1, and none that can give recommendation to 
developers on what changes can rectify this problem.  This intent of this project is to fill this gap - to help 
developers identify N+1 code paths, and to give recommendation on what changes can remove this N+1 code path 
 
The tools that django provide for avoiding N+1 queries are:
1. select_related
2. prefetch_related


This [project](http://www.googgle.com) defines what is a N+1 query, what are the various optimization techniques that django 
provides, and how they are internally implemented in django.  This doc also defines how a query signature helps us in 
figuring out N+1 queries, and how it contains clues on finding what might be wrong with the query

#### Query Profiler in action

There are two ways to use this query profiler:
1. As a context manager/decorator in code.  This way, we could optimize any arbitrary code 
2. As a chrome plugin for requests/api's, using a django middleware.  The middleware internally use context manager, but
    adds various request headers that make the chrome plugin possible

This image shows the chrome plugin in action:
TODO: Add image

#### How to setup in your code

I. Setting up query profiler as a context manager require very minimal setup
   1. Install `django-query-profiler` in the project (by adding `django-query-profiler` in the requirements.txt of your project)
   2. In settings.py for your project, prepend `django-query-profiler` to the 'ENGINE' section of `DATABASES`.  E.g if your
    project uses mysql, this is what it would look like in settings.py file: 
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '/etc/mysql/my.cnf',
            },
        }
    }
    
    After configuring django-query-profiler, it would look this:
    DATABASES = {
        'default': {
            'ENGINE': 'django_query_profiler.django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '/etc/mysql/my.cnf',
            },
        }
    }

II. Setting up as chrome plugin require more steps, in addition to above two steps:
   1. Install redis
   2. In urls.py file of the application, just add this line, for adding a link for query profiler url (from chrome plugin):
      ```
      path('', include('django_query_profiler.frontend.urls'))
      ```
   3. Add this as the first line in the middleware:  `'django_query_profiler.client.middleware.QueryProfilerMiddleware'`
   4. Add the below snippet to settings.py file:

```
        QUERY_PROFILER_ENABLED: bool = True
        QUERY_PROFILER_REDIS_HOST: str = 'localhost'
        QUERY_PROFILER_REDIS_PORT: int = 6379
        QUERY_PROFILER_REDIS_DB: int = 0
        QUERY_PROFILER_KEYS_EXPIRY_SECONDS: int = 3600
        QUERY_PROFILER_APPS_TO_REMOVE = ('django', 'IPython', 'django_query_profiler', 'test')
        
        def QUERY_PROFILER_TYPE_FUNC(_):
            from django_query_profiler.query_signature import QueryProfilerType
            return QueryProfilerType.QUERY
   ```     
 
#### How code is organized
 
  Code is organized into 7 packages, where each package has its own README.md file, to follow along what that package do
  This is kind of a brief overview of what each package do (in the order of how they should be read):
   1. query_signature: [This](django_query_profiler/query_signature/README.md) package contains the core logic of this
                        profiler.  It has the functions which rest of the packages call - to start/stop the profiler and
                        record whene a query is fired
   2. django: [This](django_query_profiler/django/README.md) package contains instrumentation for various databases 
               which make django to use our instrumented cursor, which internall calls query_signature to record a query
   3. client: [This](django_query_profiler/client/README.md) package contains all the modules which any client of this
               profiler would interact with.  It contains the context manager, middleware etc
   4. chrome_plugin: [This](django_query_profiler/chrome_plugin/README.md) package contains the code for chrome_plugin
                      which any developer can use to see the results of their profiled application
   5. chrome_plugin_helpers:  [This](django_query_profiler/chrome_plugin_helpers/README.md) contains the helper module
                               for the chrome plugin
   6. templates: This package contains the templates which are used by chrome_plugin to display the output
   7. tests: This package contains the tests
     
 
