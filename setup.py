from setuptools import setup, find_packages

setup(name='django_query_profiler',
      version='0.1',
      description='Django query profiler using query signature',
      url='',
      author='',
      author_email='',
      license='BSD',
      packages=find_packages(),
      install_requires=['django', 'moz-sql-parser', 'redis', 'mmh3'],
      zip_safe=False)

