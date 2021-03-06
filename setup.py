import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'pyramid_exclog',
    'zope.sqlalchemy',
    'waitress',
    #'psycopg2',
    'psycopg2ct',
    'redis',
    'html5lib',
    'lxml',
    'suds',
    'pygeoip',
    'tweepy',
    'prettytable',
    'Mako',
    'simplejson',
    'webhelpers',
    'beaker',
    'pyramid_beaker',
    'beaker_extensions',
    'decorator',
    'webtest',
    'nose',
    'nose-exclude',
    'pylint',
    'pyflakes',
    #'feedparser',
    'selenium',
    'stripe',
    'PyRSS2Gen',
    'nose-cov',
    'pytz',
    'pycurl',
    'coverage',
    'restkit',
    'oauth2',
    'certifi',
    'beautifulsoup4'
    #'pandas',
    #'numexpr',
    #'Cython'
    #'requests==0.8.8'
    ]

setup(name='pvscore',
      version='0.0',
      description='pvscore',
      long_description=README,
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
      test_suite='pvscore',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = pvscore:main
      [console_scripts]
      initialize_pvscore_db = pvscore.scripts.initializedb:main
      """,
      )

