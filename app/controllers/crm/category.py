import pdb, re, logging
from app.lib.validate import validate
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.controllers.base import BaseController
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn, IsInternalReferrer
from app.model.crm.campaign import Campaign
from app.model.crm.company import Company
from app.model.crm.product import Product, ProductCategory, ProductCategoryJoin
import app.lib.util as util

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
        pc = ProductCategory.load(self.request.POST.get('category_id'))
        if not pc:
            pc = ProductCategory()
        pc.bind(self.request.POST)
        pc.mod_dt = util.now()
        pc.save()
        pc.flush()
        
        pc.clear_products()
        pc.flush()
        for k in self.request.POST.keys():
            if k.startswith('child_incl'):
                child_product_id = self.request.POST.get(k)
                pc.add_product(child_product_id)

        self.request.session.flash('Successfully saved %s.' % pc.name)
        return HTTPFound('/crm/product/category/edit/%s' % pc.category_id)

