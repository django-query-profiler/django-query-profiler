'''
This module defines a mixin, which can be used by all implementations for all databases.
All the databases have a different heirarchy of DatabaseWrapper, but all of them derive from BaseDatabaseWrapper
'''

from abc import ABC

from django.db.backends.utils import CursorWrapper, CursorDebugWrapper
from django.db.backends.base.base import BaseDatabaseWrapper

from .cursor_wrapper_instrumentation import QueryProfilerCursorWrapper, QueryProfilerCursorDebugWrapper


class QueryProfilerDatabaseWrapperMixin(BaseDatabaseWrapper, ABC):

    def cursor(self):
        cursor_wrapper = super().cursor()
        kwargs = dict(cursor=cursor_wrapper.cursor,
            db=cursor_wrapper.db,
            db_row_count=self.db_row_count(cursor_wrapper.cursor))

        if isinstance(cursor_wrapper, CursorDebugWrapper):
            return QueryProfilerCursorDebugWrapper(**kwargs)
        elif isinstance(cursor_wrapper, CursorWrapper):
            return QueryProfilerCursorWrapper(**kwargs)
        else:
            raise Exception("cursor_wrapper is not of either of {CursorWrapper, CursorDebugWrapper}.  Is it because of "
                            "new version of django?  Did you run the tests in the django_query_profiler - they must  "
                            "have failed")

    @staticmethod
    def db_row_count(cursor):
        '''
        Most database would not need to override this function.  Some like mysql might do - having it as a function
        leaves open the possibility (to override)
        '''
        return cursor.rowcount
