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
from pvscore.model.core.asset import Asset
import pvscore.lib.util as util
import importlib

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


    @view_config(route_name='cms.content.save_ajax', renderer="string")
    @authorize(IsLoggedIn())
    def save_ajax(self):
        """ KB: [2013-03-04]: Only save the content and maybe the name.  Useful via ajax from aloha """
        content = Content.load(self.request.POST.get('content_id'))
        if not content:
            content = Content()
            content.user_created = self.request.ctx.user.user_id
        else:
            self.forbid_if(content.site.company.enterprise_id != self.enterprise_id)
        content.bind(self.request.POST)
        content.save()
        content.flush()
        content.invalidate_caches()
        return 'True'


    @view_config(route_name='cms.content.save_dynamic_attribute', renderer='string')
    @authorize(IsLoggedIn())
    def save_dynamic_attribute(self):
        objtype = self.request.POST.get('objtype')
        pk_id = self.request.POST.get('pk_id')
        attr = self.request.POST.get('attr')
        data = self.request.POST.get('data')
        module_name = self.request.POST.get('module')
        self.forbid_if(not objtype or not pk_id or not attr)
        
        try:
            module = importlib.import_module(module_name)
            class_ = getattr(module, objtype)
            instance = class_.load(pk_id)
            self.forbid_if(not instance)
            setattr(instance, attr, data)
            instance.save()
            instance.flush()
            instance.invalidate_caches()
            return 'True'
        except Exception as exc:
            return False
    

    @view_config(route_name='cms.content.robots_txt', renderer='string')
    def robots_txt(self):
        """ KB: [2013-03-04]: This gets run when a crawler calls /robots.txt """
        self.request.response.content_type = 'text/plain'
        return self.request.ctx.site.robots_txt


    @view_config(route_name='cms.content.file.new', renderer='/cms/content.file.edit.mako')
    @authorize(IsLoggedIn())    
    def file_new(self):
        return self._file_edit_impl()


    @view_config(route_name='cms.content.file.edit', renderer='/cms/content.file.edit.mako')
    @authorize(IsLoggedIn())    
    def file_edit(self):
        return self._file_edit_impl()


    def _file_edit_impl(self):
        site = Site.load(self.request.matchdict.get('site_id'))
        self.forbid_if(site.company.enterprise_id != self.enterprise_id)
        asset_id = self.request.matchdict.get('asset_id')
        if asset_id:
            asset = Asset.load(asset_id)
            self.forbid_if(not asset
                           or str(asset.enterprise_id) != str(self.enterprise_id))
        else:
            asset = Asset()
        return {
            'site' : site,
            'asset' : asset
            }


    @view_config(route_name='cms.content.file.save')
    @authorize(IsLoggedIn())
    def file_save(self):
        site = Site.load(self.request.matchdict.get('site_id'))
        self.forbid_if(site.company.enterprise_id != self.enterprise_id)
        asset = Asset.create_new(site, self.enterprise_id, self.request)
        asset.bind(self.request.POST, True)
        asset.save()
        asset.flush()
        self.flash('Saved image %s' % asset.name)
        return HTTPFound('/cms/content/file/edit/%s/%s' % (site.site_id, asset.id))


    @view_config(route_name='cms.content.file.list', renderer='/cms/content.file.list.mako')
    @authorize(IsLoggedIn())    
    def file_list(self):
        site = Site.load(self.request.matchdict.get('site_id'))
        self.forbid_if(site.company.enterprise_id != self.enterprise_id)
        return {
            'contents' : Asset.find_for_object(site)
            }


    # @view_config(route_name='crm.product.delete_picture', renderer="string")
    # @authorize(IsLoggedIn())
    # def delete_picture(self):
    #     product_id = self.request.matchdict.get('product_id')
    #     product = Product.load(product_id)
    #     self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
    #     asset_id = self.request.matchdict.get('asset_id')
    #     asset = Asset.load(asset_id)
    #     self.forbid_if(asset.fk_type != 'Product' or str(asset.fk_id) != str(product.product_id))
    #     asset.delete()
    #     return 'True'
