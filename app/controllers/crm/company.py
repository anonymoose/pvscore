#import pdb
import logging, os
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.controllers.base import BaseController
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import IsLoggedIn
from app.model.crm.campaign import Campaign
from app.model.crm.company import Company, Enterprise
from app.model.core.users import Users
from app.model.cms.site import Site
import app.lib.util as util
from app.model.crm.comm import Communication

log = logging.getLogger(__name__)

class CompanyController(BaseController):

    @view_config(route_name="crm.company.edit", renderer='/crm/company.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name="crm.company.new", renderer='/crm/company.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        company_id = self.request.matchdict.get('company_id')
        comms = []
        campaigns = util.select_list(Campaign.find_all(self.enterprise_id), 'campaign_id', 'name')
        company = None
        if company_id:
            company = Company.load(company_id)
            comms = util.select_list(Communication.find_all_by_company(company), 'comm_id', 'name')
        else:
            company = Company()
        return {'comms': comms,
                'company': company,
                'campaigns': campaigns}
    
    
    @view_config(route_name="crm.company.search", renderer='string') 
    @authorize(IsLoggedIn())
    def search(self):
        name = self.request.POST.get('name')
        return {'name' : name,
                'companies' :Company.search(name)}


    @view_config(route_name="crm.company.list", renderer='/crm/company.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'companies' : Company.find_all(self.enterprise_id)}


    @view_config(route_name="crm.company.save")
    @authorize(IsLoggedIn())
    def save(self):
        comp = Company.load(self.request.POST.get('company_id'))
        if not comp:
            comp = Company()
        comp.bind(self.request.POST)
        comp.save()
        comp.flush()

        if not os.path.isdir(comp.web_full_directory):
            comp.create_dir_structure()

        comp.clear_attributes()
        for i in range(10):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                comp.set_attr(attr_name, attr_value)

        self.request.session.flash('Successfully saved %s.' % comp.name)
        return HTTPFound('/crm/company/edit/%d' % int(comp.company_id))


    @view_config(route_name="crm.company.enterprise.quickstart", renderer="/crm/company.quick_start.mako")
    @authorize(IsLoggedIn())
    def quickstart(self):
        return {
            'enterprise' : None,
            'company' : None,
            'campaign' : None,
            'user' : None,
            'site' : None,
            'done' : False
            }


    @view_config(route_name="crm.company.enterprise.provision", renderer="/crm/company.quick_start.mako")
    @authorize(IsLoggedIn())
    def provision(self):
        uname = self.request.POST.get('u_username')
        if Users.is_unique_username(uname):
            ent = Enterprise()
            ent.bind(self.request.POST, True, 'ent')
            ent.save()
            ent.flush()

            comp = Company()
            comp.bind(self.request.POST, True, 'cmp')
            comp.enterprise_id = ent.enterprise_id
            comp.save()
            comp.flush()

            campaign = Campaign()
            campaign.name = comp.name + ' Default'
            campaign.company_id = comp.company_id
            campaign.save()
            campaign.flush()

            comp.default_campaign_id = campaign.campaign_id
            comp.save()
            comp.flush()

            user = Users()
            user.bind(self.request.POST, True, 'u')
            user.password = Users.encode_password('password')
            user.enterprise_id = ent.enterprise_id
            user.allow_cms = True
            user.type = 'Admin'
            user.save()
            user.flush()

            site = Site()
            site.bind(self.request.POST, True, 'st')
            site.company = comp
            site.description = comp.name + ' Site'
            site.creator = user
            #site.template = Template.find_by_name('default')
            site.save()
            site.flush()

            site.create_dir_structure()

            return {
                'enterprise' : ent,
                'company' : comp,
                'campaign' : campaign,
                'user' : user,
                'site' : site,
                'done' : True
                }


    @view_config(route_name='crm.company.enterprise.edit', renderer='/crm/company.edit_enterprise.mako')
    @authorize(IsLoggedIn())
    def edit_enterprise(self):
        return self._edit_enterprise_impl()
    

    @view_config(route_name='crm.company.enterprise.new', renderer='/crm/company.edit_enterprise.mako')
    @authorize(IsLoggedIn())
    def new_enterprise(self):
        return self._edit_enterprise_impl()


    def _edit_enterprise_impl(self):
        enterprise_id = self.request.matchdict.get('enterprise_id')
        the_enterprise = None
        if enterprise_id:
            the_enterprise = Enterprise.load(enterprise_id)
        else:
            the_enterprise = Enterprise()
        return {'the_enterprise': the_enterprise,
                'billing_methods' : Enterprise.get_billing_methods()}


    @view_config(route_name='crm.company.enterprise.list', renderer='/crm/company.list_enterprises.mako')
    @authorize(IsLoggedIn())
    def list_enterprises(self):
        return {'enterprises' : Enterprise.find_all()}


    @view_config(route_name='crm.company.enterprise.save')
    @authorize(IsLoggedIn())
    def save_enterprise(self):
        ent = Enterprise.load(self.request.POST.get('enterprise_id'))
        if not ent:
            ent = Enterprise()
        ent.bind(self.request.POST)
        ent.save()
        ent.flush()
        
        ent.clear_attributes()
        for i in range(10):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                ent.set_attr(attr_name, attr_value)

        self.request.session.flash('Successfully saved %s.' % ent.name)
        return HTTPFound('/crm/company/enterprise/edit/%d' % int(ent.enterprise_id))

    

    # KB: [2012-08-21]: When we are testing, the app has its own cache
    # and own redis.  When we delete something in the testing scaffolding,
    # it doesn't clear out the caches in the app context.  Call this
    # method after each test in tearDown to make sure you've got
    # everything.
    # Only add items here if they give you an issue in Tfull for full
    # regression testing. So dumb.
    @view_config(route_name='crm.company.enterprise.clearcache', renderer='string')
    @authorize(IsLoggedIn())
    def clear_caches(self):
        for camp in Campaign.find_all(self.enterprise_id):
            camp.invalidate_caches()
        return "ok"
