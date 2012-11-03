from pvscore.tests import TestController, UID, PWD
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
        R = self.post('/crm/customer_login', {'username': 'amers_j@yahoo.com', 'password': 'geology'})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.app.reset()

    def test_customer_login_redirect(self):
        R = self.post('/crm/customer_login',
                      {'username': 'amers_j@yahoo.com',
                       'password': 'geology',
                       'redir' : '/'})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.app.reset()


    def test_customer_login_invalid(self):
        R = self.post('/crm/customer_login', {'username': 'amers_j@yahoo.com', 'password': 'bogus'})
        assert R.status_int == 200
        R.mustcontain('this is the index')
        self.assertEqual(R.request.path, '/')
        self.app.reset()


    # @secure
    # def test_logout(self):
    #     try:
    #         self.post('/crm/logout')
    #     except Exception as exc:
    #         log.debug(exc)

        


