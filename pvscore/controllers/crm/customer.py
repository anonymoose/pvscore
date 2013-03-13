#pylint: disable-msg=C0302
import logging, re
from pvscore.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.lib.validate import validate
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn, IsCustomerLoggedIn
from pvscore.model.crm.customer import Customer, CustomerPhase
from pvscore.model.crm.product import Product, ProductReturn, InventoryJournal
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.journal import Journal
from pvscore.model.crm.customerorder import CustomerOrder
from pvscore.model.crm.orderitem import OrderItem, OrderItemTermsAcceptance
from pvscore.model.core.status import Status
from pvscore.model.core.users import Users
from pvscore.model.core.statusevent import StatusEvent
from pvscore.model.crm.billing import Billing
from pvscore.lib.billing_api import BaseBillingApi
import simplejson as json
import pvscore.lib.util as util
from pvscore.lib.cart import Cart
from pvscore.lib.mail import UserMail

log = logging.getLogger(__name__)

class CustomerController(BaseController):
    @view_config(route_name='crm.customer.edit', renderer='/crm/customer.edit.mako')
    @authorize(IsLoggedIn())
    @validate((('customer_id', 'string'),
               ('customer_id', 'required')))
    def edit(self):
        return self._edit_impl()


    @view_config(route_name='crm.customer.new', renderer='/crm/customer.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _add_to_recent(self, customer):
        if not 'recent_customers' in self.session:
            self.session['recent_customers'] = {}
        self.session['recent_customers'][customer.customer_id] = "%s, %s" % (customer.lname, customer.fname)


    def _edit_impl(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = None
        if customer_id:
            customer = Customer.load(customer_id)
            self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
            self._add_to_recent(customer)
        else:
            customer = Customer()
            customer.campaign = self.request.ctx.site.company.default_campaign
        return {
            'customer' : customer,
            'users' : util.select_list(Users.find_all(self.enterprise_id), 'user_id', ['fname', 'lname'], True),
            'phases' : util.select_list(CustomerPhase.find_all(self.enterprise_id), 'phase_id', 'display_name', True),
            'campaigns' : util.select_list(Campaign.find_all(self.enterprise_id), 'campaign_id', 'name')
            }


    @view_config(route_name='crm.customer.save')
    @authorize(IsLoggedIn())
    @validate((('fname', 'string'),
               ('fname', 'required'),
               ('lname', 'string'),
               ('lname', 'required')))
    def save(self):
        return self._save(self.request.POST['customer_id'])


    def _save(self, customer_id=None, do_redir=True):
        user_id = None
        if self.request.ctx.user:
            user_id = self.request.ctx.user.user_id
        cust = Customer.load(customer_id)
        if not cust:
            cust = Customer()
            cust.user_created = cust.user_assigned = user_id
        else:
            self.forbid_if(cust.campaign.company.enterprise_id != self.enterprise_id)
        cust.bind(self.request.POST)
        cust.save()
        cust.flush()
        cust.clear_attributes()
        for i in range(10):
            attr_name = self.request.POST.get('attr_name[%d]' % i)
            attr_value = self.request.POST.get('attr_value[%d]' % i)
            if attr_name and attr_value:
                cust.set_attr(attr_name, attr_value)
        self.flash('Successfully saved %s %s.' % (cust.fname, cust.lname))
        if do_redir:
            redir = self.request.POST.get('redir')
            return HTTPFound(redir if redir else '/crm/customer/edit/%s' % cust.customer_id)
        else:
            return cust


    @view_config(route_name='crm.customer.autocomplete.name', renderer='string')
    @authorize(IsLoggedIn())
    @validate((('search_key', 'required')))
    def autocomplete(self):
        key = self.request.GET.get('search_key')
        lnames = Customer.find_last_names_autocomplete(self.enterprise_id, key, self.request.GET.get('limit', 10))
        return json.dumps(lnames)


    @view_config(route_name='crm.customer.show_search', renderer='/crm/customer.search.mako')
    @authorize(IsLoggedIn())
    def show_search(self):
        return {
            'company_name' : None,
            'fname' : None,
            'lname' : None,
            'email' : None,
            'phone' : None,
            'customers' : None,
            'user_assigned' : None,
            'users' : util.select_list(Users.find_all(self.enterprise_id), 'user_id', ['fname', 'lname'], True)
            }


    @view_config(route_name='crm.customer.search', renderer='/crm/customer.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        ret = {
            'company_name' : None,
            'fname' : None,
            'lname' : None,
            'email' : None,
            'phone' : None,
            'customers' : None,
            'user_assigned' : None,
            'users' : util.select_list(Users.find_all(self.enterprise_id), 'user_id', ['fname', 'lname'], True)
            }

        ret['company_name'] = self.request.POST.get('company_name', self.request.GET.get('company_name'))
        ret['fname'] = self.request.POST.get('fname', self.request.GET.get('fname'))
        ret['lname'] = self.request.POST.get('lname', self.request.GET.get('lname'))
        ret['email'] = self.request.POST.get('email', self.request.GET.get('email'))
        ret['phone'] = self.request.POST.get('phone', self.request.GET.get('phone'))
        ret['user_assigned'] = self.request.POST.get('user_assigned', self.request.GET.get('user_assigned'))
        ret['customers'] = Customer.search(self.enterprise_id, ret['company_name'], ret['fname'],
                                           ret['lname'], ret['email'], ret['phone'], ret['user_assigned'])
        if 'customers' in ret and len(ret['customers']) == 1:
            ret = HTTPFound('/crm/customer/edit/%s' % ret['customers'][0].customer_id)
        return ret


    @view_config(route_name='crm.customer.show_orders', renderer='/crm/customer.orders_list.mako')
    @authorize(IsLoggedIn())
    def show_orders(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'customer' : customer,
            'orders' : [order for order in customer.orders if order.delete_dt is None and order.cancel_dt is None]
            }


    @view_config(route_name='crm.customer.show_history', renderer='/crm/customer.history_list.mako')
    @authorize(IsLoggedIn())
    def show_history(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'customer' : customer,
            'history' : Status.find_by_customer(customer, self.offset),
            'offset' : self.offset
            }


    @view_config(route_name='crm.customer.show_attributes', renderer='/crm/customer.attributes.mako')
    @authorize(IsLoggedIn())
    def show_attributes(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'customer' : customer,
            'attrs' : customer.get_attrs()
            }


    @view_config(route_name='crm.customer.show_billings', renderer='/crm/customer.billings_list.mako')
    @authorize(IsLoggedIn())
    def show_billings(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'customer' : customer,
            'billings' : Journal.find_all_by_customer(customer, self.offset),
            'offset' : self.offset
            }


    @view_config(route_name='crm.customer.show_billing_dialog', renderer='/crm/customer.view_billing.mako')
    @authorize(IsLoggedIn())
    def show_billing_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        journal_id = self.request.matchdict.get('journal_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        journal = Journal.load(journal_id)
        self.forbid_if(not journal or str(journal.customer_id) != str(customer_id))
        return {
            'customer' : customer,
            'journal' : journal
            }


    @view_config(route_name='crm.customer.cancel_order_dialog', renderer='/crm/customer.cancel_order.mako')
    @authorize(IsLoggedIn())
    def cancel_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = CustomerOrder.load(order_id)
        self.forbid_if(not order or order.customer_id != customer.customer_id)
        return {
            'customer' : customer,
            'order' : order
            }


    @view_config(route_name='crm.customer.cancel_order', renderer='string')
    @authorize(IsLoggedIn())
    def cancel_order(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        self._cancel_order_impl(order_id,
                                self.request.POST.get('cancel_reason'),
                                False)
        self.flash("Order Cancelled")
        return HTTPFound('/crm/customer/show_orders/%s' % customer_id)


    def _cancel_order_impl(self, order_id, reason, by_customer=False):
        codr = CustomerOrder.load(order_id)
        self.forbid_if(not codr)
        cust = codr.customer
        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        if api.cancel_order(codr, cust.billing):
            Status.add(cust, cust, Status.find_event(self.enterprise_id, cust, 'NOTE'), 'Billing Cancelled at gateway')
        codr.cancel(reason, by_customer)
        cust.invalidate_caches()


    @view_config(route_name='crm.customer.add_order_dialog', renderer='/crm/customer.add_order.mako')
    @authorize(IsLoggedIn())
    def add_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        return self._prep_add_order_dialog(customer_id)


    @view_config(route_name='crm.customer.add_order', renderer='string')
    @authorize(IsLoggedIn())
    def add_order(self):
        """ KB: [2013-02-20]: MOD ATTR CustomerController.add_order : Modify to allow for attributes to be passed in the post. """
        customer_id = self.request.matchdict.get('customer_id')
        cust = Customer.load(customer_id)
        self.forbid_if(not cust)

        # KB: [2013-02-24]: products are passed as products[$product_id] = quantity
        product_ids = {}
        for key in self.request.POST.keys():
            if key.startswith('products'):
                match = re.search(r'^.*\[(.*)\]', key)
                if match:
                    pid = match.group(1)
                    quant = float(util.nvl(self.request.POST.get(key), '1.0'))
                    if pid not in product_ids:
                        product_ids[pid] = 0
                    product_ids[pid] += quant


        # KB: [2013-02-24]: attributes are passed as attributes[$attribute_id] = $parent_product_id
        attributes = {}
        for key in self.request.POST.keys():
            if key.startswith('attributes'):
                match = re.search(r'^.*\[(.*)\]', key)
                if match:
                    attribute_product_id = match.group(1)
                    parent_product_id = self.request.POST.get(key)
                    attributes[attribute_product_id] = { 'parent_product' : Product.load(parent_product_id),
                                                         'attribute_product' : Product.load(attribute_product_id) }

        order_id = self._add_order_impl(customer_id, product_ids, attributes,
                                        None, self.request.ctx.user,
                                        self.request.POST.get('discount_id'),
                                        self.request.POST.get('campaign_id', self.request.GET.get('campaign_id')),
                                        self.incl_tax)
        cust.invalidate_caches()
        return str(order_id)


    @property
    def incl_tax(self):
        return int(self.request.POST.get('incl_tax', self.request.GET.get('incl_tax', 1)))


    @view_config(route_name='crm.customer.edit_order_dialog', renderer='/crm/customer.edit_order.mako')
    @authorize(IsLoggedIn())
    def edit_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        return {
            'customer' : customer,
            'order' : order,
            'comm_packing_slip_id' : order.campaign.comm_packing_slip_id,
            'total_price' : order.total_price(),
            'total_item_price' : order.total_item_price(),
            'total_handling_price' : order.total_handling_price(),
            'total_shipping_price' : order.total_shipping_price(),
            'total_payments_applied' : order.total_payments_applied(),
            'total_discounts_applied' : order.total_discounts_applied(),
            'total_due' : order.total_payments_due()
            }


    @view_config(route_name='crm.customer.return_item_dialog', renderer='/crm/customer.return_item.mako')
    @authorize(IsLoggedIn())
    def return_item_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        order_item_id = self.request.matchdict.get('order_item_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        order_item = OrderItem.load(order_item_id)
        self.forbid_if(not order_item or str(order_item.order.order_id) != str(order.order_id))
        return {
            'customer' : customer,
            'order' : order,
            'order_item' : order_item
            }


    @view_config(route_name='crm.customer.return_item', renderer='string')
    @authorize(IsLoggedIn())
    def return_item(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        order_item_id = self.request.matchdict.get('order_item_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        order_item = OrderItem.load(order_item_id)
        self.forbid_if(not order_item or str(order_item.order.order_id) != str(order.order_id))
        user = self.request.ctx.user
        return_type = self.request.POST.get('rt_refund_type')
        quantity_returned = float(self.request.POST.get('quantity_returned'))
        credit_amount = float(self.request.POST.get('credit_amount'))

        jrnl = Journal.create_new(credit_amount, customer, order, user, return_type)
        ret = ProductReturn.create_new(order_item.product, order_item.order, quantity_returned, credit_amount, jrnl, user)
        status_note = "'%s' returned.  $%.2f refunded by %s" % (order_item.product.name, credit_amount, return_type)
        Status.add(customer, order_item, Status.find_event(self.enterprise_id, order_item, 'RETURN'), status_note)

        order_item.quantity -= quantity_returned
        if order_item.quantity == 0:
            order_item.delete_dt = util.today()
        order_item.save()
        if order_item.product.track_inventory:
            InventoryJournal.create_new(order_item.product, 'Return', quantity_returned, order_item, None, None, ret)

        for attr_kid in order_item.children:
            Status.add(customer, attr_kid, Status.find_event(self.enterprise_id, attr_kid, 'RETURN'), status_note)
            attr_kid_prod = attr_kid.product
            if attr_kid_prod.track_inventory:
                InventoryJournal.create_new(attr_kid_prod, 'Return', quantity_returned, attr_kid)

        self.flash(status_note)
        if len(order.active_items) == 0:
            # KB: [2012-09-06]: Deleted the one thing out of this
            # order.  Kill the order
            status_note = 'Only item in order returned. Order cancelled.'
            self._cancel_order_impl(order_id, status_note, False)
            self.flash(status_note)
            ret = HTTPFound('/crm/customer/show_orders/%s' % customer_id)
        else:
            ret = HTTPFound('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))
        customer.invalidate_caches()
        return ret


    @view_config(route_name='crm.customer.apply_payment_dialog', renderer='/crm/customer.apply_payment.mako')
    @authorize(IsLoggedIn())
    def apply_payment_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        total_due = order.total_payments_due()
        pre_order_balance = customer.get_current_balance()
        return {
            'customer' : customer,
            'order' : order,
            'total_price' : order.total_price(),
            'payment_methods' : Journal.get_payment_methods(self.request.ctx.enterprise),
            'total_payments_applied' : order.total_payments_applied(),
            'total_discounts_applied' : order.total_discounts_applied(),
            'total_due' : total_due,
            'pre_order_balance' : pre_order_balance,
            'enterprise' : self.request.ctx.enterprise,
            'total_due_after_balance' : total_due+pre_order_balance if (total_due+pre_order_balance) > 0 else 0
            }


    @view_config(route_name='crm.customer.apply_payment')
    @authorize(IsLoggedIn())
    def apply_payment(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        if 'bill_cc_token' in self.request.POST and self.request.POST['bill_cc_token']:
            cust = Customer.load(customer_id)
            order = CustomerOrder.load(order_id)
            bill = self._create_billing(cust)
            self._bill_credit_card(cust, order, bill)
        else:
            self._apply_payment(customer_id, order_id)
        return HTTPFound('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))


    def _apply_payment(self, customer_id, order_id, pmt_amount=None, pmt_method=None, pmt_note=None):  #pylint: disable-msg=R0913
        """ KB: [2011-03-09]: Check that everything is kosher
        Create a journal entry for the order for the amount and type specified in the UI
        Create a status noting the type and amount of the payment applied.
        """
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        user = self.request.ctx.user
        current_customer_balance = customer.get_current_balance()
        #prior_payments_applied = order.total_payments_applied()
        prior_total_due = order.total_payments_due()
        balance_amount_to_apply = float(self.request.POST.get('pmt_balance_amount_to_apply', 0.0))
        amt = float(util.nvl(pmt_amount, self.request.POST.get('pmt_amount')))
        method = util.nvl(pmt_method, self.request.POST.get('pmt_method'))
        note = util.nvl(pmt_note, self.request.POST.get('pmt_note'))

        self.forbid_if(round(amt + balance_amount_to_apply, 2) > round(prior_total_due, 2),
                       "amt + balance_amount_to_apply > prior_total_due")
        self.forbid_if(current_customer_balance > 0 and round(balance_amount_to_apply, 2) > round(current_customer_balance, 2),
                       "balance_amount_to_apply > current_customer_balance")

        pmt_type = 'PartialPayment'
        if amt == prior_total_due:
            pmt_type = 'FullPayment'

        Journal.create_new(amt, customer, order, user, pmt_type, method, note)
        status_note = '%s applied: $%s' % (pmt_type, util.money(amt))
        Status.add(customer, order, Status.find_event(self.enterprise_id, order, 'PAYMENT_APPLIED'), status_note)
        self.flash(status_note)
        if balance_amount_to_apply > 0:
            Journal.create_new(balance_amount_to_apply, customer, order, user, 'CreditDecrease')
            status_note = '%s applied: $%s' % ('CreditDecrease', util.money(balance_amount_to_apply))
            Status.add(customer, order, Status.find_event(self.enterprise_id, order, 'PAYMENT_APPLIED'), status_note)
            self.flash(status_note)
        customer.invalidate_caches()
        customer.flush()
        return 'True'


    @view_config(route_name='crm.customer.edit_order', renderer='string')
    @authorize(IsLoggedIn())
    def edit_order(self):   #pylint: disable-msg=R0915,R0912
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        oids_to_delete = self.request.POST.getall('order_items_to_delete[]')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        order.shipping_total = self.request.POST.get('shipping_total') if self.request.POST.get('shipping_total') else 0.0
        order.create_dt = self.request.POST.get('create_dt') if self.request.POST.get('create_dt') else order.create_dt
        order.save()

        total_payments_applied = order.total_payments_applied()

        for oid in oids_to_delete:
            oitem = OrderItem.load(oid)
            Status.add(customer, oitem, Status.find_event(self.enterprise_id, oitem, 'DELETED'), 'OrderItem deleted ')
            prod = oitem.product
            if prod.track_inventory:
                InventoryJournal.create_new(prod, 'Cancelled Item', oitem.quantity, oitem)
            for attr_kid in oitem.children:
                Status.add(customer, attr_kid, Status.find_event(self.enterprise_id, attr_kid, 'DELETED'), 'OrderItem deleted ')
                attr_kid_prod = attr_kid.product
                if attr_kid_prod.track_inventory:
                    InventoryJournal.create_new(attr_kid_prod, 'Cancelled Item', oitem.quantity, attr_kid)
                attr_kid.soft_delete()
            oitem.soft_delete()                

        # extract order_items[27][quantity] to set those properties.
        order_items = {}
        for key in self.request.POST.keys():
            if key.startswith('order_items'):
                match = re.search(r'^.*\[(.*)\]\[(.*)\]', key)
                if match:
                    order_item_id = match.group(1)
                    attr = match.group(2)
                    new_val = float(self.request.POST.get(key)) if attr != 'product_id' else self.request.POST.get(key)
                    # KB: [2011-03-07]: If the ID ends in '_', its not really an ID but a new item.
                    # product_id will only show up as non-null in the hash of a new product
                    if order_item_id[-1] == '_':
                        order_item_product = Product.load(self.request.POST.get('order_items[%s][product_id]' % order_item_id))
                        if not order_items.has_key(order_item_id):
                            order_items[order_item_id] = order.augment_order(customer,
                                                                             order_item_product,
                                                                             customer.campaign,
                                                                             self.request.ctx.user)
                        oitem = order_items[order_item_id]
                        assert oitem.product is not None
                        if 'quantity' == attr:
                            new_val = float(new_val)
                            if order_item_product.track_inventory:
                                InventoryJournal.create_new(order_item_product, 'Sale', new_val, oitem)
                        setattr(oitem, attr, new_val)
                        oitem.save()
                    else:
                        if not order_items.has_key(order_item_id):
                            order_items[order_item_id] = OrderItem.load(order_item_id)
                        oitem = order_items[order_item_id]
                        order_item_product = oitem.product

                        if util.money(getattr(oitem, attr)) != util.money(new_val):
                            Status.add(customer, oitem, Status.find_event(self.enterprise_id, oitem, 'MODIFIED'),
                                       'Order Item modified: (id=%s). %s : %s -> %s' % (oitem.order_item_id, attr, util.money(getattr(oitem, attr)), util.money(new_val)))
                        if 'quantity' == attr:
                            new_val = float(new_val)
                            if not total_payments_applied:
                                if order_item_product.track_inventory:
                                    InventoryJournal.cleanup(oitem, 'Sale')
                                    InventoryJournal.create_new(order_item_product, 'Sale', new_val, oitem)
                        setattr(oitem, attr, new_val)
                        oitem.save()
        Status.add(customer, order, Status.find_event(self.enterprise_id, order, 'MODIFIED'), 'Order modified')
        customer.invalidate_caches()
        self.flash("Saved Order")
        return 'True'


    @view_config(route_name='crm.customer.show_status_dialog', renderer='/crm/customer.view_status.mako')
    @authorize(IsLoggedIn())
    def show_status_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        status_id = self.request.matchdict.get('status_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        status = Status.load(status_id)
        self.forbid_if(not status or str(customer.customer_id) != str(customer_id))
        return {
            'customer' : customer,
            'status' : status
            }


    @view_config(route_name='crm.customer.status_dialog', renderer='/crm/customer.status.mako')
    @authorize(IsLoggedIn())
    def status_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = order_item = events = redir = None
        if self.request.GET.get('order_id'):
            order = CustomerOrder.load(self.request.GET.get('order_id'))
            self.forbid_if(not order or order.campaign.company.enterprise_id != self.enterprise_id)
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, order), 'event_id', 'display_name', True)
            redir = '/crm/customer/show_orders/%s' % customer_id
        elif self.request.GET.get('order_item_id'):
            order_item = OrderItem.load(self.request.GET.get('order_item_id'))
            self.forbid_if(not order_item or order_item.order.campaign.company.enterprise_id != self.enterprise_id)
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, order_item), 'event_id', 'display_name', True)
            redir = '/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_item.order_id)
        else:
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, customer), 'event_id', 'display_name', True)
            redir = '/crm/customer/edit/%s' % customer_id
        return {
            'customer' : customer,
            'order' : order,
            'order_item' : order_item,
            'events' : events,
            'redir' : redir
            }


    @view_config(route_name='crm.customer.save_status')
    @authorize(IsLoggedIn())
    def save_status(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        event = StatusEvent.load(self.request.POST.get('event_id'))
        self.forbid_if(not event or not self.request.POST.get('event_id') or (not event.is_system and event.enterprise_id is not None and event.enterprise_id != self.enterprise_id))
        order = None
        note = self.request.POST.get('note')
        if self.request.POST.get('order_id'):
            order = CustomerOrder.load(self.request.POST.get('order_id'))
            self.forbid_if(not order or order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order, event, note, self.request.ctx.user)
            self.flash('Statused Order to %s' % event.display_name)
        elif self.request.POST.get('order_item_id'):
            order_item = OrderItem.load(self.request.POST.get('order_item_id'))
            self.forbid_if(not order_item or order_item.order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order_item, event, note, self.request.ctx.user)
            self.flash('Statused Item to %s' % event.display_name)
        else:
            Status.add(customer, customer, event, note, self.request.ctx.user)
            self.flash('Statused Customer to %s' % event.display_name)
        customer.invalidate_caches()
        return self.find_redirect()


    @view_config(route_name='crm.customer.delete', renderer='string')
    @authorize(IsLoggedIn())
    def delete(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        customer.mod_dt = util.now()
        customer.delete_dt = util.now()
        Status.add(customer, customer, StatusEvent.find(self.enterprise_id, 'Customer', 'DELETED'), 'Customer Deleted')
        return 'True'


    @view_config(route_name='crm.customer.check_duplicate_email', renderer='string')
    def check_duplicate_email(self):
        email = self.request.matchdict.get('email')
        cust = Customer.find(email, self.request.ctx.site.company)
        return 'True' if cust else 'False'


    def _prep_add_order_dialog(self, customer_id):
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        products = Product.find_by_campaign(customer.campaign)
        return {
            'customer' : customer,
            'products' : products
            }


    def _add_order_impl(self, customer_id, product_ids, attributes, prices, user, discount_id, campaign_id, incl_tax=True):   #pylint: disable-msg=R0913
        """ KB: [2013-02-20]:
        attributes = [{quantity : 0, product : <Product...>}, {...}]
        """
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        cart = Cart()
        campaign_id = campaign_id if campaign_id else cust.campaign_id
        cart.discount_id = discount_id
        for pid in product_ids.keys():
            quantity = product_ids[pid]
            price = prices[pid] if prices and pid in prices else None
            attrs = {}
            for attr in [attr['attribute_product'] for attr in attributes.values() if str(attr['parent_product'].product_id) == pid]:
                attrs[attr.product_id] = { 'quantity' : 0,
                                           'product' : attr}
            cart.add_item(product=Product.load(pid),
                          campaign=cust.campaign,
                          quantity=quantity,
                          attributes=attrs,
                          base_price=price)
        order = cust.add_order(cart, user, self.enterprise_id, cust.campaign, incl_tax)
        order.flush()
        return order.order_id


    @view_config(route_name='crm.customer.purchase_cart')
    def purchase_cart(self):
        self.forbid_if(not self.request.ctx.customer or 'cart' not in self.session or not self.session['cart'])
        cust = self.request.ctx.customer
        cart = self.session['cart']
        order = self._site_purchase(cust, self.session['cart'])
        cart.remove_all()
        return self.find_redirect("?order_id=%s" % order.order_id)


    @view_config(route_name='crm.customer.signup')
    def signup(self):
        cust = self._signup()
        if cust:
            self.flash('Customer created: %s %s' % (cust.fname, cust.lname))
            return self.find_redirect('?customer_id=' + str(cust.customer_id))


    @validate((('fname', 'string'), ('fname', 'required'),
              ('lname', 'string'), ('lname', 'required'),
              ('email', 'string'), ('email', 'required'),
              ('password', 'required'), ('confirmpassword', 'required')
              ))
    def _signup(self):
        """ KB: [2011-04-26]:
        Customer can't exist.  Fail if there is a customer_id param
        The customer should never be able to get here if he's logged in.  Forbid if there is a self.session open.
        Try to find the customer by the email provided.
        - If found by email, redirect back to the calling page (POST['url_path'] with msg = already_exists
        Save the customer object and store in the self.session as though the customer has logged in.

        If something goes wrong, redirect back to the calling page with msg = signup_failed
        """
        self.forbid_if(self.request.POST.get('customer_id') or self.request.ctx.customer or not self.request.ctx.campaign)
        campaign = self.request.ctx.campaign
        cust = Customer.find(self.request.POST.get('email'), campaign)
        if cust:
            self.flash('Email %s already in use' % cust.email)
            self.raise_redirect(self.request.referrer)
        cust = Customer()
        cust.campaign_id = campaign.campaign_id
        cust.bind(self.request.POST)
        cust.save()
        cust.flush()
        self.session['customer_id'] = cust.customer_id
        cust.invalidate_caches()
        return cust


    @view_config(route_name='crm.customer.save_and_purchase')
    @validate((('customer_id', 'required')))
    def save_and_purchase(self):
        """ KB: [2012-02-05]: Useful for multi-step signup processes where the
        customer is saved after step 1, and at the end you buy something. """
        self.forbid_if(not self.request.ctx.customer)
        cust = self._save(self.request.ctx.customer.customer_id, False) # don't let it redirect
        self._site_purchase(cust)
        return HTTPFound(util.nvl(self.request.POST.get('redir'), '/') + '?customer_id=' + str(cust.customer_id)) #pylint: disable-msg=E1103


    def _create_billing(self, cust):
        bill = Billing.create(cust)
        bill.set_cc_info(self.request.POST.get('bill_cc_num'), self.request.POST.get('bill_cc_cvv'))
        bill.cc_exp = self.request.POST.get('bill_cc_exp')
        bill.cc_token = self.request.POST.get('bill_cc_token')
        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')
        bill.bind(self.request.POST, False, 'bill')
        cust.billing = bill
        cust.save()
        bill.save()
        return bill


    def _site_purchase(self, cust, cart=None):  #pylint: disable-msg=R0912,R0915
        """ KB: [2013-02-20]: MOD ATTR CustomerController._site_purchase : Allow for attributes passed in the post """
        bill = self._create_billing(cust)
        campaign = Campaign.load(cust.campaign_id)

        if not cart:
            cart = Cart()
            product_skus = self.request.POST.getall('product_sku')
            for sku in product_skus:
                prod = Product.find_by_sku(self.enterprise_id, campaign, sku)
                if prod:
                    cart.add_item(product=prod,
                                  campaign=cust.campaign,
                                  start_dt=self.request.POST.get('bill_start_dt')
                                  )
                else:
                    self.flash("No such product sku: %s" % sku)
                    self.raise_redirect(self.request.referrer)

        order = cust.add_order(cart, None, self.enterprise_id, campaign)
        return self._bill_credit_card(cust, order, bill)


    def _bill_credit_card(self, cust, order, bill):
        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        api.set_coupon(self.request.POST.get('coupon_code'))
        if api.purchase(order, bill, util.request_ip(self.request)):
            # accept terms if they sent accept_terms as positive across (checkbox)
            if ('accept_terms' in self.request.POST and self.request.POST['accept_terms'] == '1'):
                accept = OrderItemTermsAcceptance()
                accept.order_id = order.order_id
                accept.signature = cust.email
                accept.save()
                accept.flush()

            self._apply_payment(cust.customer_id, order.order_id, order.total_price(), api.payment_method)
            try:
                order.campaign.send_post_purchase_comm(order)
            except Exception as exc:  #pragma: no cover
                log.exception(exc)
            return order
        else:
            (_, last_note) = api.get_last_status()
            self.flash('Unable to bill credit card: %s' % last_note)
            log.error('CC DECLINED %s %s %s' % (cust.customer_id, cust.email, last_note))
            self.raise_redirect(self.request.referrer)


    @view_config(route_name='crm.customer.self_save')
    @authorize(IsCustomerLoggedIn())
    def self_save(self):
        # if they didn't provide a password, don't record blank.
        if self.request.POST.get('password') in (None, ''):
            del self.request.POST['password']
        # fix this.  double lookup of customer is lame.
        return self._save(self.request.ctx.customer.customer_id)


    @view_config(route_name='crm.customer.self_save_billing')
    @authorize(IsCustomerLoggedIn())
    def self_save_billing(self):
        cust = self.request.ctx.customer
        self.forbid_if(cust.campaign.company.enterprise_id != self.enterprise_id)
        bill = cust.billing
        if not bill:
            bill = Billing.create(cust, True)

        bill.set_cc_info(self.request.POST.get('bill_cc_num'), self.request.POST.get('bill_cc_cvv'))
        bill.cc_exp = self.request.POST.get('bill_cc_exp')
        bill.cc_token = self.request.POST.get('bill_cc_token')
        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')

        bill.bind(self.request.POST, False, 'bill')
        bill.save()
        cust.save()
        self.db_flush()
        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        if api.update_billing(cust, bill):
            Status.add(cust, cust, Status.find_event(self.enterprise_id, cust, 'NOTE'),
                       'Billing Updated at gateway')
            self.flash('Successfully saved billing information.')
            cust.invalidate_caches()
            return self.find_redirect()
        else:
            (_, last_note) = api.get_last_status()
            self.flash('Unable to save credit card information: %s' % last_note)
            log.error('CC CHANGE DECLINED %s %s %s' % (cust.customer_id, cust.email, last_note))
            self.raise_redirect(self.request.referrer)


    @view_config(route_name='crm.customer.self_cancel_order')
    @authorize(IsCustomerLoggedIn())
    def self_cancel_order(self):
        """ KB: [2011-04-07]: If the order id is specified, then cancel that order, otherwise, cancel every active order.
        User has to specify user_id and password to confirm cancellation.
        """
        cust = self.request.ctx.customer
        self.forbid_if(cust.campaign.company.enterprise_id != self.enterprise_id)
        self.forbid_if('username' not in self.request.POST or 'password' not in self.request.POST)

        if not cust.authenticate(self.request.POST.get('username'), self.request.POST.get('password'), cust.campaign.company):
            self.flash('Username or password incorrect.  Unable to cancel.')
            self.raise_redirect()

        if self.request.POST.get('order_id'):
            self._cancel_order_impl(self.request.POST.get('order_id'),
                                    None, True)
        else:
            for cord in cust.get_active_orders():
                self._cancel_order_impl(cord.order_id,
                                        None, True)
        self.flash('Order cancelled.')
        cust.invalidate_caches()
        cust.campaign.send_post_cancel_comm(cust)
        return self.find_redirect()


    @view_config(route_name='crm.customer.get_balance', renderer='string')
    @authorize(IsLoggedIn())
    def get_balance(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return str(customer.get_current_balance())


    @view_config(route_name='crm.customer.self_get_balance', renderer='string')
    @authorize(IsCustomerLoggedIn())
    def self_get_balance(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or str(self.request.ctx.customer.customer_id) != str(customer_id) or customer.campaign.company.enterprise_id != self.enterprise_id)
        return str(customer.get_current_balance())


    @view_config(route_name='crm.customer.contact')
    def contact(self):
        camp = self.request.ctx.campaign
        message = self.request.POST.get('message')
        email = self.request.POST.get('email')
        msg = "%s %s<br>(%s)<br><br>%s<br><br>%s" % (self.request.POST.get('fname'),
                                                     self.request.POST.get('lname'),
                                                     email,
                                                     self.request.POST.get('phone'),
                                                     message)
        if util.nvl(self.request.POST.get('save')):
            cust = Customer.find(email, camp)
            if not cust:
                cust = Customer()
                cust.campaign = camp
                cust.bind(self.request.POST)
                cust.phone = cust.phone[:20] if cust.phone else None # prevents people from putting in "904-716-7487 (mobile)" and it barfs
                cust.save()
            Status.add(cust, cust, Status.find_event(self.enterprise_id, cust, 'NOTE'),
                       'NOTE FROM CUSTOMER\n%s' % message)

        email_info = camp.get_email_info()
        mail = UserMail(camp)
        mail.send(email_info.email, 'SITE CONTACT FORM %s' % self.request.host, msg)
        return self.find_redirect()


    @view_config(route_name='crm.customer.signup_and_purchase')
    def signup_and_purchase(self):
        cust = self._signup()
        if not cust:
            return HTTPFound('{url}?msg=signup_failed' % self.request.referrer)
        self._site_purchase(cust)
        return self.find_redirect('?customer_id=' + str(cust.customer_id))


#    def signup_free(self):
#        """ KB: [2011-04-26]:
#        Sign up just like in self.signup.
#        Add the product ID's to the cart.
#        Add a real order and save everything
#        - Products are whatever free thing is being offered.
#        - Don't create billing because this thing is free.
#        Send the customer the post_purchase comm as configured for the campaign.
#        Redirect to POST['redir']
#        """
#        if not self._signup():
#            return HTTPFound(url('{url}?msg=signup_failed'.format(url=self.request.POST.get('url_path'))))
#
#        product_ids = self.request.POST.getall('prod_product_id')
#        cust = Customer.load(self.session['customer_id'])
#        cart = Cart()
#        for id in product_ids:
#            cart.add_item(Product.load(id), cust.campaign_id)
#
#        campaign = Campaign.load(cust.campaign_id)
#        order = cust.add_order(cart,
#                               None,
#                               Site.load(self.session['site_id']),
#                               campaign)
#        self.db_commit()
#        campaign.send_post_purchase_comm(order)
#        return HTTPFound(self.request.POST.get('redir'))
#

#    def cc_response_handler(self, api, response_dict, history_record, order, billing):
#        """ KB: [2010-10-20]: Callback for handling the API when it's completed processing. """
#        if api.is_declined(response_dict):
#            Status.add(order.customer, order, Status.find_event(self.enterprise_id, order, 'BILLING_DECLINED'),
#                       'Billing Declined: %s' % history_record.notes).flush()
#            return False
#        else:
#            Status.add(order.customer, order, Status.find_event(self.enterprise_id, order, 'BILLING_SUCCESS'),
#                       'Billing Succeeded: %s' % history_record.notes).flush()
#            j = Journal.create_new(order.total_payments_due(), order.customer, order, None,
#                                   'FullPayment', 'Credit Card', None)
#            if j:
#                j.flush()
#            return True

    # @view_config(route_name='crm.customer.show_summary', renderer='/crm/customer.summary_report.mako')
    # @authorize(IsLoggedIn())
    # def show_summary(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     customer = Customer.load(customer_id)
    #     self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
    #     today = util.today()
    #     start_dt = util.parse_date(self.request.GET.get('start_dt') if self.request.GET.get('start_dt') else '%s-01-01' % today.year)
    #     end_dt = util.parse_date(self.request.GET.get('end_dt') if self.request.GET.get('end_dt') else util.format_date(today))
    #     return {
    #         'start_dt' : start_dt,
    #         'end_dt' : end_dt,
    #         'customer' : customer,
    #         'orders' : CustomerOrder.find_by_customer(customer, None, start_dt, end_dt)
    #         }

    # @authorize(IsCustomerLoggedIn())
    # @validate((('password', 'required'),
    #            ('confirmpassword', 'required')))
    # def self_change_password(self):
    #     """ KB: [2012-01-31]: Called from end site customer self-edit section. """
    #     self.forbid_if('customer_id' not in self.session)
    #     cust = Customer.load(self.session['customer_id'])
    #     self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)

    #     cust.password = self.request.POST.get('password')
    #     cust.save()
    #     self.flash('Password changed.')
    #     if self.request.POST.get('redir'):
    #         return HTTPFound(self.request.POST.get('redir'))
    #     else:
    #         return HTTPFound(self.request.referrer)



    # @view_config(route_name='crm.customer.edit_billing_dialog', renderer='/crm/customer.edit_billing.mako')
    # @authorize(IsLoggedIn())
    # def edit_billing_dialog(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     customer = Customer.load(customer_id)
    #     self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
    #     if not customer.billing:
    #         customer.billing = Billing.create(customer, False)
    #     billing_types = Billing.get_billing_types()
    #     return {
    #         'customer' : customer,
    #         'billing_types' : billing_types
    #         }


    # @view_config(route_name='crm.customer.edit_billing', renderer='string')
    # @authorize(IsLoggedIn())
    # def edit_billing(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     cust = Customer.load(customer_id)
    #     self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
    #     if not cust.billing:
    #         cust.billing = Billing.create(cust)
    #         cust.billing.user_created = self.request.ctx.user
    #     if self.request.POST.has_key('cc_num'):
    #         cust.billing._cc_num = self.request.POST.get('cc_num')
    #     cust.billing.bind(self.request.POST)
    #     cust.billing.save()
    #     return 'True'


    # @view_config(route_name='crm.customer.cancel_billing', renderer='string')
    # @authorize(IsLoggedIn())
    # def cancel_billing(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     journal_id = self.request.matchdict.get('journal_id')
    #     cust = Customer.load(customer_id)
    #     self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
    #     jrnl = Journal.load(journal_id)
    #     self.forbid_if(not jrnl or jrnl.customer_id != cust.customer_id)
    #     jrnl.cancel()
    #     self.flash('Billing record cancelled.')
    #     return HTTPFound('/crm/customer/show_billings/%s' % cust.customer_id)


    # @view_config(route_name='crm.customer.add_order_and_apply', renderer='string')
    # @authorize(IsLoggedIn())
    # def add_order_and_apply(self):
    #     """ KB: [2011-10-21]:
    #     If an email thats not POS@ was specified, then send them a receipt.
    #     otherwise, just save it and move on to the next order.
    #     """
    #     customer_id = self.request.matchdict.get('customer_id')
    #     pmt_method = self.request.matchdict.get('pmt_method')
    #     email = self.request.GET.get('email')
    #     cust = None
    #     if email:
    #         campaign = Campaign.load(self.request.GET.get('campaign_id'))
    #         cust = Customer.find(email, campaign)
    #         if not cust:
    #             cust = Customer()
    #             cust.campaign = campaign
    #         cust.email = email
    #         cust.save()
    #         cust.flush()
    #         customer_id = cust.customer_id
    #     order_id = self.add_order(customer_id, False)
    #     self.forbid_if(not order_id)
    #     order = CustomerOrder.load(order_id)
    #     self.forbid_if(not order)
    #     ret = self.apply_payment(customer_id, order_id, 'FullPayment', pmt_method, order.total_price())
    #     if cust:
    #         cust.campaign.send_post_purchase_comm(order)
    #     return ret


    # @view_config(route_name='crm.customer.add_order_item_dialog', renderer='/crm/customer.add_order_item.mako')
    # @authorize(IsLoggedIn())
    # def add_order_item_dialog(self):
    #     customer_id = self.request.matchdict.get('customer_id')
    #     return self._prep_add_order_dialog(customer_id)
