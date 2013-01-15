#pylint:disable-msg=C0103
import os, transaction
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
from pvscore.model.crm.company import Company, Enterprise
from pvscore.model.crm.product import Product, InventoryJournal
from pvscore.model.crm.journal import Journal
from pvscore.model.cms.site import Site
#from pvscore.lib.catalog import Catalog, Cart
import ConfigParser
import paste.deploy   #pylint: disable-msg=F0401
from pyramid import testing
import logging
from pvscore import command_line_main

logger = logging.getLogger(__name__)
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
#logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)

environ = {}

PVS_ROOT_UID = 'kenneth.bedwell@gmail.com'
PVS_ROOT_PWD = 'Zachary234'

UID = 'supplement@pppvonline.com'
PWD = 'password'

TEST_UID = 'test_kwbedwell@hotmail.com'
TEST_UID_PASSWORD = 'swordfish'
T_PRODUCT = 'Test Product for Nose'
TEST_CUSTOMER_EMAIL = 'kenneth.bedwell@gmail.com'
TEST_CUSTOMER_PASSWORD = 'password'

class TestController(TestCase):

    def init_app(self, settings):
        return command_line_main(settings)

    def setUp(self):
        self.settings = paste.deploy.appconfig('config:unittest.ini', relative_to='.')
        app = self.init_app(self.settings)
        self.app = TestApp(app)
        self.site = Site.find_by_host(self.get_host())


    def tearDown(self):
        pass


    # def quiet(self):
    #     self.old_stdout = sys.stdout #pylint: disable-msg=W0201
    #     self.old_stderr = sys.stderr #pylint: disable-msg=W0201
    #     sys.stdout = StringIO()
    #     sys.stderr = StringIO()


    # def unquiet(self):
    #     sys.stdout = self.old_stdout
    #     sys.stderr = self.old_stderr


    def get_host(self):
        return os.environ['PVS_HOST'] if 'PVS_HOST' in os.environ else 'healthyustore.net' #'ww.wealthmakers.com'


    def _get_headers(self, headers):
        return headers if headers else {'Host': str(self.site.domain),
                                        'HTTP_X_REAL_IP': '98.231.77.218', # a real PV ip addr.
                                        'X-Real-Ip': '98.231.77.218'
                                        }


    def get_customer(self, username=TEST_CUSTOMER_EMAIL):
        custs = Customer.find_all_by_email(username)
        assert custs is not None and len(custs) > 0
        return custs[0]


    def login_customer(self, username=TEST_CUSTOMER_EMAIL, password=TEST_CUSTOMER_PASSWORD):
        # this sets the site it.
        self.post('/crm/customer_login',
                  {'username' : username, 'password' : password})
        assert self.site
        os.environ['enterprise_id'] = str(self.site.company.enterprise_id)


    def logout_customer(self):
        return self.logout_crm()


    def login_crm(self, username=UID, password=PWD):
        # this sets the site it.
        self.get('/crm')

        # this logs us into that site.
        self.post('/crm/login', {'username': username,
                                 'password': password})
        assert self.site
        os.environ['enterprise_id'] = str(self.site.company.enterprise_id)

        user = Users.authenticate(username, password)
        #user = Users.load(username)
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
        return resp


    def post(self, url, params=None, headers=None):
        if params == None:
            params = {}
        resp = self.app.post(url, params=params, headers=self._get_headers(headers))
        if resp.status_int in [302, 301]:
            resp = resp.follow()
        return resp


    def commit(self):
        transaction.commit()

    def get_prods(self):
        ent = Enterprise.find_all()[0]
        prods = Product.find_all(ent.enterprise_id)
        assert len(prods) > 0
        return prods


    def get_prod(self, idx=0):
        return self.get_prods()[idx]



def customer_logged_in(func, username=TEST_CUSTOMER_EMAIL, password=TEST_CUSTOMER_PASSWORD):
    def wrap(self):
        self.login_customer(username, password)
        ret = func(self)
        self.logout_customer()
        return ret
    wrap.__name__ = func.__name__
    return wrap


def secure_as_root(func, username=PVS_ROOT_UID, password=PVS_ROOT_PWD):
    def wrap(self):
        self.login_crm(username, password)
        ret = func(self)
        self.logout_crm()
        return ret
    wrap.__name__ = func.__name__
    return wrap


def secure(func, username=UID, password=PWD):
    def wrap(self):
        self.login_crm(username, password)
        ret = func(self)
        self.logout_crm()
        return ret
    wrap.__name__ = func.__name__
    return wrap


class alternate_site(object):    #pylint: disable-msg=R0903
    """ KB: [2012-11-29]: If in a test method you want to use a site that is configured other than "healthyustore.net"
    @alternate_site('test2.com')
    def test_whatever(self):
        :::
    """
    def __init__(self, domain):
        self.domain = domain

    def __call__(self, original_func):
        def wrap(func_self, *args, **kwargs):
            orig_site = func_self.site
            func_self.site = Site.find_by_host(self.domain)
            try:
                return original_func(func_self, *args, **kwargs)
            finally:
                func_self.site = orig_site

        wrap.__name__ = original_func.__name__
        return wrap



# def quiet(func):
#     def wrap(self):
#         self.quiet()
#         ret = func(self)
#         self.unquiet()
#         return ret
#     wrap.__name__ = func.__name__
#     return wrap
