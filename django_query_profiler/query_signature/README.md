This package contains all the modules which are needed for implementing query signature in django.  This 
[link](http://www.google.com) defines what a query signature is, and how it helps us to find N+1 code paths, and how
it contains hints to fix them.

Module level comments on each of the below modules explain more detailed implementation notes.  This is a very brief 
summary.  Click on each individual modules to read module level comments:

1. The most important and the most complex part of the module (and also of the whole project) is 
   [data_storage.py](data_storage.py).  It contains the code that the context manager calls to start/stop the profiler 
   for a block, and the cursor layer calls to record query details.  
2. There are two helper modules that data_storage.py calls:
    - stack_tracer.py: [This](stack_tracer.py) module contains code to record stack-trace where we segregate stack-trace
      into application & django's stack-trace.
    - query_signature_analyze.py: [This](query_signature_analyze.py) module contains code to find out what should be 
      changed in the code to remove N+1 code path.  This is dependent on the stack-trace that django code generates,
      and hence in a way, is susceptible to changes when django version changes.  To mitigate the risk, we have 
        i.  Used actual functions and derive strings for stack-trace from it -- if django renames these, or deletes them, 
            the code woudl fail rather than give incorrect results
        ii. Test cases that verify the output
3.  All the model definitions are in [__init__.py](__init__.py).  The most important part of the classes defined here
    is the implementation of python magic functions -- especially __ add __(self, other)
        
     
