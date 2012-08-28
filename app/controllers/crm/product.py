import pdb, re, logging
from app.lib.validate import validate
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn, IsInternalReferrer
from app.model.core.users import Users
from app.model.crm.campaign import Campaign
from app.model.crm.company import Company, Enterprise
from app.model.crm.product import Product, ProductReturn, InventoryJournal, ProductCategory
from app.model.core.statusevent import StatusEvent
from app.model.core.status import Status
from app.model.crm.purchase import Vendor
import app.lib.util as util
import app.lib.db as db
import simplejson as json

log = logging.getLogger(__name__)

class ProductController(BaseController):

    @view_config(route_name='crm.product.edit', renderer='/crm/product.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()

        
    @view_config(route_name='crm.product.new', renderer='/crm/product.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        product_id = self.request.matchdict.get('product_id')
        campaigns = Campaign.find_all(self.enterprise_id)
        companies = util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name')
        product_types = Product.get_types()
        vendors = util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name', True)
        categories = util.select_list(ProductCategory.find_all(self.enterprise_id), 'category_id', 'name', True)
        if product_id:
            product = Product.load(product_id)
            self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)

            """ KB: [2011-11-03]: We are allowing them to  """
            product_categories = ProductCategory.find_by_product(product)
        else:
            product = Product()
            product_categories = []
        self.forbid_if(self.request.ctx.user.is_vendor_user() and product.product_id and not self.request.ctx.user.vendor_id == product.vendor_id)
        children = product.get_children()
        other_products = product.find_eligible_children()
        non_children = []
        for p in other_products:
            found = False
            for kid in children:
                if kid.child_id == p.product_id:
                    found = True
                    break
            if found == False:
                non_children.append(p)

        return  {
            'product' : product,
            'campaigns' : campaigns,
            'companies' : companies,
            'product_types' : product_types,
            'vendors' : vendors,
            'categories' : categories,
            'product_categories' : product_categories,
            'children' : children,
            'non_children': non_children,
            'other_products' : other_products,
            'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name')
            }


    @view_config(route_name='crm.product.list', renderer='/crm/product.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'products' : Product.find_by_vendor(self.enterprise_id,
                                                    self.request.ctx.user.vendor) \
                    if self.request.ctx.user.is_vendor_user() \
                    else Product.find_all (self.enterprise_id)}


    @view_config(route_name='crm.product.inventory_list', renderer='string')
    @authorize(IsLoggedIn())
    def inventory_list(self):
        products = Product.find_by_vendor(self.request.ctx.user.vendor) \
            if self.request.ctx.user and self.request.ctx.user.is_vendor_user() else Product.find_all(self.enterprise_id)

        campaigns = Campaign.find_all(self.enterprise_id)

        response = {
            'page': 1,
            'total': 1,
            'records': len(products)}

        rows = []

        for i,p in enumerate(products):
            #log.debug('%s %s/%s' % (p.product_id, i+1, len(products)))
            # blank spot at the beginning of the row is to make room for the
            # action buttons.  don't remove it.
            cells = ['', unicode(p.product_id),
                     util.nvl(p.name),
                     util.nvl(p.sku),
                     util.nvl(p.manufacturer),
                     util.nvl(unicode(p.inventory)),
                     util.nvl(unicode(p.inventory_par)),
                     util.nvl(unicode(p.unit_cost))]
            # the column ordering in the UI is dependant on the order of the
            # campaigns that comes back from Campaign.find_all().  We use the
            # same ordering here so we are fine not adding some campaign ID here.
            for cmp in campaigns:
                cells.append(util.nvl(util.money(p.get_retail_price(cmp))))

            rows.append({'id': str(p.product_id),
                         'cell': cells})

        response['rows'] = rows
        return json.dumps(response)


    @view_config(route_name='crm.product.show_inventory', renderer='/crm/product.inventory.mako')
    @authorize(IsLoggedIn())
    def show_inventory(self):
        return {'products' : Product.find_by_vendor(self.enterprise_id, self.request.ctx.user.vendor) \
                    if self.request.ctx.user.is_vendor_user() else Product.find_all(self.enterprise_id),
                'campaigns' : Campaign.find_all(self.enterprise_id)
                }

    
    @view_config(route_name='crm.product.save_inventory', renderer='string')
    @authorize(IsLoggedIn())
    @validate((('id', 'required'),
               ('inventory', 'required'),('inventory', 'number'),
               ('inventory_par', 'number'),
               ('name', 'required'),
               ('unit_cost', 'number')))
    def save_inventory(self):
        prod = Product.load(self.request.POST.get('id'))
        self.forbid_if(not prod or prod.company.enterprise_id != self.enterprise_id)
        InventoryJournal.create_new(prod, 'Inventory Adjust', float(self.request.POST.get('inventory', 0)))
        prod.name = self.request.POST.get('name')
        prod.manufacturer = self.request.POST.get('manufacturer')
        prod.unit_cost = util.nvl(self.request.POST.get('unit_cost'), 0.0)
        prod.sku = self.request.POST.get('sku')
        prod.inventory_par = util.nvl(self.request.POST.get('inventory_par'), None)
        prod.save()

        # save all the prices, prefixed by "cmp_"
        for k in self.request.POST.keys():
            if k.startswith('cmp_'):
                m = re.search(r'^.*_(.*)', k)
                if m:
                    campaign = Campaign.load(m.group(1))
                    price = self.request.POST.get(k)
                    if price:
                        price = util.float_(price)
                        prod.set_price_only(campaign, price)
                    else:
                        prod.remove_price(campaign)
                    prod.invalidate_caches(campaign_id=campaign.campaign_id)
        return 'True'
    

    @view_config(route_name='crm.product.save', renderer='/crm/product.edit.mako')
    @authorize(IsLoggedIn())
    @validate((('name', 'required')))
    def save(self):
        product_id = self.request.POST.get('product_id')
        if product_id:
            p = Product.load(product_id)
        else:
            p = Product()
        p.bind(self.request.POST, True)
        p.mod_dt = util.now()
        p.clear_children()
        p.save()
        self.db_flush()

        for k in self.request.POST.keys():
            if k.startswith('campaign_price'):
                m = re.search(r'^.*\[(.*)\]', k)
                if m:
                    log.debug('loading campaign %s %s' % (k, m.group(1)))
                    campaign = Campaign.load(m.group(1))
                    price = self.request.POST.get(k)
                    discount = self.request.POST.get('campaign_discount[%d]' % campaign.campaign_id)
                    if price:
                        price = util.float_(price)
                        discount = util.float_(discount)
                        p.set_price(campaign, price, discount)
                    else:
                        p.remove_price(campaign)

            if k.startswith('child_incl'):
                child_product_id = self.request.POST.get(k)
                child_product_quantity = self.request.POST.get('child_quantity_%d' % int(child_product_id))
                p.add_child(child_product_id, child_product_quantity)

        p.save()
        self.db_flush()

        inventory = str(self.request.POST.get('prod_inventory', '0'))
        if inventory and str(round(float(inventory), 2)) != str(round(util.nvl(InventoryJournal.total(p), 0), 2)):
            InventoryJournal.create_new(p, 'Inventory Adjust', inventory)
            self.db_flush()
            self.flash('Inventory Adjusted to %s' % inventory)

        p.clear_attributes()
        for i in range(30):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                p.set_attr(attr_name, attr_value)

        """ KB: [2011-11-03]: We are only handling the one-to-one product-to-category relationship in the product manager screen.
        Anything more complex has to be handled elsewhere.
        So, if category_id is in the post, then we know that the UI detected that there was only one category before.
        Thus, we are safe to delete here.

        if 'category_id' in self.request.POST:
            ProductCategory.clear_by_product(p)
            pc = ProductCategory.load(self.request.POST.get('category_id'))
            if pc:
                pc.add_product(p.product_id)
        """
        
        self.flash('Successfully saved %s.' % p.name)
        return HTTPFound('/crm/product/edit/%s' % p.product_id)


    @view_config(route_name='crm.product.ac.name', renderer='string')
    @authorize(IsLoggedIn())
    def autocomplete_by_name(self):
        if not 'search_key' in self.request.GET or not self.request.GET.get('search_key'): return
        q = self.request.GET.get('search_key')
        lnames = Product.find_names_by_name(self.enterprise_id, q, self.request.GET.get('max_rows', 10))
        return json.dumps(lnames)


    @view_config(route_name='crm.product.show_orders', renderer='/crm/product.orders_list.mako')
    @authorize(IsLoggedIn())
    def show_orders(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'orders' : product.get_orders_report()}


    @view_config(route_name='crm.product.show_sales', renderer='/crm/product.sales_list.mako')
    @authorize(IsLoggedIn())
    def show_sales(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'sales' : product.get_sales_report(),
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'product' : product}


    @view_config(route_name='crm.product.show_purchases', renderer='/crm/product.purchases_list.mako')
    @authorize(IsLoggedIn())
    def show_purchases(self):
        product_id = self.request.matchdict['product_id']
        from app.model.crm.purchase import PurchaseOrderItem
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'purchase_order_items' : PurchaseOrderItem.find_by_product(product)}


    @view_config(route_name='crm.product.show_history', renderer='/crm/product.history_list.mako')
    @authorize(IsLoggedIn())
    def show_history(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'history' : Status.find(product)
                }


    @view_config(route_name='crm.product.show_returns', renderer='/crm/product.returns_list.mako')
    @authorize(IsLoggedIn())
    def show_returns(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'returns' : ProductReturn.find(product)}


    @view_config(route_name='crm.product.save_status')
    @authorize(IsLoggedIn())
    @validate((('product_id', 'required'),
               ('event_id', 'required')))
    def save_status(self):
        product_id = self.request.POST['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        event = StatusEvent.load(self.request.POST['event_id'])
        self.forbid_if(not event or (not event.is_system and event.enterprise_id != self.enterprise_id))
        note = self.request.POST.get('note')
        Status.add(None, product, event, note, self.request.ctx.user)
        return HTTPFound('/crm/product/show_history/%s' % product_id)


    """
    @view_config(route_name='crm.product.json', renderer='/crm/product.json.mako')
    @authorize(IsLoggedIn())
    def json(self):
        product_id = self.request.matchdict['product_id']
        campaign_id = self.request.matchdict['campaign_id']
        product = Product.load(product_id)
        if not product: return 'False'
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'unit_price' : product.get_unit_price(campaign_id),
                'product' : product}


    def show_barcode(self, product_id):
        c.product_id = product_id
        return self.render('/crm/product.barcode.mako')


    def barcodes(self):
        e = Enterprise.load(self.enterprise_id)
        self.forbid_if(not e)
        c.products = []

        for cmp in e.companies:
            for p in cmp.get_all_active_products():
                c.products.append(p)

        return self.render('/crm/product.all_barcodes.mako')
    """
     
