This package contains code on how to intercept queries, and "do something/nothing" when a query is fired -   for all the
databases supported by django.
The "do something/nothing" part is the responsibility of [query_profiler_thread_local_storage](../query_signature/data_storage.py) 
add_query_profiler_data() function, and this package responsibility ends with delegating the call to that function.

1.  Now, to intercept queries, we have to figure out the last layer in django's layer system, after which python
    part is over, and the call is handed to database drivers.  It turns out, that layer is the Cursor layer - which is
    defined by every database.  As an example, look at [django sqlite3](https://github.com/django/django/blob/2.2/django/db/backends/sqlite3/base.py#L373)
    SQLiteCursorWrapper  
    (To learn about various layers in django, see [this](https://www.youtube.com/watch?v=tkwZ1jG3XgA&t=994s) talk by 
    James Bennett) 

2.  It looks like we have to wrap every such cursor in all databases to intercept the queries.  Not so fast!  It turns
    out that django wraps cursor of every database with a layer of its own.
     - These wrappers are in [django/db/backends/utils.py](https://github.com/django/django/blob/2.2/django/db/backends/sqlite3/base.py#L373): CursorWrapper/CursorDebugWrapper.  So, we would not have to wrap all the cursors, but just this one cursorwrapper.  
     - We have done this in the module [cursor_wrapper_instrumentation.py](db/backends/cursor_wrapper_instrumentation.py) for both 
        CursorWrapper and CursorDebugWrapper

3.  At this stage, we have a cursorWrapper implementation which does what we want to do.  Now we have to make sure that
    django uses our Cursorwrapper implementation, and not its own CursorWrapper.  There are three possible ways:
    -  Modify django
    -  Monkey patch django
    -  Django provides a way to customize databbase engine, which is taken as a string.  We can explore more into this

    Django provides this functionality of specifying database engine as a string, so that it can support other database
    backends.  E.g. there are projects which support Microsoft sql server, which is not included in django.
    
    **Basic Idea**
    
    The basic idea is - we can implement our own database engines, which delegates all resposbility to existing database
    engines except overriding the part of creating the cursor.  This way, all the clients would just have to change
    in settings.py, for getting this profiler.

    **Existing Implementation Examples**
    
    So, it looks like we can define our own DatabaseWrapper, which can inherit from each of the databases
    DatabaseWrapper, and just override the function that creates the cursor.  There are multiple open source projects
    that follow almost the same idea:
    - [Postgres read-only](https://github.com/opbeat/django-postgres-readonly)
    - [Microsoft sql server](https://github.com/denisenkom/django-sqlserver)
    - [Connection pooling](https://github.com/heroku-python/django-postgrespool)
    - [This](https://simpleisbetterthancomplex.com/media/2016/11/db.pdf) is a good document to read more

    The common theme in all the implementation is we have to define a package with base.py, having class DatabaseWrapper
    and then specifying it in DATABASE['ENGINE'] setting.  The requirement about defining a base.py file comes from this 
    function in django - "django/db/utils.py: [load_backend()](https://github.com/django/django/blob/2.2/django/db/utils.py#L115-L119)"

    This is the approach we are going to take.  For every database, we are going to define a package with base.py file
    , defining DatabaseWrapper which extends the base DatabaseWrapper for that database.  All we want is to change
    the part where cursor() is created.  Instead of the cursor that the database provides, we are going to insert
    our own implementation of cursor.

    **Implementation Details**
    
    Now, we know what we have to do, lets dive more for sqlite.  It would be the same for all other databases.
    Sqlite DatabaseWrapper extends from BaseDatabaseWrapper.  In BaseDatabaseWrapper, there is a function call cursor()
    which is the one called by django to return cursor.  Ahh!
    -  That is the function we would override, and return our own cursor.  We are doing this in [database_wrapper_mixin.py](db/backends/database_wrapper_mixin.py)
    -  To use QueryProfilerDatabaseWrapperMixin defined in the above module, we would just use multiple inheritance
        in the file [sqlite3/base.py](db/backends/sqlite3/base.py)
    - Changing the hierarchy for DatabaseWrapper, by making sure that BaseDatabaseWrapper is the last call in
      the hierarchy ==> the call to cursor() would stop at "QueryProfilerDatabaseWrapperMixin: cursor()" call
    -  Lets also make sure that the package structure resembles what is in django, so that for the client, the only
        change would be to prepend "django_query_profiler" to the DATABASE['ENGINE'] setting.  This is just to make it
        easier to configure profiler

    Once it is done for sqlite, it would follow the same for all databases.

4.  The final thing that we would want to do is - it would be a good idea to know the rowcount, since most of the
    database drivers provide it.  That seems like something that would be useful to know the number of rows a query
    returned, and that information is available in the cursor.  All we have to do is grab it.
    The only problem is that this information can change from database to database.  For most of them, its
    cursor.rowcount, but mysql for example, has a different way of dealing with errors.

    Since we have our own DatabaseWrapper for all databases now, lets add it in the mixin, and any database (especially
    mysql) can override it

    Thats all there is to "intercepting queries" part.  Lets see the "do something/nothing" implementation now
