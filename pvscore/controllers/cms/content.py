import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.model.cms.content import Content
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.company import Company
from pvscore.model.crm.campaign import Campaign
from pvscore.model.cms.site import Site
import pvscore.lib.util as util

log = logging.getLogger(__name__)


class ContentController(BaseController):

    @view_config(route_name='cms.content.edit', renderer='/cms/content.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name="cms.content.new", renderer='/cms/content.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        site_id = self.request.matchdict.get('site_id')
        site = Site.load(site_id)
        self.forbid_if(not site or str(site.company.enterprise_id) != str(self.enterprise_id))
        content_id = self.request.matchdict.get('content_id')
        if content_id:
            content = Content.load(content_id)
            self.forbid_if(not content
                           or str(content.site.company.enterprise_id) != str(self.enterprise_id)
                           or str(content.site_id) != str(site_id))
        else:
            content = Content()
            content.site_id = site_id
        return {
            'site' : site,
            'content' : content,
            'companies' : util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name'),
            'campaigns' : util.select_list(Campaign.find_all(self.enterprise_id), 'campaign_id', 'name')
            }


    @view_config(route_name='cms.content.list', renderer='/cms/content.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        site = Site.load(self.request.matchdict.get('site_id'))
        self.forbid_if(not site or str(site.company.enterprise_id) != str(self.enterprise_id))
        return {
            'site' : site,
            'contents' : Content.find_by_site(site)
            }


    @view_config(route_name='cms.content.save')
    @authorize(IsLoggedIn())
    def save(self):
        content = Content.load(self.request.POST.get('content_id'))
        if not content:
            content = Content()
            content.user_created = self.request.ctx.user.user_id
        else:
            self.forbid_if(content.site.company.enterprise_id != self.enterprise_id)
        content.bind(self.request.POST, True)
        content.save()
        content.flush()
        content.invalidate_caches()
        self.flash('Successfully saved %s.' % (content.content_id))
        return HTTPFound('/cms/content/edit/%s/%s' % (content.site_id, content.content_id))


    @view_config(route_name='cms.content.robots_txt', renderer='string')
    def robots_txt(self):
        self.request.response.content_type = 'text/plain'
        return self.request.ctx.site.robots_txt


