import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.model.crm.customer import load_customer
from pyramid.response import Response
from pyramid.renderers import render
from pvscore.lib.cart import Cart
from pvscore.model.crm.product import Product, ProductCategory
from pvscore.model.crm.appointment import Appointment
import pvscore.lib.util as util
from pvscore.lib.smart.scatalog import SmartCatalog, SmartPricing, SmartSeo
from pvscore.model.cms.content import Content

log = logging.getLogger(__name__)

class CatalogBaseController(BaseController):

    def params(self):
        campaign = self.request.ctx.campaign
        site = self.request.ctx.site
        if not 'cart' in self.session:
            self.session['cart'] = Cart(site)
        cart = self.session['cart']
        events = Appointment.find_public(self.enterprise_id)
        return {'site' : site,
                'base' : '%s/%s/' % (self.request.host_url.replace('http', 'https') if util.is_production() else self.request.host_url , site.namespace),
                'user' : self.request.ctx.user,
                'product' : None,
                'products_related' : None,
                'category' : None,
                'cart' : cart,
                'events' : events,
                'seo_title' : site.seo_title,
                'seo_keywords' : site.seo_keywords,
                'seo_description' : site.seo_description,
                'campaign' : campaign,
                'categories' : SmartCatalog.category_list(campaign),
                'customer' : load_customer(self.request, True),  # this way customer is always there, just may be empty
                'matchdict' : self.request.matchdict,
                'back_link' : self.session.get('back_link'),
                'specials' : self.specials_product_list(self.request.GET.get('specials_category_id'), 0, 4),
                'recent_products' : self.session['recent_products'] if 'recent_products' in self.session else {}
                }


    def render(self, mako_file, params=None):
        site = self.request.ctx.site
        path = "/%s/%s.mako" % (site.namespace, mako_file)
        return Response(render(path,
                               params if params is not None else self.params(),
                               self.request))


    # def personal_product_list(self, customer):
    #     activeorders = customer.get_active_orders()
    #     products = {}
    #     for aorder in activeorders:
    #         for oitem in aorder.items:
    #             if not oitem.product.name in products:
    #                 products[oitem.product.name] = Product.load(oitem.product.product_id)
    #     return products.values()


    # def manufacturer_product_list(self, manufacturer_name, offset=None, limit=None):
    #     return util.page_list(Product.find_by_manufacturer(self.enterprise_id, manufacturer_name), offset, limit)


    def new_product_list(self, offset=None, limit=None):
        return SmartCatalog.new_product_list(self.request.ctx.campaign, offset, limit)


    def specials_product_list(self, specials_category_id, offset=None, limit=None):
        """ KB: [2012-12-24]: You can pass "specials_category_id=qwerqewfzdsxfdsfg" in the URL anywhere and the specials will show up as that category. """
        if specials_category_id:
            return SmartCatalog.category_product_list(self.request.ctx.campaign, specials_category_id, offset, limit)
        else:
            return SmartCatalog.specials_product_list(self.request.ctx.campaign, offset, limit)


    def featured_product_list(self, offset=None, limit=None):
        return SmartCatalog.featured_product_list(self.request.ctx.campaign, offset, limit)



