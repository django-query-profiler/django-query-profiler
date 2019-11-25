import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='django_query_profiler',
      version='0.1',
      description='Django query profiler',
      long_description=read('README.md'),
      url='',
      author='Yash Maheshwari, Glynn Morrison',
      author_email='yash.maheshwari@gmail.com, glynn@zenefits.com',
      license='BSD',
      packages=find_packages(),
      install_requires=['django', 'moz-sql-parser', 'redis', 'mmh3'],
      zip_safe=False,
      test_suite="tests",
      setup_requires=['flake8'])
