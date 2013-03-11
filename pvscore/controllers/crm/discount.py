import logging
import datetime, calendar
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.discount import Discount
from pvscore.model.crm.comm import Communication
from pvscore.model.crm.company import Company
from pvscore.model.crm.product import Product
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class DiscountController(BaseController):

    @view_config(route_name="crm.discount.edit", renderer='/crm/discount.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name="crm.discount.new", renderer='/crm/discount.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        discount_id = self.request.matchdict.get('discount_id')
        discount = None
        if discount_id:
            discount = Discount.load(discount_id)
            self.forbid_if(not discount or discount.enterprise_id != self.enterprise_id)
        else:
            discount = Discount()

        included_products = discount.get_products()
        not_included_products = []
        for prod in Product.find_all(self.enterprise_id):
            found = False
            for incl in included_products:
                if incl.product_id == prod.product_id:
                    found = True
                    break
            if found == False:
                not_included_products.append(prod)

        return {
            'discount': discount,
            'included_products' : included_products,
            'not_included_products' : not_included_products,
            'excluded' : Product.find_all(self.enterprise_id),
            'tomorrow' : util.today_date() + datetime.timedelta(days=1),
            'plus14' : util.today_date() + datetime.timedelta(days=14)
            }


    @view_config(route_name="crm.discount.list", renderer='/crm/discount.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'discounts' : Discount.find_all_active(self.enterprise_id)}


    @view_config(route_name='crm.discount.delete', renderer='string')
    @authorize(IsLoggedIn())
    def delete(self):
        discount_id = self.request.matchdict.get('discount_id')
        discount = Discount.load(discount_id)
        self.forbid_if(not discount or str(discount.enterprise_id) != str(self.enterprise_id))
        discount.mod_dt = util.now()
        discount.delete_dt = util.now()
        discount.invalidate_caches()
        return 'True'


    @view_config(route_name="crm.discount.save")
    @authorize(IsLoggedIn())
    def save(self):
        discount = Discount.load(self.request.POST.get('discount_id'))
        if not discount:
            discount = Discount()
            discount.enterprise_id = self.enterprise_id
        else:
            self.forbid_if(discount.enterprise_id != self.enterprise_id)
        discount.bind(self.request.POST)
        discount.save()
        discount.flush()

        included_products = {}
        for k in self.request.POST.keys():
            if k.startswith('product_incl'):
                product_id = self.request.POST.get(k)
                included_products[product_id] = 1

        for current_prod in discount.get_products():
            if current_prod.product_id not in included_products.keys():
                discount.clear_product(current_prod.product_id)
                
        for new_included_product_id in included_products.keys():
            discount.add_product(new_included_product_id)

        discount.invalidate_caches()
        self.request.session.flash('Successfully saved %s.' % discount.name)
        return HTTPFound('/crm/discount/edit/%s' % discount.discount_id)

