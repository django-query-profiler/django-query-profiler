installation
============

requirements
^^^^^^^^^^^^

This works with any version of django >= 2.0, and running on python >= 3.6

for usage
^^^^^^^^^
Simplest way to get the profiler is to use pip, and installing chrome extension from chrome store:

- Python package::

   $ pip install django-query-profiler


  You can verify that the application is available on your PYTHONPATH by opening a python interpreter and entering the following commands::

  >>> import django_query_profiler
  >>> django_query_profiler.VERSION

- Chrome extension:  Download from chrome `webstore <https://chrome.google.com/webstore/detail/django-query-profiler/ejdgfhecpkhdnpdmdheacfmknaegicff>`__

Note that the chrome extension works on any chromium based browser.  We have tested it on Google Chrome and Brave Browser


for development
^^^^^^^^^^^^^^^
- clone the git repository for python package from GitHub and run setup.py::

     $ git clone git://github.com/django-query-profiler/django-query-profiler.git
     $ <venv activate command>
     $ cd django-query-profiler
     $ python setup.py test;  python setup.py install;

- clone the git repository for chrome plugin and add it to any chromium based browser::

    git clone git://github.com/django-query-profiler/django-query-profiler-chrome-plugin.git
    Open chrome://extensions (command works in any chromium based browser)
      - check Developer mode,
      - click on load unpacked.
      - Select the cloned package above

