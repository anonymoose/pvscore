#import pdb
import logging
import math
import datetime
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import IsLoggedIn
from app.model.crm.report import Report
from app.model.core.users import Users
from app.model.crm.company import Company
from app.model.crm.campaign import Campaign
from app.model.crm.product import Product
from app.model.crm.purchase import Vendor
import app.lib.util as util
import app.lib.db as db
import simplejson as json

log = logging.getLogger(__name__)

class ReportController(BaseController):

    @view_config(route_name='crm.report.edit', renderer='/crm/report.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name='crm.report.new', renderer='/crm/report.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self.edit()


    def _edit_impl(self):
        report_id = self.request.matchdict.get('report_id')
        report = None
        if report_id:
            report = Report.load(report_id)
            self.forbid_if(not report)
        else:
            report = Report()
        return {
            'report' : report,
            'reports' : Report.find_all(self.request.ctx.user.is_vendor_user()),
            'companies' : util.select_list(Company.find_all_all(), 'company_id', 'name')
            }


    def _show_prep(self, report_id):
        report = Report.load(report_id)
        campaigns = products = companies = users = vendors = None
        if report.show_campaign_id:
            campaigns = util.select_list(Campaign.find_all(self.enterprise_id), 'campaign_id', 'name', True)

        if report.show_vendor_id:
            vendors = util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name', True)

        if report.show_company_id:
            companies = util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name', True)

        if report.show_user_id:
            users = util.select_list(Users.find_all(self.enterprise_id), 'username', 'username', True)

        if report.show_product_id:
            products = util.select_list(Product.find_all(self.enterprise_id), 'product_id', 'name', True)

        return {
            'today' : util.today_date(),
            'thirty_ago' : util.today_date() - datetime.timedelta(days=30),
            'rpt_end_dt' : self.request.GET.get('rpt_end_dt'),
            'rpt_start_dt' : self.request.GET.get('rpt_start_dt'),
            'enterprise_id' : self.enterprise_id,
            'report' : report,
            'campaigns' : campaigns,
            'products' : products,
            'companies' : companies,
            'users' : users,
            'vendors' : vendors
            }

    
    @view_config(route_name='crm.report.show', renderer='/crm/report.show.mako')
    @authorize(IsLoggedIn())
    def show(self):
        return self._show_prep(self.request.matchdict.get('report_id'))


    @view_config(route_name='crm.report.list', renderer='/crm/report.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'reports' :Report.find_all(self.request.ctx.user.is_vendor_user())}


    @view_config(route_name='crm.report.save', renderer='/crm/report.edit.mako')
    @authorize(IsLoggedIn())
    def save(self):
        rep = Report.load(self.request.POST.get('report_id'))
        if not rep:
            rep = Report()
        rep.bind(self.request.POST, True)
        rep.save()
        rep.flush()
        return HTTPFound('/crm/report/edit/%s' % rep.report_id)


    @view_config(route_name='crm.report.results', renderer='string')
    @authorize(IsLoggedIn())
    def results(self):
        report_id = self.request.matchdict.get('report_id')
        rep = Report.load(report_id)
        page = self.request.GET.get('page', 1)
        limit = self.request.GET.get('rows', 100) # get how many rows we want to have into the grid
        sidx = self.request.GET.get('sidx', None)  # get index row - i.e. user click to sort
        sord = self.request.GET.get('sord', 'asc')  # get the direction

        rpt_start_dt = self.request.GET.get('rpt_start_dt') if self.request.GET.get('rpt_start_dt') else util.str_today()
        rpt_end_dt = self.request.GET.get('rpt_end_dt') if self.request.GET.get('rpt_end_dt') else util.str_today()
        rpt_campaign_id = self.request.GET.get('rpt_campaign_id') if 'rpt_campaign_id' in self.request.GET else ''
        rpt_company_id = self.request.GET.get('rpt_company_id') if 'rpt_company_id' in self.request.GET else ''
        rpt_user_id = self.request.GET.get('rpt_user_id') if 'rpt_user_id' in self.request.GET else ''
        rpt_product_id = self.request.GET.get('rpt_product_id') if 'rpt_product_id' in self.request.GET else ''
        rpt_vendor_id = self.request.GET.get('rpt_vendor_id') if 'rpt_vendor_id' in self.request.GET else ''
        rpt_p0 = self.request.GET.get('rpt_p0') if 'rpt_p0' in self.request.GET else ''
        rpt_p1 = self.request.GET.get('rpt_p1') if 'rpt_p1' in self.request.GET else ''
        rpt_p2 = self.request.GET.get('rpt_p2') if 'rpt_p2' in self.request.GET else ''

        sql = rep.sql.format(enterprise_id=self.enterprise_id,
                             vendor_id=self.request.ctx.user.vendor_id,
                             rpt_start_dt=rpt_start_dt,
                             rpt_end_dt=rpt_end_dt,
                             rpt_campaign_id=rpt_campaign_id,
                             rpt_company_id=rpt_company_id,
                             rpt_user_id=rpt_user_id,
                             rpt_product_id=rpt_product_id,
                             rpt_vendor_id=rpt_vendor_id,
                             rpt_p0=rpt_p0,
                             rpt_p1=rpt_p1,
                             rpt_p2=rpt_p2)

        count = db.get_value('select count(0) from (%s) x' % sql)
        total_pages = 0
        if count > 0:
            total_pages = math.ceil(int(count)/int(limit))
            total_pages = total_pages if total_pages > 1 else 1

        if int(page) > int(total_pages):
            page = total_pages

        start = int(limit)*int(page)-int(limit)  # // do not put $limit*($page - 1)
        if not limit:
            limit = 'all'
        if start < 0:
            start = 0
        results = db.get_list(sql +
                              (' ORDER BY %s %s ' % (sidx, sord) if sidx else '') +
                              ' LIMIT {limit} offset {start}'.format(limit=limit,
                                                                     start=start))
        response = {
            'page': page,
            'total': int(total_pages),
            'records': int(count)}

        rows = []
        for res_row in results:
            rows.append({'id': str(res_row[0]),
                         'cell': list([unicode(util.nvl(i)) for i in res_row])})

        response['rows'] = rows
        return json.dumps(response)


    @view_config(route_name='crm.report.export', renderer='/crm/report.export.mako')
    @authorize(IsLoggedIn())
    def results_export(self):
        report_id = self.request.matchdict.get('report_id')
        rep = Report.load(report_id)
        enterprise_id = self.enterprise_id
        sidx = self.request.GET.get('sidx')  # get index row - i.e. user click to sort
        sord = self.request.GET.get('sord')  # get the direction

        rpt_start_dt = self.request.GET.get('rpt_start_dt') if self.request.GET.get('rpt_start_dt') else util.str_today()
        rpt_end_dt = self.request.GET.get('rpt_end_dt') if self.request.GET.get('rpt_end_dt') else util.str_today()
        rpt_campaign_id = self.request.GET.get('rpt_campaign_id') if 'rpt_campaign_id' in self.request.GET else ''
        rpt_company_id = self.request.GET.get('rpt_company_id') if 'rpt_company_id' in self.request.GET else ''
        rpt_user_id = self.request.GET.get('rpt_user_id') if 'rpt_user_id' in self.request.GET else ''
        rpt_product_id = self.request.GET.get('rpt_product_id') if 'rpt_product_id' in self.request.GET else ''
        rpt_vendor_id = self.request.GET.get('rpt_vendor_id') if 'rpt_vendor_id' in self.request.GET else ''
        rpt_p0 = self.request.GET.get('rpt_p0') if 'rpt_p0' in self.request.GET else ''
        rpt_p1 = self.request.GET.get('rpt_p1') if 'rpt_p1' in self.request.GET else ''
        rpt_p2 = self.request.GET.get('rpt_p2') if 'rpt_p2' in self.request.GET else ''

        sql = rep.sql.format(enterprise_id=enterprise_id,
                             vendor_id=self.request.ctx.user.vendor_id,
                             rpt_start_dt=rpt_start_dt,
                             rpt_end_dt=rpt_end_dt,
                             rpt_campaign_id=rpt_campaign_id,
                             rpt_company_id=rpt_company_id,
                             rpt_user_id=rpt_user_id,
                             rpt_product_id=rpt_product_id,
                             rpt_vendor_id=rpt_vendor_id,
                             rpt_p0=rpt_p0,
                             rpt_p1=rpt_p1,
                             rpt_p2=rpt_p2)
        
        results = db.get_list(sql + (' ORDER BY %s %s ' % (sidx, sord) if sidx else ''))

        self.request.response.content_type = 'application/vnd.ms-excel'
        self.request.response.headers['Content-Disposition'] = 'attachment; filename="report.xls"'

        return {
            'rows' : results,
            'columns' : json.loads(rep.column_names)
            }


