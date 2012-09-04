from app.tests import TestController, secure

# bin/T app.tests.controllers.test_crm_dashboard

class TestCrmDashboard(TestController):

    @secure
    def test_dashboard(self):
        self.login_crm()
        R = self.get('/crm/dashboard')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Dashboard')




