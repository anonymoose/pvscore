import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.model.crm.product import Product
from pvscore.controllers.catalog.catalog import CatalogBaseController
from pvscore.lib.shipping.shipping import UPSShipping

log = logging.getLogger(__name__)

class CartController(CatalogBaseController):

    @view_config(route_name='ecom.site.cart')
    @view_config(route_name='ecom.site.cart.default')
    def cart(self):
        page = self.request.matchdict.get('page', 'cart')
        params = self.params()
        return self.render(page, params)


    @view_config(route_name='ecom.site.cart.add', renderer="string")
    def add(self):
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


    @view_config(route_name='ecom.site.cart.set_shipping', renderer="string")
    def set_shipping(self):
        if not 'cart' in self.session:
            return 'True'
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        shipping_code = self.request.matchdict.get('shipping_code')
        cart.shipping_selection = shipping_code
        self.session.changed()
        return 'True' if not redir else HTTPFound(redir)


