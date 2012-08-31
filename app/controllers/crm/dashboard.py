#import pdb
import logging
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import IsLoggedIn
from pyramid.view import view_config
from app.controllers.base import BaseController
from app.model.crm.company import Company
from app.model.crm.customerorder import PeriodOrderSummary, MTDSalesByVendor
from app.model.crm.customer import PeriodCustomerCountSummary

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def _prep(self):
        charts = []
        # basic included snapshot reports.
        if self.request.ctx.user.priv.view_report:
            charts.append(PeriodOrderSummary(self.request))
            charts.append(MTDSalesByVendor(self.request))
            charts.append(PeriodCustomerCountSummary(self.request))

        return {'companies': Company.find_all(self.request.ctx.enterprise.enterprise_id),
                'charts' : charts}

    @view_config(route_name="crm.dashboard", renderer="/crm/dashboard.mako")
    @authorize(IsLoggedIn())
    def dashboard(self):
        return self._prep()
             

