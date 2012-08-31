import logging
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import IsLoggedIn
from app.model.crm.company import Company
from app.model.crm.product import Product, InventoryJournal
from app.model.core.status import Status
from app.model.core.statusevent import StatusEvent
import app.lib.util as util
from app.model.crm.purchase import PurchaseOrder, PurchaseOrderItem, Vendor
import simplejson as json

log = logging.getLogger(__name__)

class PurchaseController(BaseController):

    @view_config(route_name='crm.purchase.vendor.edit', renderer='/crm/purchase.edit_vendor.mako')
    @authorize(IsLoggedIn())
    def edit_vendor(self):
        return self._edit_vendor_impl()
        

    @view_config(route_name='crm.purchase.vendor.new', renderer='/crm/purchase.edit_vendor.mako')
    @authorize(IsLoggedIn())
    def new_vendor(self):
        return self._edit_vendor_impl()

    def _edit_vendor_impl(self):
        vendor_id = self.request.matchdict.get('vendor_id')
        return {'vendor' : Vendor.load(vendor_id) if vendor_id else Vendor() }


    @view_config(route_name='crm.purchase.vendor.list', renderer='/crm/purchase.list_vendors.mako')
    @authorize(IsLoggedIn())
    def list_vendors(self):
        return {'vendors' : Vendor.find_all(self.enterprise_id) }


    @view_config(route_name='crm.purchase.vendor.save')
    @authorize(IsLoggedIn())
    def save_vendor(self):
        ent = Vendor.load(self.request.POST.get('vendor_id'))
        if not ent:
            ent = Vendor()
        ent.bind(self.request.POST, True)
        ent.enterprise_id = self.enterprise_id
        ent.save()
        ent.flush()
        self.flash('Successfully saved %s.' % ent.name)
        return HTTPFound('/crm/purchase/vendor/edit/%d' % int(ent.vendor_id))


    @view_config(route_name='crm.purchase.new', renderer='/crm/purchase.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    @view_config(route_name='crm.purchase.edit', renderer='/crm/purchase.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()

    
    def _edit_impl(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        purchase = PurchaseOrder.load(purchase_order_id) if purchase_order_id else PurchaseOrder()
        return {
            'companies' : util.select_list(Company.find_all(self.enterprise_id), 'company_id', 'name'),
            'vendors' : util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name', True),
            'products' : Product.find_all(self.enterprise_id),
            'purchase' : purchase,
            'events' : util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, purchase), 'event_id', 'display_name') if purchase.purchase_order_id else []
            }

    
    @view_config(route_name='crm.purchase.search', renderer='/crm/purchase.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        vendor_id = self.request.POST.get('vendor_id') 
        from_dt = self.request.POST.get('from_dt', util.str_today())
        to_dt = self.request.POST.get('to_dt', util.str_today())
        return {
            'vendor_id' : vendor_id, 
            'from_dt' : from_dt, 
            'to_dt' : to_dt, 
            'purchases' : PurchaseOrder.search(self.enterprise_id, vendor_id, from_dt, to_dt),
            'vendors' : util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name')
            }


    @view_config(route_name='crm.purchase.show_search', renderer='/crm/purchase.search.mako')
    @authorize(IsLoggedIn())
    def show_search(self):
        return {
            'vendors' : util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name'),
            'purchases' : None
            }


    @view_config(route_name='crm.purchase.show_history', renderer='/crm/purchase.history_list.mako')
    @authorize(IsLoggedIn())
    def show_history(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        purchase = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not purchase or purchase.company.enterprise_id != self.enterprise_id)
        return {
            'history' : Status.find(purchase),
            'purchase' : purchase,
            'offset' : self.offset
            }

                
    @view_config(route_name='crm.purchase.list', renderer='/crm/purchase.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'purchases' : PurchaseOrder.find_all_open(self.enterprise_id)}


    @view_config(route_name='crm.purchase.save')
    @authorize(IsLoggedIn())
    def save(self):
        porder = PurchaseOrder.load(self.request.POST.get('purchase_order_id'))
        new = False
        if not porder:
            new = True
            porder = PurchaseOrder()
        porder.bind(self.request.POST)
        porder.save()
        porder.flush()
        Status.add(None, porder, Status.find_event(self.enterprise_id, porder, 'CREATED' if new else 'MODIFIED'),
                   'Purchase Order %s' % ('CREATED' if new else 'MODIFIED'),
                   self.request.ctx.user)
        self.db_flush()
        self.flash('Successfully saved PO %s.' % porder.purchase_order_id)
        return HTTPFound('/crm/purchase/edit/%d' % int(porder.purchase_order_id))


    @view_config(route_name='crm.purchase.order_item_json', renderer="string")
    @authorize(IsLoggedIn())
    def order_item_json(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        order_item_id = self.request.matchdict.get('order_item_id')
        porder = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not porder)
        poi = PurchaseOrderItem.load(order_item_id)
        self.forbid_if(not poi or poi.purchase_order != porder)
        return json.dumps({'order_item_id':poi.order_item_id, 
                           'note':poi.note,
                           'quantity':poi.quantity, 
                           'unit_cost':poi.unit_cost,
                           'prod_name':poi.product.name})


    @view_config(route_name='crm.purchase.save_purchase_order_item', renderer="string")
    @authorize(IsLoggedIn())
    def save_purchase_order_item(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        self.forbid_if(not 'product_id' in self.request.GET or not self.request.GET.get('product_id'))
        poi = PurchaseOrderItem.load(self.request.POST.get('order_item_id'))
        if not poi:
            poi = PurchaseOrderItem()
            poi.purchase_order_id = purchase_order_id
        poi.bind(self.request.POST)
        poi.product_id = self.request.GET.get('product_id')
        poi.note = self.request.POST.get('order_note')
        poi.save()
        poi.flush()
        porder = poi.purchase_order
        Status.add(None, porder, Status.find_event(self.enterprise_id, porder, 'MODIFIED'),
                   'Purchase Order %s. "%s" added.' % ('MODIFIED', poi.product.name),
                   self.request.ctx.user)
        self.db_flush()
        return '{"id": %s}' % poi.order_item_id


    @view_config(route_name='crm.purchase.delete_purchase_order_item', renderer="string")
    @authorize(IsLoggedIn())
    def delete_purchase_order_item(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        order_item_id = self.request.matchdict.get('order_item_id')
        porder = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not porder)
        poi = PurchaseOrderItem.load(order_item_id)
        self.forbid_if(not poi or poi.purchase_order != porder)
        prod = poi.product
        poi.delete()
        Status.add(None, porder, Status.find_event(self.enterprise_id, porder, 'MODIFIED'),
                   'Purchase Order %s. "%s" removed.' % ('MODIFIED', prod.name),
                   self.request.ctx.user)
        poi.flush()
        return 'True'


    @view_config(route_name='crm.purchase.save_status')
    @authorize(IsLoggedIn())
    def save_status(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        purchase = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not purchase or purchase.company.enterprise_id != self.enterprise_id)
        event = StatusEvent.load(self.request.POST.get('event_id'))
        self.forbid_if(not event or not self.request.POST.get('event_id') or (not event.is_system and event.enterprise_id != self.enterprise_id))
        note = self.request.POST.get('note')
        Status.add(None, purchase, event, note, self.request.ctx.user)
        self.flash("Saved status")
        return HTTPFound('/crm/purchase/edit/%s' % purchase_order_id)


    @view_config(route_name='crm.purchase.complete', renderer="string")
    @authorize(IsLoggedIn())
    def complete(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        porder = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not porder or porder.company.enterprise_id != self.enterprise_id)
        porder.complete_dt = util.today()
        porder.save()
        for oitem in porder.order_items:
            if not oitem.complete_dt:
                oitem.complete_dt = util.today()
                oitem.save()
                InventoryJournal.create_new(oitem.product, 'Item Receipt', oitem.quantity)
        Status.add(None, porder, Status.find_event(self.enterprise_id, porder, 'COMPLETED'),
                   'Purchase Order Completed', self.request.ctx.user) 
        return 'True'


    @view_config(route_name='crm.purchase.complete_item', renderer="string")
    @authorize(IsLoggedIn())
    def complete_item(self):
        purchase_order_id = self.request.matchdict.get('purchase_order_id')
        order_item_id = self.request.matchdict.get('order_item_id')
        porder = PurchaseOrder.load(purchase_order_id)
        self.forbid_if(not porder)
        poi = PurchaseOrderItem.load(order_item_id)
        self.forbid_if(not poi or poi.purchase_order != porder or poi.complete_dt)
        poi.complete_dt = util.today()
        poi.save()
        poi.flush()
        InventoryJournal.create_new(poi.product, 'Item Receipt', poi.quantity)
        Status.add(None, porder, Status.find_event(self.enterprise_id, porder, 'COMPLETED'),
                   'Purchase Order Item "%s" Completed' % poi.product.name,
                   self.request.ctx.user) 
        return 'True'
