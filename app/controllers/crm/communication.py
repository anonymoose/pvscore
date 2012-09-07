#import pdb
import logging
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import IsLoggedIn
from app.model.crm.comm import Communication
from app.model.crm.company import Company
from app.model.crm.customer import Customer
from app.model.crm.customerorder import CustomerOrder
import app.lib.util as util

log = logging.getLogger(__name__)

class CommunicationController(BaseController):
    
    @view_config(route_name='crm.communication.edit', renderer='/crm/communication.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name='crm.communication.new', renderer='/crm/communication.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self.edit()


    def _edit_impl(self):
        comm_id = self.request.matchdict.get('comm_id')
        comm = None
        if comm_id:
            comm = Communication.load(comm_id)
            self.forbid_if(not comm or comm.enterprise_id != self.enterprise_id)
        else:
            comm = Communication()
        return {
            'comm_types' : Communication.get_types(),
            'comm_tokens' :  Communication.get_tokens(),
            'companies' : util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name', True),
            'comm' : comm
            }


    @view_config(route_name='crm.communication.list', renderer='/crm/communication.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'comms' : Communication.find_all(self.enterprise_id)}

    
    @view_config(route_name='crm.communication.view_comm_dialog', renderer='/crm/passthru.mako')
    @authorize(IsLoggedIn())
    def view_comm_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        comm_id = self.request.matchdict.get('comm_id')
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        comm = Communication.load(comm_id)
        self.forbid_if(not comm or comm.enterprise_id != self.enterprise_id)
        order = None
        if self.request.GET.get('order_id'):
            order = CustomerOrder.load(self.request.GET.get('order_id'))
            self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)

        return { 'content' : comm.render(cust, order, self.request.POST.get('msg')) }



    @view_config(route_name='crm.communication.send_comm_dialog', renderer='/crm/communication.send.mako')
    @authorize(IsLoggedIn())
    def send_comm_dialog(self):
        customer_id = self.request.GET.get('customer_id')
        cust = None
        if customer_id:
            cust = Customer.load(customer_id)
            self.forbid_if(cust.campaign.company.enterprise_id != self.enterprise_id)
            comms = Communication.find_all_by_company(cust.campaign.company, True)
        else:
            comms = Communication.find_all(self.enterprise_id, True)
        return {
            'comms' : util.select_list(comms, 'comm_id', 'name'),
            'cust' : cust
            }


    # @view_config(route_name='crm.communication.send_customer_comm', renderer='string')
    # @authorize(IsLoggedIn())
    # def send_customer_comm(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     comm_id = self.request.matchdict.get('comm_id')
    #     cust = Customer.load(customer_id)
    #     self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
    #     comm = Communication.load(comm_id)
    #     self.forbid_if(not comm or comm.enterprise_id != BaseController.get_enterprise_id())

    #     if cust.campaign != None:
    #         sender = cust.campaign.company
    #     else:
    #         sender = Users.load(session['user_id'])

    #     if comm.send_to_customer(sender, cust, None, self.request.POST.get('msg')):
    #         return 'True'
    #     else:
    #         return 'Unable to send email to %s' % cust.email

    @view_config(route_name='crm.communication.save', renderer='/crm/communication.edit.mako')
    @authorize(IsLoggedIn())
    def save(self):
        comm = Communication.load(self.request.POST.get('comm_id'))
        if not comm:
            comm = Communication()
            comm.enterprise_id = self.enterprise_id
        else:
            self.forbid_if(comm.enterprise_id != self.enterprise_id)

        comm.bind(self.request.POST, True)
        comm.save()
        comm.flush()
        self.flash('Successfully saved %s.' % comm.name)
        return HTTPFound('/crm/communication/edit/%s' % comm.comm_id)


    # def search(self):
    #     c.companies = util.select_list(Company.find_all(), 'company_id', 'name')
    #     c.name = request.POST.get('name')
    #     c.company_id = request.POST.get('company_id')
    #     c.comms = Communication.search(c.name, c.company_id)
    #     return self.render('/crm/communication.search.mako')

