import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.model.crm.product import Product
from pvscore.controllers.catalog.catalog import CatalogBaseController
from pvscore.lib.smart.scatalog import SmartCatalog
from pvscore.lib.shipping.shipping import UPSShipping
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class CartController(CatalogBaseController):

    @view_config(route_name='ecom.site.cart')
    @view_config(route_name='ecom.site.cart.default')
    def cart(self):
        page = self.request.matchdict.get('page', 'cart')
        params = self.params()
        params['products_related'] = SmartCatalog.related_product_list_cart(params['cart'], params['campaign'])
        return self.render(page, params)


    @view_config(route_name='ecom.site.cart.add', renderer="string")
    def add(self):
        """ KB: [2013-02-20]: MOD ATTR:  CartController.add : Allow for ajax of adding a simple item (HUS), or post/redir for adding products with attributes. """
        product_id = self.request.matchdict.get('product_id')
        quantity = self.request.matchdict.get('quantity')
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        product = Product.load(product_id)
        cart.add_item(product, self.request.ctx.campaign, quantity)
        self.session.changed()
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.update', renderer="string")
    def update(self):
        product_id = self.request.matchdict.get('product_id')
        quantity = self.request.matchdict.get('quantity')
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        product = Product.load(product_id)
        cart.remove_item(product)
        cart.add_item(product, self.request.ctx.campaign, quantity)
        self.session.changed()
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.clear', renderer="string")
    def clear(self):
        if not 'cart' in self.session:
            return 'True'
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        cart.remove_all()
        self.session.changed()
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.remove', renderer="string")
    def remove(self):
        if not 'cart' in self.session:
            return 'False' #pragma: no cover
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        product_id = self.request.matchdict.get('product_id')
        product = Product.load(product_id)
        cart.remove_item(product)
        self.session.changed()
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.checkout.default')
    @view_config(route_name='ecom.site.cart.checkout')
    def checkout(self):
        page = self.request.matchdict.get('page')
        if 'cart' not in self.session:
            return HTTPFound('/')   #pragma: no cover
        params = self.params()
        cart = self.session['cart']
        if self.request.ctx.site.config_json and not cart.shipping_options:
            shipper = None
            if self.request.ctx.site.shipping_method == 'UPS':
                shipper = UPSShipping()
            if shipper:
                cart.shipping_options = shipper.get_options(self.request.ctx.customer,
                                                            self.request.ctx.site,
                                                            cart)
                self.session.changed()
        return self.render(page, params)


    @view_config(route_name='ecom.site.cart.save_shipping')
    def save_shipping(self):
        if not 'cart' in self.session:
            return 'True'  #pragma: no cover
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        shipping_code = self.request.POST.get('shipping_code')
        cust = self.request.ctx.customer
        self.redir_if(not cust or not cart)
        cart.shipping_selection = shipping_code
        cart.shipping_addr1 = util.nvl(self.request.POST.get('shipping_addr1'), cust.addr1)
        cart.shipping_addr2 = util.nvl(self.request.POST.get('shipping_addr2'), cust.addr2)
        cart.shipping_city = util.nvl(self.request.POST.get('shipping_city'), cust.city)
        cart.shipping_state = util.nvl(self.request.POST.get('shipping_state'), cust.state)
        cart.shipping_zip = util.nvl(self.request.POST.get('shipping_zip'), cust.zip)
        cart.shipping_country = util.nvl(self.request.POST.get('shipping_country'), cust.country)
        cart.shipping_phone = util.nvl(self.request.POST.get('shipping_phone'), cust.phone)
        self.session.changed()
        return self.find_redirect()


