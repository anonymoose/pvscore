from app.tests import TestController, UID, PWD

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
        try:
            self.post('/crm/logout')
        except Exception as exc:
            pass
        


