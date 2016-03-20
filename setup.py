import os

from setuptools import setup, find_packages

setup(
  name='tags_counter',
  version='0.1.0',
  description='html tags counter.',
  long_description=('REST service, count html tags on page, using celery'),
  url='http://github.com/harlov/tags_counter',
  license='MIT',
  author='Harlov Nikita',
  author_email='nikita@harlov.com',
  packages=['tags_counter'],
  install_requires=[
    'flask==0.10',
    'marshmallow==2.6.1',
    'flask_script==2.0.5',
    'Celery==3.1.23',
    'pymongo==3.2.2',
    'requests[security]==2.9.1',
    'requests_mock==0.7.0',
    'gunicorn==19.4.5'
  ],
  include_package_data=True,
  entry_points = {
  'console_scripts': [
    'run_wsgi = scripts:run_wsgi.sh'
  ]
  },
  package_data={
    'config': 'config/*',
    },
  classifiers=[
    "Private :: Do Not Upload"
  ],
)