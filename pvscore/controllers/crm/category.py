#import pdb
import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.lib.decorators.authorize import authorize 
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.company import Company
from pvscore.model.crm.product import Product, ProductCategory
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class CategoryController(BaseController):
    @view_config(route_name='crm.product.category.new', renderer='/crm/category.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()

    @view_config(route_name='crm.product.category.edit', renderer='/crm/category.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()

    def _edit_impl(self):
        category_id = self.request.matchdict.get('category_id')
        companies = util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name')
        if category_id:
            category = ProductCategory.load(category_id)
            self.forbid_if(not category or category.company.enterprise_id != self.enterprise_id)
        else:
            category = ProductCategory()

        all_products = Product.find_all(self.enterprise_id)
        return {'companies' : companies,
                'category' : category,
                'all_products' : all_products}
    

    @view_config(route_name='crm.product.category.list', renderer='/crm/category.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'categories' : ProductCategory.find_all(self.enterprise_id) }


    @view_config(route_name='crm.product.category.save', renderer='/crm/category.edit.mako')
    @authorize(IsLoggedIn())
    def save(self):
        pcat = ProductCategory.load(self.request.POST.get('category_id'))
        if not pcat:
            pcat = ProductCategory()
        pcat.bind(self.request.POST)
        pcat.mod_dt = util.now()
        pcat.save()
        pcat.flush()
        
        pcat.clear_products()
        pcat.flush()
        for k in self.request.POST.keys():
            if k.startswith('child_incl'):
                child_product_id = self.request.POST.get(k)
                pcat.add_product(child_product_id)

        pcat.flush()
        pcat.invalidate_caches()
        self.request.session.flash('Successfully saved %s.' % pcat.name)
        return HTTPFound('/crm/product/category/edit/%s' % pcat.category_id)

