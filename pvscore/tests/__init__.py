#pylint:disable-msg=C0103
import pdb, os, transaction
from unittest import TestCase
from webtest import TestApp
from pvscore.model.meta import Session
from pvscore.model.core.users import Users
from decorator import decorator
import pvscore.lib.util as util
import nose
from cStringIO import StringIO
import sys
from pvscore.model.crm.comm import Communication
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.company import Company
from pvscore.model.crm.product import Product, InventoryJournal
from pvscore.model.crm.journal import Journal
from pvscore.model.cms.site import Site
#from pvscore.lib.catalog import Catalog, Cart
import ConfigParser
import paste.deploy
from pyramid import testing
import logging

logger = logging.getLogger(__name__)

# Invoke websetup with the current config file
os.environ['PVS_TESTING'] = 'TRUE'
#SetupCommand('setup-app').run([pylons.test.pylonscore.config['__file__']])

environ = {}

UID = 'kenneth.bedwell@gmail.com'
PWD = 'Zachary234'
TEST_UID = 'test_kwbedwell@hotmail.com'
TEST_UID_PASSWORD = 'swordfish'
T_PRODUCT = 'Test Product for Nose'
SITEDOMAIN = 'healthyustore.net'

class TestController(TestCase):

    def setUp(self):
        from pvscore import command_line_main
        settings = paste.deploy.appconfig('config:unittest.ini', relative_to='.')
        app = command_line_main(settings)
        self.app = TestApp(app)
        self.site = Site.find_by_host(SITEDOMAIN)


    def tearDown(self):
        pass


    def quiet(self):
        self.old_stdout = sys.stdout #pylint: disable-msg=W0201
        self.old_stderr = sys.stderr #pylint: disable-msg=W0201
        sys.stdout = StringIO()
        sys.stderr = StringIO()


    def unquiet(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


    def get_host(self):
        return os.environ['PVS_HOST'] if 'PVS_HOST' in os.environ else 'www.healthyustore.net' #'ww.wealthmakers.com'


    def _get_headers(self, headers):
        return headers if headers else {'Host': self.get_host(),
                                        'HTTP_X_REAL_IP': '98.231.77.218', # a real PV ip addr.
                                        'X-Real-Ip': '98.231.77.218'
                                        }


    def login_crm(self, username='kenneth.bedwell@gmail.com', password='Zachary234'):
        # this sets the site it.
        self.get('/crm')

        # this logs us into that site.
        self.post('/crm/login', {'username': username,
                                 'password': password})
        assert self.site
        os.environ['enterprise_id'] = str(self.site.company.enterprise_id)

        user = Users.load(username)
        assert user is not None
        return user


    def logout_crm(self):
        try:
            R = self.get('/crm/company/enterprise/clearcache')
            R.mustcontain('ok')
            R = self.get('/crm/logout')
            self.site = None
        except Exception as exc:
            logger.debug(exc)
        self.app.reset()
        return True


    def get(self, url, params=None, headers=None):
        resp = self.app.get(url, params=params, headers=self._get_headers(headers))
        if resp.status_int in [302, 301]:
            resp = resp.follow()
            if resp.status_int in [302, 301]:
                resp = resp.follow()
        return resp


    def post(self, url, params=None, headers=None):
        if params == None:
            params = {}
        resp = self.app.post(url, params=params, headers=self._get_headers(headers))
        if resp.status_int in [302, 301]:
            resp = resp.follow()
            if resp.status_int in [302, 301]:
                resp = resp.follow()
        return resp


    def commit(self):
        transaction.commit()


def secure(func, username='kenneth.bedwell@gmail.com', password='Zachary234'):
    def wrap(self):
        self.login_crm(username, password)
        ret = func(self)
        self.logout_crm()
        return ret
    wrap.__name__ = func.__name__
    return wrap


def quiet(func):
    def wrap(self):
        self.quiet()
        ret = func(self)
        self.unquiet()
        return ret
    wrap.__name__ = func.__name__
    return wrap
