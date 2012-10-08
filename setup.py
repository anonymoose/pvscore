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
    'zope.sqlalchemy',
    'waitress',
    'psycopg2',
    'redis==2.6.0',
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
    'beaker_extensions==0.1.2dev',
    'decorator',
    'webtest',
    'nose',
    'nose-exclude',
    'pylint',
    'pyflakes',
    'feedparser',
    'selenium',
    'stripe'
    ]

setup(name='pvscore',
      version='0.0',
      description='pvscore',
      long_description=README,
      dependency_links = ['http://wwww.palmvalleysoftware.com/download/beaker_extensions-0.1.2dev.tar.gz#egg=beaker_extension-0.1.2dev'],
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

