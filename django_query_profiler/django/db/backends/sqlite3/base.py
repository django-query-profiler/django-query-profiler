import django.db.backends.sqlite3.base as sqlite_base

from django_query_profiler.django.db.backends.database_wrapper_mixin import QueryProfilerDatabaseWrapperMixin


class DatabaseWrapper(sqlite_base.DatabaseWrapper, QueryProfilerDatabaseWrapperMixin):
    pass
