from typing import Optional

import django.db.backends.mysql.base as mysql_base

from django_query_profiler.django.db.backends.database_wrapper_mixin import QueryProfilerDatabaseWrapperMixin


class DatabaseWrapper(mysql_base.DatabaseWrapper, QueryProfilerDatabaseWrapperMixin):

    @staticmethod
    def db_row_count(cursor) -> Optional[int]:
        return cursor.rowcount if not cursor.connection.errno() else -1
