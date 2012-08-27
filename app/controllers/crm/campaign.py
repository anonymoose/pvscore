import pdb
import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.controllers.base import BaseController
from app.lib.validate import validate
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn
from app.model.crm.campaign import Campaign
from app.model.crm.comm import Communication
from app.model.crm.company import Company
import app.lib.util as util

log = logging.getLogger(__name__)

class CampaignController(BaseController):
    
    @view_config(route_name="crm.campaign.edit", renderer='/crm/campaign.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()

    
    @view_config(route_name="crm.campaign.new", renderer='/crm/campaign.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        campaign_id = self.request.matchdict.get('campaign_id')
        comms = []
        companies = util.select_list(Company.find_all(self.enterprise_id),
                                       'company_id', 'name')
        campaign = None
        if campaign_id:
            campaign = Campaign.load(campaign_id)
            self.forbid_if(not campaign or campaign.company.enterprise_id != self.enterprise_id)
            comms = util.select_list(Communication.find_all_by_company(campaign.company), 'comm_id', 'name', True)
        else:
            campaign = Campaign()

        return {'comms': comms,
                'campaign': campaign,
                'companies': companies}


    @view_config(route_name="crm.campaign.list", renderer='/crm/campaign.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'campaigns' : Campaign.find_all(self.enterprise_id)}


    @view_config(route_name="crm.campaign.search", renderer="string") # KB: [2012-08-13]: If we ever really need this, change the renderer """
    @authorize(IsLoggedIn())
    def search(self):
        name = self.request.POST.get('name')
        company_id = self.request.POST.get('company_id')
        return {
            'companies' : util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name'),
            'name' : name,
            'company_id' : company_id,
            'campaigns' : Campaign.search(self.enterprise_id, name, company_id)
        }


    @view_config(route_name="crm.campaign.save")
    @authorize(IsLoggedIn())
    def save(self):
        cmpn = Campaign.load(self.request.POST.get('campaign_id'))
        if not cmpn:
            cmpn = Campaign()
        else:
            self.forbid_if(cmpn.company.enterprise_id != self.enterprise_id)
        cmpn.bind(self.request.POST)
        cmpn.save()

        cmpn.clear_attributes()
        for i in range(10):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                cmpn.set_attr(attr_name, attr_value)

        self.request.session.flash('Successfully saved %s.' % cmpn.name)
        return HTTPFound('/crm/campaign/edit/%s' % cmpn.campaign_id)

