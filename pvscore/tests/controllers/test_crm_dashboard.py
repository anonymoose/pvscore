from pvscore.tests import TestController, secure

# bin/T pvscore.tests.controllers.test_crm_dashboard

class TestCrmDashboard(TestController):

    @secure
    def test_dashboard(self):
        self.login_crm()
        R = self.get('/crm/dashboard')
        assert R.status_int == 200
        R.mustcontain('Dashboard')




