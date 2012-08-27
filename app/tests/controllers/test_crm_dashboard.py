import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
from app.model.crm.product import Product, ProductCategory
from app.model.crm.customer import Customer
import simplejson as json
from app.controllers.crm.dashboard import DashboardController

# nosetests app.tests.controllers.test_crm_dashboard

class TestCrmDashboard(TestController):

    def test_dashboard(self):
        self.login_crm()
        R = self.get('/crm/dashboard')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Dashboard')




