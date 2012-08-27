import pdb, os, transaction
from unittest import TestCase
from webtest import TestApp
from app.model.meta import Session
from app.model.core.users import Users
from decorator import decorator
import app.lib.util as util
import nose
from cStringIO import StringIO
import sys
from app.model.crm.comm import Communication
from app.model.crm.customer import Customer
from app.model.crm.company import Company
from app.model.crm.product import Product, InventoryJournal
from app.model.crm.journal import Journal
from app.model.cms.site import Site
#from app.lib.catalog import Catalog, Cart
import ConfigParser
import paste.deploy
from pyramid import testing

#__all__ = ['environ', 'url', 'TestController', 'secure', 'quiet']

# Invoke websetup with the current config file
os.environ['PVS_TESTING'] = 'TRUE'
#SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

environ = {}

UID = 'kenneth.bedwell@gmail.com'
PWD = 'Zachary234'
TEST_UID = 'test_kwbedwell@hotmail.com'
TEST_UID_PASSWORD = 'swordfish'
T_PRODUCT = 'Test Product for Nose'
SITEDOMAIN = 'healthyustore.net'

class TestController(TestCase):
    def setUp(self):
        from app import command_line_main
        settings = paste.deploy.appconfig('config:unittest.ini', relative_to='.')
        app = command_line_main(settings)
        from webtest import TestApp
        self.app = TestApp(app)
        self.site = Site.find_by_host(SITEDOMAIN)


    def tearDown(self):
        pass


    def quiet(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
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


    """ KB: [2011-09-02]: To send something back up the chain from deep in the app...
    util.local_cache_set('PVS_TEST', something_important)
    or
    util.test_set_var(something_important)
    """
    def get_message(self, key='PVS_TEST'):
        v = util.local_cache_get(key)
        util.local_cache_del(key)
        return v


    def login_crm(self, enterprise_id=None, username='kenneth.bedwell@gmail.com', password='Zachary234'):
        # this sets the site it.
        R = self.get('/crm')

        # this logs us into that site.
        R = self.post('/crm/login', {'username': username,
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
        except:
            pass
        self.app.reset()
        return True


    def get(self, url, params=None, headers=None):
        resp = self.app.get(url, params=params, headers=self._get_headers(headers))
        if resp.status_int in [302, 301]:
            resp = resp.follow()
            if resp.status_int in [302, 301]:
                resp = resp.follow()
        return resp


    def post(self, url, params={}, headers=None):
        resp = self.app.post(url, params=params, headers=self._get_headers(headers))
        if resp.status_int in [302, 301]:
            resp = resp.follow()
            if resp.status_int in [302, 301]:
                resp = resp.follow()
        return resp


    def commit(self):
        transaction.commit()


    def rollback(self):
        transaction.rollback()

    
    def _get_a_product(self, idx=0):
        l = Product.find_all_active(self.site.company)
        assert len(l) > 0
        return l[idx]


    def _create_test_product(self):
        com = self.site.company
        p = Product()
        p.name = T_PRODUCT
        p.company = com
        p.description = 'Description'
        p.detail_description = 'Description Description Description'
        p.manufacturer = 'Test Manufacturer'
        p.sku = 'SKUSKU'
        p.web_visible=True
        p.enabled = True
        p.save()
        p.commit()
        p.set_price(com.default_campaign, 111, 111)
        p.commit()
        return p


    def _delete_test_product(self):
        com = self.site.company
        p = Product.find_by_name(com.default_campaign, T_PRODUCT)
        assert p
        Product.full_delete(p.product_id)
        p = Product.find_by_name(com.default_campaign, T_PRODUCT)
        assert not p


    def _create_test_customer(self):
        com = self.site.company
        c = Customer()
        c.campaign = com.default_campaign
        c.fname = 'Test'
        c.lname = 'Tester'
        c.phone = '9047167487'
        c.addr1 = '123 Elm St.'
        c.company_name = 'Fud Factor'
        c.city = 'Ponte Vedra'
        c.state = 'FL'
        c.zip = '32082'
        c.country = 'USA'
        c.email = TEST_UID
        c.password = TEST_UID_PASSWORD
        c.save()
        c.commit()
        assert c.customer_id
        return c


    def _delete_test_customer(self):
        com = self.site.company
        cust = Customer.find(TEST_UID, com.default_campaign)
        Customer.full_delete(cust.customer_id, True)
        cust = Customer.find(TEST_UID, com.default_campaign)
        assert cust == None


    """
    def _create_order(self, cust):
        cmp = self.site.company.default_campaign
        ps = Product.find_all_active(self.site.company)
        assert ps and len(ps) > 2
        p0 = ps[0]
        price0 = cmp.get_product_price(p0)
        p1 = ps[1]
        price1 = cmp.get_product_price(p1)
        p2 = ps[2]

        c = Cart()
        c.add_item(p0, cmp.campaign_id)
        assert c.get_total() == price0
        assert c.get_product_total() == price0

        c.add_item(p1, cmp.campaign_id, 2)
        tot = (price0 + (price1*2))
        assert c.get_total() == tot
        assert c.get_product_total() == tot
        assert c.has_product_id(p0.product_id)
        assert c.has_product_id(p1.product_id)

        o = cust.add_order(c, None, self.site, cmp)
        assert o
        assert o.total_payments_due() == tot
        assert o.total_price() == tot
        assert o.total_shipping_price() == 0
        assert o.total_handling_price() == 0

        assert cust.has_purchased_product(p0)
        assert cust.has_purchased_product(p1)
        assert not cust.has_purchased_product(p2)

        o2 = cust.get_order(o.order_id)
        assert o2
        assert o2.order_id == o.order_id
        return o
    """


def secure(func, enterprise_id=None, username='kenneth.bedwell@gmail.com', password='Zachary234'):
    def wrap(self):
        self.login_crm(enterprise_id, username, password)
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
