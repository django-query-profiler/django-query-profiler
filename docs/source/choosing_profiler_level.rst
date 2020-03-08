choosing profiler level
=======================

Explaining profiling levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two levels of query profiler, and both of them have different capabilities, and different overheads.  The
idea to have two different levels is to allow the application developer to choose the right level, based on how much
overhead is acceptable for their API.

Currently, there are two levels of profiling:

1. **QUERY_SIGNATURE**:  This is the mode where we capture the query as well as the stack-trace.   The grouping unit here is
(stack-trace, normalized sql), and that grouping helps us to figure out if there are N+1 code paths.  Django stack-trace
helps us find recommendations - like if a particular query can be stopped by applying select_related/prefetch_related

The main overhead comes from calculating stack-traces whenever a query is executed, and for normalizing sql by applying
a regex.  From our experience of using it in production, the overhead is generally to the order of
**1 millisecond per 7 queries**

2. **QUERY**: This is the mode where we just capture queries, and *not* the stack-trace.  The grouping unit here is just
(sql).  Because we don't have access to stack-traces, we don't know if any code path is N+1 or not.  We don't
have any code recommendation either.

From our experience of using it, the overhead is generally to the order of **1 millisecond per 25 queries**


Configuring profiling levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the overhead that profiler adds for every query, the profiler level can be configured in the application
settings.py file.

1. The default setting is to run the profiler in `QUERY_SIGNATURE` level.  If you want to run the application in QUERY level,
this is how you should configure in your settings.py file::

    from django_query_profiler.settings import *
    from django_query_profiler.query_profiler_storage import QueryProfilerLevel

    def DJANGO_QUERY_PROFILER_LEVEL_FUNC(request) -> Optional[QueryProfilerLevel]:
      return QueryProfilerLevel.QUERY


2. If you want to configure it per request, the profiler provides a hook for changing the profiler type given a request object

  The profiling level of each API is calculated per request, and can be configured easily.
  See :doc:`customizing_defaults<../customizing_defaults/>` on how this can be done

