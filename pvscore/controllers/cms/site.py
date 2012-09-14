import logging, os
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.renderers import render
from mako.exceptions import TopLevelLookupException
from pvscore.controllers.base import BaseController
from pvscore.model.cms.site import Site
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.company import Company
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.customer import Customer
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


def _load_customer(request):
    """ KB: [2012-09-12]: Get the customer_id from the various places it
    may be stashed.  session first."""
    customer_id = None
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
    elif 'customer_id' in request.POST:
        customer_id = request.POST.get('customer_id')
    elif 'customer_id' in request.GET:
        customer_id = request.GET.get('customer_id')
    customer = Customer.load(customer_id)
    if customer_id:
        if not customer or customer.campaign.company.enterprise_id != request.ctx.enterprise.enterprise_id:
            raise HTTPForbidden()
    return customer
    

def dynamic_url_lookup(request):
    """ KB: [2012-09-12]: This will render dynamic content.
    http://stackoverflow.com/questions/6321625/pyramid-is-it-possible-to-render-my-mako-template-as-a-string-within-my-view-c
    /fud/a/b                 -->  /${site.namespace}/fud.mako
                                    request.GET['param0'] = 'a'
                                    request.GET['param1'] = 'b'
    /derf.fud/a/b            -->  /${site.namespace}/derf/fud.mako   <--    note the dot in the first part
                                    request.GET['param0'] = 'a'
                                    request.GET['param1'] = 'b'
    /  ("")                  -->  /${site.namespace}/index.mako
    """
    try:
        parts = request.path.split('/')
        mako_path_parts = parts[1].split('-')

        filepath = None
        if len(mako_path_parts) == 1:
            # this is single path rooted in the namespace
            filepath = '/%s' % (mako_path_parts[0] if mako_path_parts[0] != '' else 'index')
        elif len(mako_path_parts) > 1:
            # this is a file in a subdir of the namespace
            filepath = "/".join(mako_path_parts)

        matchdict = {}
        if len(parts) > 2:
            for i, param in enumerate(parts[2:]):
                matchdict['param%s' % i] = param

        path = "/%s/%s.mako" % (request.ctx.site.namespace, filepath)
        return Response(render(path,
                               {'site' : request.ctx.site,
                                'user' : request.ctx.user,
                                'campaign' : request.ctx.campaign,
                                'customer' : _load_customer(request),
                                'matchdict' : matchdict},                                
                               request))
    except TopLevelLookupException as exc:
        log.error(exc)
        return HTTPNotFound()





