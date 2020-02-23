installation
============

for usage
^^^^^^^^^
Simplest way to get the profiler is to use pip, and installing chromium extension from chrome store:

- Python package::

   $ pip install django-query-profiler


  You can verify that the application is available on your PYTHONPATH by opening a python interpreter and entering the following commands::

  >>> import django_query_profiler
  >>> django_query_profiler.VERSION

- Chromium extension::

     https://www.google.com


for development
^^^^^^^^^^^^^^^
- clone the git repository for python package from GitHub and run setup.py::

     $ git clone git://github.com/django-query-profiler/django-query-profiler.git
     $ <venv>
     $ cd django-query-profiler
     $ python setup.py test;  python setup.py install;

- clone the git repository for chromium plugin and add it to any chromium based browser::

    git clone git://github.com/django-query-profiler/django-query-profiler-chrome-plugin.git
    Open chrome://extensions in any chromium based browser,
      - check Developer mode,
      - click on load unpacked.
      - Select the cloned package above

