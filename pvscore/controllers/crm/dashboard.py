#import pdb
import logging
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pyramid.view import view_config
from pvscore.controllers.base import BaseController
from pvscore.model.crm.company import Company
from pvscore.model.crm.customerorder import PeriodOrderSummary, MTDSalesByVendor
#from pvscore.model.crm.customer import PeriodCustomerCountSummary
from pvscore.model.crm.appointment import Appointment

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def _prep(self):
        charts = []
        # basic included snapshot reports.
        if self.request.ctx.user.priv.view_report:
            charts.append(PeriodOrderSummary(self.request))
            charts.append(MTDSalesByVendor(self.request))
            #charts.append(PeriodCustomerCountSummary(self.request))

        return {
            'companies': Company.find_all(self.request.ctx.enterprise.enterprise_id),
            'charts' : charts,
            'appointments' : Appointment.find_by_user(self.request.ctx.user)[:10]
            }

    @view_config(route_name="crm.dashboard", renderer="/crm/dashboard.mako")
    @authorize(IsLoggedIn())
    def dashboard(self):
        return self._prep()


