import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'psycopg2',
    'redis',
    'html5lib',
    'lxml',
    'suds',
    'pygeoip',
    'tweepy',
    'prettytable',
    'Mako==0.7.2',
    'simplejson',
    'webhelpers',
    'beaker',
    'pyramid_beaker',
    'decorator',
    'webtest',
    'nose',
    'nose-exclude',
    'pylint'
    ]

setup(name='app',
      version='0.0',
      description='app',
      long_description='app',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='app',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = app:main
      [console_scripts]
      initialize_app_db = app.scripts.initializedb:main
      """,
      )

