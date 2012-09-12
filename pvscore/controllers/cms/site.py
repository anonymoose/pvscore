import logging, os
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.model.cms.site import Site
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.company import Company
from pvscore.model.crm.campaign import Campaign
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class SiteController(BaseController):

    @view_config(route_name='cms.site.edit', renderer='/cms/site.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name="cms.site.new", renderer='/cms/site.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        site_id = self.request.matchdict.get('site_id')
        if site_id:
            site = Site.load(site_id)
            self.forbid_if(not site or str(site.company.enterprise_id) != str(self.enterprise_id))
            site_config = self._check_config(site)
        else:
            site = Site()
            site_config = None
        return {
            'site' : site,
            'site_config' : site_config,
            'shipping_methods' : Site.get_shipping_methods(),
            'tax_methods' : Site.get_tax_methods(),
            'companies' : util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name'),
            'campaigns' : util.select_list(Campaign.find_all(self.enterprise_id), 'campaign_id', 'name')
            }


    def _check_config(self, site):
        dirr = site.site_full_directory
        return (os.path.exists(dirr) and os.path.exists(dirr + '/site.config'))


    @view_config(route_name='cms.site.list', renderer='/cms/site.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {
            'sites' : Site.find_all(self.enterprise_id)
            }


    @view_config(route_name='cms.site.save')
    @authorize(IsLoggedIn())
    def save(self):
        site = Site.load(self.request.POST.get('site_id'))
        if not site:
            site = Site()
            site.user_created = self.request.ctx.user.username
        else:
            self.forbid_if(site.company.enterprise_id != self.enterprise_id)
        site.bind(self.request.POST, True)
        site.save()
        site.flush()
        if not os.path.isdir(site.site_full_directory):
            site.create_dir_structure()
        self.flash('Successfully saved %s.' % (site.domain))
        return HTTPFound('/cms/site/edit/%s' % site.site_id)


    def show_page(self, pid):
        return self.render(self.siteutil.show_page(pid))


    def show_dynamic_page(self, root, mako):
        return self.render(self.siteutil.show_dynamic_page(root, mako))


    def show_css(self, template_id, css):
        return self.render(self.siteutil.show_css(template_id, css))


    def show_root(self):
        return self.render(self.siteutil.show_root())




def dynamic_url_lookup(request):
    return Response('Hello world!')
