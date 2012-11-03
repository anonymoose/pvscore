import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.model.crm.product import Product
from pvscore.controllers.catalog.catalog import CatalogBaseController


log = logging.getLogger(__name__)

class CartController(CatalogBaseController):

    @view_config(route_name='ecom.site.cart')
    @view_config(route_name='ecom.site.cart.default')
    def cart(self):
        # /cart/{page}
        page = self.request.matchdict.get('page', 'cart')
        params = self.params()
        return self.render(page, params)


    @view_config(route_name='ecom.site.cart.add', renderer="string")
    def add(self):
        # /cart/{page}
        product_id = self.request.matchdict.get('product_id')
        quantity = self.request.matchdict.get('quantity')
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        product = Product.load(product_id)
        cart.add_item(product, self.request.ctx.campaign, quantity)
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.clear', renderer="string")
    def clear(self):
        if not 'cart' in self.session:
            return 'True'
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        del cart.items
        cart.items = []
        return 'True' if not redir else HTTPFound(redir)


    @view_config(route_name='ecom.site.cart.clear', renderer="string")
    def remove(self):
        if not 'cart' in self.session:
            return 'False'
        redir = self.request.GET.get('redir')
        cart = self.session['cart']
        product_id = self.request.matchdict.get('product_id')
        product = Product.load(product_id)
        cart.remove_item(product)
        return 'True' if not redir else HTTPFound(redir)


