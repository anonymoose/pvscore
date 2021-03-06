from pvscore.tests import TestController, UID, PWD, TEST_CUSTOMER_EMAIL, TEST_CUSTOMER_PASSWORD
from pvscore.model.crm.customer import Customer
import logging

log = logging.getLogger(__name__)

# nosetests pvscore.tests.controllers.test_crm_login

class TestCrmLogin(TestController):

    def test_index(self):
        R = self.get('/crm')
        assert R.status_int == 200
        R.mustcontain('CRM Login')
        self.app.reset()


    def test_login_empty(self):
        R = self.post('/crm/login')
        assert R.status_int == 200
        R.mustcontain('Invalid User or Password')
        self.app.reset()


    def test_valid(self):
        R = self.post('/crm/login', {'username': UID, 'password': PWD})
        assert R.status_int == 200
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
        assert R.status_int == 200
        R.mustcontain('Dashboard')
        self.app.reset()


    def test_goto_path_vars(self):
        R = self.post('/crm/login', {'username': UID, 'password': PWD,
                                     'path': '/crm/dashboard', 'vars': 'a=b'})
        assert R.status_int == 200
        R.mustcontain('Dashboard')
        self.app.reset()


    def test_customer_login(self):
        R = self.post('/crm/customer_login', {'username': TEST_CUSTOMER_EMAIL, 'password': TEST_CUSTOMER_PASSWORD})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.app.reset()

    def test_customer_login_redirect(self):
        R = self.post('/crm/customer_login',
                      {'username': TEST_CUSTOMER_EMAIL,
                       'password': TEST_CUSTOMER_PASSWORD,
                       'redir' : '/'})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.app.reset()


    def test_customer_login_invalid(self):
        R = self.post('/crm/customer_login', {'username': TEST_CUSTOMER_EMAIL, 'password': 'bogus'})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.assertEqual(R.request.path, '/')
        self.app.reset()


    def test_customer_forgot_password_invalid_username(self):  #pylint: disable-msg=C0103
        R = self.post('/crm/customer_forgot_password',
                      {'username': 'bogus@bogus.com'})
        assert R.status_int == 200
        assert "Your new password has been sent" not in R.body


    def test_customer_forgot_password(self):
        R = self.post('/crm/customer_forgot_password',
                      {'username': TEST_CUSTOMER_EMAIL})
        assert R.status_int == 200
        assert "Your new password has been sent" in R.body
        custs = Customer.find_all_by_email(TEST_CUSTOMER_EMAIL)
        assert len(custs) > 0
        cust = custs[0]
        assert cust.password != TEST_CUSTOMER_PASSWORD
        cust.password = TEST_CUSTOMER_PASSWORD
        cust.save()
        self.commit()


    # @secure
    # def test_logout(self):
    #     try:
    #         self.post('/crm/logout')
    #     except Exception as exc:
    #         log.debug(exc)




