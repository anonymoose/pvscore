import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController

# nosetests app.tests.controllers.test_crm_login

class TestCrmLogin(TestController):

    def test_index(self):
        R = self.get('/crm')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('CRM Login')
        self.app.reset()

    def test_login_empty(self):
        R = self.post('/crm/login')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Invalid User or Password')
        self.app.reset()

    def test_valid(self):
        R = self.post('/crm/login', {'username': UID, 'password': PWD})
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Dashboard')
        self.app.reset()


    def test_catch_goto_path(self):
        R = self.get('/crm/dashboard')
        R.mustcontain('CRM Login')
        self.assertEqual(R.forms[0]['path'].value, '/crm/dashboard')
        self.assertEqual(R.forms[0]['vars'].value, '')
        self.app.reset()


    def test_catch_goto_path_vars(self):
        R = self.get('/crm/dashboard?a=b')
        R.mustcontain('CRM Login')
        self.assertEqual(R.forms[0]['path'].value, '/crm/dashboard')
        self.assertEqual(R.forms[0]['vars'].value, 'a=b')
        self.app.reset()


    def test_goto_path(self):
        R = self.post('/crm/login', {'username': UID, 'password': PWD,
                                     'path': '/crm/dashboard', 'vars': ''})
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Dashboard')
        self.app.reset()


    def test_goto_path_vars(self):
        R = self.post('/crm/login', {'username': UID, 'password': PWD,
                                     'path': '/crm/dashboard', 'vars': 'a=b'})
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Dashboard')
        self.app.reset()

        
    def test_logout(self):
        R = self.post('/crm/logout')
        

    # '/crm/customer/edit/{customer_id}',  action='edit'
    """
    @secure
    def test_crm_customer_login(self):
        try:
            cust = self._create_test_customer()
            R = self.post('/crm/customer_login',
                          {'username': TEST_UID,
                           'password': TEST_UID_PASSWORD})
            assert R.status_int == 200
            assert 'username' in R.session and R.session['username'] == TEST_UID
            assert 'customer_id' in R.session and R.session['customer_id'] == str(cust.customer_id)
            assert 'customer_logged_in' in R.session and R.session['customer_logged_in'] == True
            assert 'crm_logged_in' in R.session and R.session['crm_logged_in'] == False
        finally:
            self._delete_test_customer()
            """



