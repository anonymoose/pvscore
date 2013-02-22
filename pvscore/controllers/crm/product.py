import re, logging
from pvscore.lib.validate import validate
from pvscore.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.company import Company
from pvscore.model.crm.product import Product, ProductReturn, InventoryJournal, ProductCategory
from pvscore.model.core.statusevent import StatusEvent
from pvscore.model.core.status import Status
from pvscore.model.crm.purchase import Vendor
from pvscore.model.core.asset import Asset
import pvscore.lib.util as util
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
            product_categories = ProductCategory.find_by_product(product)
        else:
            product = Product()
            product_categories = []
        self.forbid_if(self.request.ctx.user.is_vendor_user() and product.product_id and not self.request.ctx.user.vendor_id == product.vendor_id)
        children = product.get_children()
        other_products = product.find_eligible_children()
        non_children = []
        for prod in other_products:
            found = False
            for kid in children:
                if kid.child_id == prod.product_id:
                    found = True
                    break
            if found == False:
                non_children.append(prod)

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
            'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
            'is_attribute' : self.request.GET.get('is_attribute') == 'True', 
            'parent_product' : Product.load(self.request.GET.get('parent_id')) if 'parent_id' in self.request.GET else None
            }


    @view_config(route_name='crm.product.list', renderer='/crm/product.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'products' : Product.find_by_vendor(self.enterprise_id,
                                                    self.request.ctx.user.vendor) \
                    if self.request.ctx.user.is_vendor_user() \
                    else Product.find_all(self.enterprise_id)}


    @view_config(route_name='crm.product.inventory_list', renderer='string')
    @authorize(IsLoggedIn())
    def inventory_list(self):
        products = Product.find_by_vendor(self.request.ctx.user.vendor) if self.request.ctx.user and self.request.ctx.user.is_vendor_user() else Product.find_all(self.enterprise_id) #pylint: disable-msg=E1120

        campaigns = Campaign.find_all(self.enterprise_id)

        response = {
            'page': 1,
            'total': 1,
            'records': len(products)}

        rows = []

        for prod in products:
            #log.debug('%s %s/%s' % (p.product_id, i+1, len(products)))
            # blank spot at the beginning of the row is to make room for the
            # action buttons.  don't remove it.
            cells = ['', unicode(prod.product_id),
                     util.nvl(prod.name),
                     util.nvl(prod.sku),
                     util.nvl(prod.manufacturer),
                     util.nvl(unicode(prod.inventory)),
                     util.nvl(unicode(prod.inventory_par)),
                     util.nvl(unicode(prod.unit_cost))]
            # the column ordering in the UI is dependant on the order of the
            # campaigns that comes back from Campaign.find_all().  We use the
            # same ordering here so we are fine not adding some campaign ID here.
            for camp in campaigns:
                cells.append(util.nvl(util.money(prod.get_retail_price(camp))))

            rows.append({'id': str(prod.product_id),
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
                match = re.search(r'^.*_(.*)', k)
                if match:
                    campaign = Campaign.load(match.group(1))
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
            prod = Product.load(product_id)
        else:
            prod = Product()
        prod.bind(self.request.POST, True)
        prod.mod_dt = util.now()
        prod.clear_children()
        prod.save()
        self.db_flush()

        for k in self.request.POST.keys():
            if k.startswith('campaign_price'):
                match = re.search(r'^.*\[(.*)\]', k)
                if match:
                    campaign = Campaign.load(match.group(1))
                    price = self.request.POST.get(k)
                    discount = self.request.POST.get('campaign_discount[%s]' % campaign.campaign_id)
                    if price:
                        price = util.float_(price)
                        discount = util.float_(util.nvl(discount, 0.0))
                        prod.set_price(campaign, price, discount)
                    else:
                        prod.remove_price(campaign)

            if k.startswith('child_incl'):
                child_product_id = self.request.POST.get(k)
                child_product_quantity = self.request.POST.get('child_quantity_%s' % child_product_id)
                prod.add_child(child_product_id, child_product_quantity)

        prod.save()
        self.db_flush()

        redir_params = ''
        if 'parent_id' in self.request.POST and self.request.POST['parent_id']:
            parent = Product.load(self.request.POST['parent_id'])
            if not parent.has_child(prod.product_id):
                parent.add_child(prod.product_id)
                parent.save()
            redir_params = '?is_attribute=True&parent_id=%s' % parent.product_id

        inventory = str(self.request.POST.get('prod_inventory', '0'))
        if inventory and str(round(float(inventory), 2)) != str(round(util.nvl(InventoryJournal.total(prod), 0), 2)):
            InventoryJournal.create_new(prod, 'Inventory Adjust', inventory)
            self.db_flush()
            self.flash('Inventory Adjusted to %s' % inventory)

        prod.clear_attributes()
        for i in range(30):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                prod.set_attr(attr_name, attr_value)

        self.flash('Successfully saved %s.' % prod.name)
        
        return HTTPFound('/crm/product/edit/%s%s' % (prod.product_id, redir_params))


    @view_config(route_name='crm.product.ac.name', renderer='string')
    @authorize(IsLoggedIn())
    def autocomplete_by_name(self):
        if 'search_key' in self.request.GET and self.request.GET.get('search_key'):
            srch = self.request.GET.get('search_key')
            # customer_id = self.request.GET.get('customer_id')
            # if customer_id:
            #     customer = Customer.load(customer_id)
            #     lnames = Product.find_names_by_name_and_campaign(self.enterprise_id, srch, self.request.GET.get('max_rows', 10), customer.campaign)
            lnames = Product.find_names_by_name(self.enterprise_id, srch, self.request.GET.get('max_rows', 10))
            return json.dumps(lnames)


    @view_config(route_name='crm.product.show_orders', renderer='/crm/product.orders_list.mako')
    @authorize(IsLoggedIn())
    def show_orders(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'orders' : product.get_orders_report()
                }


    @view_config(route_name='crm.product.show_sales', renderer='/crm/product.sales_list.mako')
    @authorize(IsLoggedIn())
    def show_sales(self):
        product_id = self.request.matchdict['product_id']
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'sales' : product.get_sales_report(),
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'product' : product
                }


    @view_config(route_name='crm.product.show_purchases', renderer='/crm/product.purchases_list.mako')
    @authorize(IsLoggedIn())
    def show_purchases(self):
        product_id = self.request.matchdict['product_id']
        from pvscore.model.crm.purchase import PurchaseOrderItem
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        return {'product' : product,
                'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, product), 'event_id', 'display_name'),
                'purchase_order_items' : PurchaseOrderItem.find_by_product(product)
                }


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


    @view_config(route_name='crm.product.upload_picture', renderer="string")
    def upload_picture(self):
        product_id = self.request.matchdict.get('product_id')
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        ass = Asset.create_new(product, self.enterprise_id, self.request)
        self.flash('Uploaded new image to product')
        product.invalidate_caches()
        return str(ass.id)


    @view_config(route_name='crm.product.delete_picture', renderer="string")
    @authorize(IsLoggedIn())
    def delete_picture(self):
        product_id = self.request.matchdict.get('product_id')
        product = Product.load(product_id)
        self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
        asset_id = self.request.matchdict.get('asset_id')
        asset = Asset.load(asset_id)
        self.forbid_if(asset.fk_type != 'Product' or str(asset.fk_id) != str(product.product_id))
        asset.delete()
        return 'True'
        

    # @view_config(route_name='crm.product.json', renderer='/crm/product.json.mako')
    # @authorize(IsLoggedIn())
    # def json(self):
    #     product_id = self.request.matchdict['product_id']
    #     campaign_id = self.request.matchdict['campaign_id']
    #     product = Product.load(product_id)
    #     if not product: return 'False'
    #     self.forbid_if(not product or product.company.enterprise_id != self.enterprise_id)
    #     return {'unit_price' : product.get_unit_price(campaign_id),
    #             'product' : product}


    # def show_barcode(self, product_id):
    #     c.product_id = product_id
    #     return self.render('/crm/product.barcode.mako')


    # def barcodes(self):
    #     e = Enterprise.load(self.enterprise_id)
    #     self.forbid_if(not e)
    #     c.products = []

    #     for cmp in e.companies:
    #         for p in cmp.get_all_active_products():
    #             c.products.append(p)

    #     return self.render('/crm/product.all_barcodes.mako')

     