class CatalogController(CatalogBaseController):

    @view_config(route_name='ecom.site.product')
    @view_config(route_name='ecom.site.product.named')
    @view_config(route_name='ecom.site.product.default')
    def product(self):
        product_id = self.request.matchdict.get('product_id')
        if not util.is_uuid(product_id):
            # it's not really a product ID, but a search string from a bot.
            raise HTTPFound('/ecom/search?search=%s' % product_id)
        prod = Product.load(product_id)
        self.redir_if(not prod or not prod.enabled or not prod.web_visible)
        
        page = self.request.matchdict.get('page', util.nvl(prod.render_template, 'product'))   # /product/{product_id}/{page}

        self.session['last_product_id'] = product_id
        self.session['back_link'] = '/product/%s' % product_id
        params = self.params()
        self._add_to_recent_products(prod)

        params['product'] = prod
        params['products_also_liked'] = SmartCatalog.also_liked_product_list(prod, params['campaign'])
        params['products_related'] = SmartCatalog.related_product_list(prod, params['campaign'])
        params['product_attributes'] = self._prep_product_attributes(prod.get_product_attributes())
        params['attrs'] = prod.get_attrs()
        params['price'] = SmartPricing.product_price(prod, params['campaign'])
        (params['seo_title'], params['seo_keywords'], params['seo_description']) = SmartSeo.product_seo(prod, self.request.ctx.site)
        return self.render(page, params)


    def _prep_product_attributes(self, product_attributes):
        attr_classes = list(set([pa.attr_class for pa in product_attributes]))
        ret = {}
        for acl in attr_classes:
            ret[acl] = [pa for pa in product_attributes if pa.attr_class == acl]
        return ret


    def _add_to_recent_products(self, prod):
        if not 'recent_products' in self.session:
            self.session['recent_products'] = {}
        self.session['recent_products'][prod.product_id] = prod.name


    @view_config(route_name='ecom.site.products')
    @view_config(route_name='ecom.site.products.default')
    def products(self):
        # /products/{subset}/{page}
        page = self.request.matchdict.get('page', 'products')
        subset = self.request.matchdict.get('subset')
        self.session['back_link'] = '/products/%s' % subset
        params = self.params()
        params['subset'] = subset
        params['products'] = {'new' : self.new_product_list,
                              'featured' : self.featured_product_list,
                              'specials' : self.specials_product_list
                              }.get(subset)(self.request.GET.get('offset'), self.request.GET.get('limit'))
        return self.render(page, params)


    @view_config(route_name='ecom.site.category.default')
    @view_config(route_name='ecom.site.category.named')
    @view_config(route_name='ecom.site.category')
    def category(self):
        # /category/{category_id}/{page}
        page = self.request.matchdict.get('page', 'category')
        category_id = util.to_uuid(self.request.matchdict.get('category_id'))
        category = ProductCategory.load(category_id)
        self.redir_if(not category)
        self.session['back_link'] = '/category/%s' % category_id
        params = self.params()
        params['products'] = util.page_list(SmartCatalog.category_product_list(self.request.ctx.campaign, category_id),
                                            self.request.GET.get('offset'), self.request.GET.get('limit'))
        params['category'] = category
        (params['seo_title'], params['seo_keywords'], params['seo_description']) = SmartSeo.category_seo(category, self.request.ctx.site)
        return self.render(page, params)


    @view_config(route_name='ecom.site.search.default')
    @view_config(route_name='ecom.site.search')
    def search(self):
        page = self.request.matchdict.get('page', 'search_results')
        params = self.params()
        params['subset'] = 'search'
        params['products'] = util.page_list(Product.catalog_search(self.enterprise_id,
                                                                   str(util.nvl(self.request.GET.get('search'))).strip()),
                                            self.request.GET.get('offset'),
                                            self.request.GET.get('limit'))
        return self.render(page, params)


    @view_config(route_name='ecom.site.page')
    def page(self):
        return self.render(self.request.matchdict.get('page'))


    @view_config(route_name='ecom.site.content.default')
    @view_config(route_name='ecom.site.content')
    def content(self):
        page = self.request.matchdict.get('page', 'content')
        params = self.params()
        params['content_name'] = content_name = self.request.matchdict.get('content_name')
        content = Content.find_by_name(self.request.ctx.site, content_name)
        if content:
            (params['seo_title'], params['seo_keywords'], params['seo_description']) = SmartSeo.obj_seo(content, self.request.ctx.site)
        return self.render(page, params)


    @view_config(route_name='ecom.site.login.default')
    @view_config(route_name='ecom.site.login')
    def login(self):
        page = self.request.matchdict.get('page', 'login')
        params = self.params()
        if params['customer'].customer_id and 'nextlink' in self.request.GET:
            return HTTPFound(self.request.GET['nextlink'])
        return self.render(page, params)
