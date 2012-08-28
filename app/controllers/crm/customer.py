import logging, re, pdb
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.validate import validate
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn, IsCustomerLoggedIn
from app.model.core.users import Users
from app.model.crm.customer import Customer
from app.model.crm.billing import Billing
from app.model.crm.product import Product, ProductReturn, InventoryJournal
from app.model.crm.campaign import Campaign
from app.model.crm.journal import Journal
from app.model.crm.customerorder import CustomerOrder
from app.model.crm.orderitem import OrderItem, OrderItemTermsAcceptance
from app.model.core.status import Status
from app.model.core.statusevent import StatusEvent
from app.model.cms.site import Site
import simplejson as json
import app.lib.util as util
from app.model.crm.company import Company
from app.lib.billing_api import BaseBillingApi

log = logging.getLogger(__name__)

class CustomerController(BaseController):
    @view_config(route_name='crm.customer.edit', renderer='/crm/customer.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name='crm.customer.new', renderer='/crm/customer.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    def _edit_impl(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = None
        if customer_id:
            customer = Customer.load(customer_id)
            self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        else:
            customer = Customer()
            customer.campaign = self.request.ctx.site.company.get_default_campaign()
        return {
            'customer' : customer,
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
        username = self.request.ctx.user.username
        kv_map = self.request.POST
        cust = Customer.load(customer_id)
        if not cust:
            cust = Customer()
            cust.user_created = cust.user_assigned = username
        else:
            self.forbid_if(cust.campaign.company.enterprise_id != self.enterprise_id)
        cust.bind(kv_map)
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
    def autocomplete(self):
        if not 'search_key' in self.request.GET or not self.request.GET.get('search_key'): return
        q = self.request.GET.get('search_key')
        lnames = Customer.find_last_names_autocomplete(self.enterprise_id, q, self.request.GET.get('limit', 10))
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
            'external_cart_id' : None,
            'customers' : None
            }


    @view_config(route_name='crm.customer.search', renderer='/crm/customer.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        external_cart_id = self.request.POST.get('external_cart_id', self.request.GET.get('external_cart_id'))
        ret = {
            'company_name' : None,
            'fname' : None,
            'lname' : None,
            'email' : None,
            'phone' : None,
            'external_cart_id' : external_cart_id,
            'customers' : None
            }

        if not external_cart_id:
            ret['company_name'] = self.request.POST.get('company_name', self.request.GET.get('company_name'))
            ret['fname'] = self.request.POST.get('fname', self.request.GET.get('fname'))
            ret['lname'] = self.request.POST.get('lname', self.request.GET.get('lname'))
            ret['email'] = self.request.POST.get('email', self.request.GET.get('email'))
            ret['phone'] = self.request.POST.get('phone', self.request.GET.get('phone'))
            ret['customers'] = Customer.search(self.enterprise_id, ret['company_name'], ret['fname'], ret['lname'], ret['email'], ret['phone'])
        else:
            order = CustomerOrder.find_by_external_cart_id(external_cart_id)
            if order:
                ret['customers'] = [order.customer]

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
            'orders' : CustomerOrder.find_by_customer(customer)
            }


    @view_config(route_name='crm.customer.show_summary', renderer='/crm/customer.summary_report.mako')
    @authorize(IsLoggedIn())
    def show_summary(self):
        customer_id = self.request.matchdict.get('customer_id')
        today = util.today()
        start_dt = util.parse_date(self.request.GET.get('start_dt') if self.request.GET.get('start_dt') else '%s-01-01' % today.year)
        end_dt = util.parse_date(self.request.GET.get('end_dt') if self.request.GET.get('end_dt') else util.format_date(today))
        return {
            'start_dt' : start_dt,
            'end_dt' : end_dt,
            'orders' : CustomerOrder.find_by_customer(customer, None, start_dt, end_dt)
            }


    @view_config(route_name='crm.customer.show_history', renderer='/crm/customer.history_list.mako')
    @authorize(IsLoggedIn())
    def show_history(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'customer' : customer,
            'history' : Status.find_by_customer(customer),
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
            'billings' : Journal.find_all_by_customer(customer),
            'offset' : self.offset
            }


    @view_config(route_name='crm.customer.edit_billing_dialog', renderer='/crm/customer.edit_billing.mako')
    @authorize(IsLoggedIn())
    def edit_billing_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        if not c.customer.billing:
            b = Billing.create(customer, False)
        billing_types = Billing.get_billing_types()
        return {
            'customer' : customer,
            'billing_types' : billing_types
            }

    @view_config(route_name='crm.customer.edit_billing', renderer='string')
    @authorize(IsLoggedIn())
    def edit_billing(self):
        customer_id = self.request.matchdict.get('customer_id')
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        if not cust.billing:
            cust.billing = Billing.create(cust)
            if user:
                cust.billing.user_created = user.username
        if kv_map.has_key('cc_num'):
            cust.billing._cc_num = kv_map['cc_num']
        cust.billing.bind(kv_map)
        cust.billing.save()
        return 'True'


    @view_config(route_name='crm.customer.cancel_order', renderer='string')
    @authorize(IsLoggedIn())    
    def cancel_order(self):
        customer_id = self.request.matchdict.get('customer_id')
        self._cancel_order_impl(customer_id,
                                self.request.POST.get('order_id'),
                                self.request.POST.get('cancel_reason'),
                                False)
        return 'True'


    @view_config(route_name='crm.customer.cancel_billing', renderer='string')
    @authorize(IsLoggedIn())
    def cancel_billing(self):
        customer_id = self.request.matchdict.get('customer_id')
        journal_id = self.request.matchdict.get('journal_id')
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        j = Journal.load(journal_id)
        self.forbid_if(not j or j.customer_id != cust.customer_id)
        j.cancel()
        return 'True'


    @view_config(route_name='crm.customer.add_order_dialog', renderer='/crm/customer.add_order.mako')
    @authorize(IsLoggedIn())
    def add_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        return self._prep_add_order_dialog(customer_id)


    """ KB: [2011-10-21]:
    If an email thats not POS@ was specified, then send them a receipt.
    otherwise, just save it and move on to the next order.
    """
    @view_config(route_name='crm.customer.add_order_and_apply', renderer='string')
    @authorize(IsLoggedIn())
    def add_order_and_apply(self):
        customer_id = self.request.matchdict.get('customer_id')
        pmt_method = self.request.matchdict.get('pmt_method')
        email = self.request.GET.get('email')
        cust = None
        if email:
            campaign = Campaign.load(self.request.GET.get('campaign_id'))
            cust = Customer.find(email, campaign)
            if not cust:
                cust = Customer()
                cust.campaign = campaign
            cust.email = email
            cust.save()
            cust.flush()
            customer_id = cust.customer_id
        order_id = self.add_order(customer_id, False)
        self.forbid_if(not order_id)
        order = CustomerOrder.load(order_id)
        self.forbid_if(not order)
        ret = self.apply_payment(customer_id, order_id, 'FullPayment', pmt_method, order.total_price())
        if cust:
            cust.campaign.send_post_purchase_comm(order)
        return ret


    @view_config(route_name='crm.customer.add_order', renderer='string')
    @authorize(IsLoggedIn())
    def add_order(self):
        customer_id = self.request.matchdict.get('customer_id')
        product_ids = {}
        for k in self.request.POST.keys():
            if k.startswith('products'):
                m = re.search(r'^.*\[(.*)\]', k)
                if m:
                    pid = m.group(1)
                    quant = float(self.request.POST.get(k))
                    if pid in product_ids:
                        product_ids[pid] += quant
                    else:
                        product_ids[pid] = quant

        order_id = self._add_order_impl(customer_id, product_ids,
                                        None, self.request.ctx.user,
                                        self.request.POST.get('discount_id'),
                                        self.request.POST.get('campaign_id', self.request.GET.get('campaign_id')),
                                        self.incl_tax)
        return str(order_id)

    @property
    def incl_tax(self):
        incl_tax = 1
        if 'incl_tax' in self.request.POST or 'incl_tax' in self.request.GET:
            incl_tax = int(self.request.POST.get('incl_tax', self.request.GET.get('incl_tax', 1)))
        return incl_tax


    @view_config(route_name='crm.customer.add_order_item_dialog', renderer='/crm/customer.add_order_item.mako')
    @authorize(IsLoggedIn())
    def add_order_item_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        return self._prep_add_order_dialog(customer_id)


    @view_config(route_name='crm.customer.edit_order_dialog', renderer='/crm/customer.edit_order.mako')
    @authorize(IsLoggedIn())
    def edit_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        return {
            'order' : order,
            'comm_packing_slip_id' : order.campaign.comm_packing_slip_id,
            'customer' : customer
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
        user = Users.load(self.session['user_id'])

        return_type = 'Refund' if 'T' == self.request.POST.get('rt_refund') else 'CreditIncrease'
        quantity_returned = float(self.request.POST.get('quantity_returned'))
        credit_amount = float(self.request.POST.get('credit_amount'))

        j = Journal.create_new(credit_amount, customer, order, user, return_type)
        r = ProductReturn.create_new(order_item.product, order_item.order, quantity_returned, credit_amount, j, user)
        Status.add(customer, customer, Status.find_event(customer, 'NOTE'),
                   '%s applied: %s' % (return_type, util.money(credit_amount)))

        order_item.quantity -= quantity_returned
        order_item.save()
        if self.request.POST.get('update_inventory') == u'true':
            InventoryJournal.create_new(order_item.product, 'Return', quantity_returned, order_item, None, None, r)
        return 'True'


    @view_config(route_name='crm.customer.apply_payment_dialog', renderer='/crm/customer.apply_payment.mako')
    @authorize(IsLoggedIn())
    def apply_payment_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        return {
            'customer' : customer,
            'order' : order,
            'payment_methods' : Journal.get_payment_methods(),
            'discount' : self.request.GET.get('discount', None)
            }


    @view_config(route_name='crm.customer.apply_payment', renderer='string')
    @authorize(IsLoggedIn())
    def apply_payment(self, pmt_type_param=None, pmt_method_param=None, pmt_amt_param=None):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        return self._apply_payment(customer_id, order_id, pmt_type_param, pmt_method_param, pmt_amt_param)


    def _apply_payment(self, customer_id, order_id, pmt_type_param=None, pmt_method_param=None, pmt_amt_param=None):
        """ KB: [2011-03-09]: Check that everything is kosher
        Create a journal entry for the order for the amount and type specified in the UI
        Create a status noting the type and amount of the payment applied.
        """
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        order = customer.get_order(order_id)
        self.forbid_if(not order)
        user = None
        if 'user_id' in self.session:
            user = Users.load(self.session['user_id'])
        pmt_type = self.request.POST.get('pmt_type', pmt_type_param)
        self.forbid_if(pmt_type not in Journal.get_types())

        prior_payments_applied = order.total_payments_applied()
        prior_total_due = order.total_payments_due()

        pmt_amt = float(self.request.POST.get('pmt_amount', pmt_amt_param))
        pmt_method = self.request.POST.get('pmt_method', pmt_method_param)
        Journal.create_new(pmt_amt, customer, order, user, pmt_type, pmt_method, self.request.POST.get('pmt_note')) # either FullPayment or PartialPayment
        Status.add(customer, order, Status.find_event(order, 'PAYMENT_APPLIED'),
                   '%s applied: %s' % (pmt_type, util.money(pmt_amt)))

        pre_order_balance = float(self.request.POST.get('pre_order_balance', 0))
        if pre_order_balance > 0:
            Journal.create_new(pre_order_balance, customer, order, user, 'CreditDecrease') # either FullPayment or PartialPayment
            Status.add(customer, order, Status.find_event(order, 'PAYMENT_APPLIED'),
                   '%s applied: %s' % ('CreditDecrease', util.money(pre_order_balance)))
        return 'True'


    @view_config(route_name='crm.customer.get_balance', renderer='string')
    @authorize(IsLoggedIn())
    def get_balance(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        return str(customer.get_current_balance())

    
    @view_config(route_name='crm.customer.edit_order', renderer='string')
    @authorize(IsLoggedIn())
    def edit_order(self):
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
            oi = OrderItem.load(oid)
            Status.add(customer, oi, Status.find_event(oi, 'DELETED'), 'Order Item deleted ')
            p = oi.product
            InventoryJournal.create_new(p, 'Cancelled Item', oi.quantity, oi)
            oi.delete_dt = util.today()
            oi.save()

        # extract order_items[27][quantity] to set those properties.
        order_items = {}
        for k in kv_map.keys():
            if k.startswith('order_items'):
                m = re.search(r'^.*\[(.*)\]\[(.*)\]', k)
                if m:
                    order_item_id = m.group(1)
                    attr = m.group(2)
                    new_val = float(kv_map.get(k))
                    """ KB: [2011-03-07]: If the ID ends in '_', its not really an ID but a new item.
                    product_id will only show up as non-null in the hash of a new product
                    """
                    if order_item_id[-1] == '_':
                        order_item_product = Product.load(self.request.POST.get('order_items[%s][product_id]' % order_item_id))
                        if not order_items.has_key(order_item_id):
                            order_items[order_item_id] = order.augment_order(customer,
                                                                               order_item_product,
                                                                               customer.campaign,
                                                                               Users.load(self.session['user_id']) if 'user_id' in self.session else None)
                        oi = order_items[order_item_id]
                        if 'quantity' == attr:
                            new_val = float(new_val)
                            InventoryJournal.create_new(order_item_product, 'Sale', new_val, oi)
                        setattr(oi, attr, new_val)
                        oi.save()
                    else:
                        if not order_items.has_key(order_item_id):
                            order_items[order_item_id] = OrderItem.load(order_item_id)
                        oi = order_items[order_item_id]
                        order_item_product = oi.product

                        if util.money(getattr(oi, attr)) != util.money(new_val):
                            Status.add(customer, oi, Status.find_event(oi, 'MODIFIED'),
                                       'Order Item modified: (id=%s). %s : %s -> %s' % (oi.order_item_id, attr, util.money(getattr(oi, attr)), util.money(new_val)))
                        if 'quantity' == attr:
                            new_val = float(new_val)
                            if not total_payments_applied:
                                InventoryJournal.cleanup(oi, 'Sale')
                                InventoryJournal.create_new(order_item_product, 'Sale', new_val, oi)

                        setattr(oi, attr, new_val)
                        oi.save()
        Status.add(customer, order, Status.find_event(order, 'MODIFIED'), 'Order modified')
        return 'True'


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


    @view_config(route_name='crm.customer.show_status_dialog', renderer='/crm/customer.view_status.mako')
    @authorize(IsLoggedIn())
    def show_status_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        journal_id = self.request.matchdict.get('status_id')
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
        order = order_item = events = None
        if self.request.GET.get('order_id'):
            order = CustomerOrder.load(self.request.GET.get('order_id'))
            self.forbid_if(not order or order.campaign.company.enterprise_id != self.enterprise_id)
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, order), 'event_id', 'display_name', True)
        elif self.request.GET.get('order_item_id'):
            order_item = OrderItem.load(self.request.GET.get('order_item_id'))
            self.forbid_if(not order_item or order_item.order.campaign.company.enterprise_id != self.enterprise_id)
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, order_item), 'event_id', 'display_name', True)
        else:
            events = util.select_list(StatusEvent.find_all_applicable(self.enterprise_id, customer), 'event_id', 'display_name', True)
        return {
            'customer' : customer,
            'order' : order,
            'order_item' : order_item,
            'events' : events
            }


    @view_config(route_name='crm.customer.save_status', renderer='string')
    @authorize(IsLoggedIn())
    def save_status(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        event = StatusEvent.load(self.request.POST.get('event_id'))
        self.forbid_if(not event or not self.request.POST.get('event_id') or (not event.is_system and event.enterprise_id != self.enterprise_id))
        order = None
        note = self.request.POST.get('note')
        if self.request.GET.get('order_id'):
            order = CustomerOrder.load(self.request.GET.get('order_id'))
            self.forbid_if(not order or order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order, event, note)
        elif self.request.GET.get('order_item_id'):
            order_item = OrderItem.load(self.request.GET.get('order_item_id'))
            self.forbid_if(not order_item or order_item.order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order_item, event, note)
        else:
            Status.add(customer, customer, event, note)
        return 'True'


    @view_config(route_name='crm.customer.delete', renderer='string')
    @authorize(IsLoggedIn())
    def delete(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        customer.mod_dt = util.now()
        customer.delete_dt = util.now()
        Status.add(customer, customer, StatusEvent.find('Customer', 'DELETED'), 'Customer Deleted')
        return 'True'


    """
    @authorize(OneMet(IsLoggedIn(), IsCustomerLoggedIn()))
    def self_save(self):
        self.forbid_if('customer_id' not in self.session)
        return self._save(self.session['customer_id'])
    """


    """ KB: [2012-01-31]: Called from end site customer self-edit section. """
    @authorize(IsCustomerLoggedIn())
    @validate((('password', 'required'),
               ('confirmpassword', 'required')))
    def self_change_password(self):
        self.forbid_if('customer_id' not in self.session)
        cust = Customer.load(self.session['customer_id'])
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)

        cust.password = self.request.POST.get('password')
        cust.save()
        cust.commit()
        self.flash('Password changed.')
        if self.request.POST.get('redir'):
            return HTTPFound(self.request.POST.get('redir'))
        else:
            return HTTPFound(self.request.referrer)

    """ KB: [2012-01-31]: Called from end site customer self-edit section. """
    @authorize(IsCustomerLoggedIn())
    def self_save_billing(self):
        self.forbid_if('customer_id' not in self.session or 'redir' not in self.request.POST)
        cust = Customer.load(self.session['customer_id'])
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        bill = cust.billing
        if not bill:
            bill = Billing.create(cust, True)

        bill._cc_num = self.request.POST.get('bill_cc_num')
        bill._cc_cvv = self.request.POST.get('bill_cc_cvv')
        bill.cc_exp = self.request.POST.get('bill_cc_exp')
        bill.cc_token = self.request.POST.get('bill_cc_token')
        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')

        bill.bind(self.request.POST, False, 'bill')
        bill.save()
        cust.save()
        self.db_commit()

        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        if api:
            if api.update_billing(cust, bill):
                Status.add(cust, cust, Status.find_event(cust, 'NOTE'), 'Billing Updated at gateway')

        self.flash('Successfully saved billing information.')
        return HTTPFound(self.request.POST.get('redir'))

    """ KB: [2011-04-07]: If the order id is specified, then cancel that order, otherwise, cancel every active order.
    User has to specify username and password to confirm cancellation.
    """
    @authorize(IsCustomerLoggedIn())
    def self_cancel_order(self):
        self.forbid_if('customer_id' not in self.session)
        cust = Customer.load(self.session['customer_id'])
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        self.forbid_if('username' not in self.request.POST or 'password' not in self.request.POST)

        if cust.email.lower() != self.request.POST.get('username').lower() or cust.password != self.request.POST.get('password'):
            self.flash('Username or password incorrect.  Unable to cancel.')
            return HTTPFound(self.request.referrer)

        if self.request.POST.get('order_id'):
            self._cancel_order_impl(self.session['customer_id'],
                                    self.request.POST.get('order_id'),
                                    None, True)
        else:
            for co in cust.get_active_orders():
                self._cancel_order_impl(cust.customer_id,
                                        co.order_id,
                                        None, True)

        BaseController.cancel_self.session()
        self.flash('Order cancelled.')

        cust.campaign.send_post_cancel_comm(cust)
        if self.request.POST.get('redir'):
            return HTTPFound(self.request.POST.get('redir'))
        else:
            return HTTPFound(self.request.referrer)

    """ KB: [2012-02-05]: Useful for multi-step signup processes where the
    customer is saved after step 1, and at the end you buy something. """
    def save_and_purchase(self):
        self._save(self.request.POST['customer_id'], False) # don't let it redirect
        cust = self._site_purchase(False)
        return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(cust.customer_id))

    """ KB: [2011-04-26]:
    Sign up just like in self.signup.
    Add the product ID's to the cart.
    Create all the requisite billing information from the info in POST.
    Add a real order and save everything
    Hit the configured BillingApi and bill through it.
    - If everything comes back ok then send the customer a post_purchase comm and redirect to POST['redir']
    - If not, set a self.flash as to the reason why it failed.
        - Delete the billing we just created and the order we just created.
        - Redirect back from where we came.
    Send the customer the post_purchase comm as configured for the campaign.
    Redirect to POST['redir']
    """
    def signup_and_purchase(self):
        if not self._signup():
            return HTTPFound(url('{url}?msg=signup_failed'.format(url=self.request.POST.get('url_path'))))
        cust = self._site_purchase(False)
        return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(cust.customer_id))

    def _site_purchase(self, do_redir=True):
        cust = Customer.load(self.session['customer_id'])
        bill = Billing.create(cust)
        bill._cc_num = self.request.POST.get('bill_cc_num')
        bill._cc_cvv = self.request.POST.get('bill_cc_cvv')
        bill.cc_exp = self.request.POST.get('bill_cc_exp')
        bill.cc_token = self.request.POST.get('bill_cc_token')
        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')
        bill.bind(self.request.POST, False, 'bill')
        cust.billing = bill
        cust.save()
        bill.save()
        campaign = Campaign.load(cust.campaign_id)

        cart = Cart()
        """ KB: [2012-02-12]: You can add it by product ID or by sku (which is
        less error prone when moving to production. """
        product_ids = self.request.POST.getall('prod_product_id')
        for id in product_ids:
            p = Product.load(id)
            if p:
                cart.add_item(p, cust.campaign_id)
            else:
                self.flash('No such product id = %s' % id)
                return HTTPFound(self.request.referrer)

        product_skus = self.request.POST.getall('prod_sku')
        for sku in product_skus:
            p = Product.find_by_sku(campaign, sku)
            if p:
                cart.add_item(p, cust.campaign_id)
            else:
                self.flash('No such product sku = %s' % sku)
                return HTTPFound(self.request.referrer)

        order = cust.add_order(cart,
                               None,
                               Site.load(self.session['site_id']),
                               campaign)

        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        api.set_coupon(self.request.POST.get('coupon_code'))
        if not api or api.purchase(order, bill, self.cc_response_handler, util.self.request_ip()):
            # accept terms if they sent accept_terms as positive across (checkbox)
            if ('accept_terms' in self.request.POST and self.request.POST['accept_terms'] == '1'):
                accept = OrderItemTermsAcceptance()
                accept.order_id = order.order_id
                accept.signature = cust.email
                accept.save()
                accept.commit()

            self._apply_payment(cust.customer_id, order.order_id, 'FullPayment', api.payment_method, order.total_price())
            try:
                campaign.send_post_purchase_comm(order)
            except:
                pass
            if do_redir:
                return HTTPFound(self.request.POST.get('redir'))
            else:
                return cust
        else:
            (last_status, last_note) = api.get_last_status()
            self.flash('Unable to bill credit card: %s' % last_note)
            bill.delete_billing(cust)
            order.delete()
            bill.commit()
            #BaseController.cancel_self.session()
            return HTTPFound(self.request.referrer)

    """ KB: [2011-04-26]:
    Customer can't exist.  Fail if there is a customer_id param
    The customer should never be able to get here if he's logged in.  Forbid if there is a self.session open.
    Try to find the customer by the email provided.
    - If found by email, redirect back to the calling page (POST['url_path'] with msg = already_exists
    Save the customer object and store in the self.session as though the customer has logged in.

    If something goes wrong, redirect back to the calling page with msg = signup_failed
    """
    @validate((('fname', 'string'), ('fname', 'required'),
               ('lname', 'string'), ('lname', 'required'),
               ('email', 'string'), ('email', 'required'),
               ('password', 'required'), ('confirmpassword', 'required')
               ))
    def _signup(self):
        self.forbid_if(self.request.POST.get('customer_id') or 'customer_id' in self.session or 'campaign_id' not in self.session)

        campaign = Campaign.load(self.session['campaign_id'])
        cust = Customer.find(self.request.POST.get('email'), campaign)
        if cust:
            return HTTPFound('/?msg=already_exists')

        cust = Customer()
        cust.campaign = campaign
        cust.bind(self.request.POST)
        g = self.get_geoip()
        if g and 'latitude' in g and 'longitude' in g:
            cust.default_latitude = g['latitude']
            cust.default_longitude = g['longitude']
        cust.save()
        self.db_commit()
        self.session['customer_id'] = cust.customer_id
        self.session['customer_logged_in'] = True
        self.session.save()
        c.customer = cust
        return True

    def signup(self):
        if self._signup():
            return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(c.customer.customer_id))

    """ KB: [2011-04-26]:
    Sign up just like in self.signup.
    Add the product ID's to the cart.
    Add a real order and save everything
    - Products are whatever free thing is being offered.
    - Don't create billing because this thing is free.
    Send the customer the post_purchase comm as configured for the campaign.
    Redirect to POST['redir']
    """
    def signup_free(self):
        if not self._signup():
            return HTTPFound(url('{url}?msg=signup_failed'.format(url=self.request.POST.get('url_path'))))

        product_ids = self.request.POST.getall('prod_product_id')
        cust = Customer.load(self.session['customer_id'])
        cart = Cart()
        for id in product_ids:
            cart.add_item(Product.load(id), cust.campaign_id)

        campaign = Campaign.load(cust.campaign_id)
        order = cust.add_order(cart,
                               None,
                               Site.load(self.session['site_id']),
                               campaign)
        self.db_commit()
        campaign.send_post_purchase_comm(order)
        return HTTPFound(self.request.POST.get('redir'))


    def check_duplicate_email(self, email):
        if not 'site_id' in self.session: return ''
        site = Site.load(self.session['site_id'])
        cust = Customer.find(email, site.company)
        return 'True' if cust else 'False'

    """ KB: [2010-10-20]: Callback for handling the API when it's completed processing. """
    def cc_response_handler(self, api, response_dict, history_record, order, billing):
        if api.is_declined(response_dict):
            Status.add(order.customer, order, Status.find_event(order, 'BILLING_DECLINED'),
                       'Billing Declined: %s' % history_record.notes).commit()
            return False
        else:
            Status.add(order.customer, order, Status.find_event(order, 'BILLING_SUCCESS'),
                       'Billing Succeeded: %s' % history_record.notes).commit()
            j = Journal.create_new(order.total_payments_due(), order.customer, order, None,
                                   'FullPayment', 'Credit Card', None)
            if j:
                j.commit()
            return True


    def _prep_add_order_dialog(self, customer_id):
        customer = Customer.load(customer_id)
        self.forbid_if(not c.customer or c.customer.campaign.company.enterprise_id != BaseController.get_enterprise_id())
        return {
            'customer' : customer,
            'products' : Product.find_by_campaign(customer.campaign)
            }


    def _add_order_impl(self, customer_id, product_ids, prices, user, discount_id, campaign_id, incl_tax=True):
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != BaseController.get_enterprise_id())
        cart = Cart()
        campaign_id = campaign_id if campaign_id else cust.campaign_id
        cart.discount_id = discount_id
        for id in product_ids.keys():
            quantity = product_ids[id]
            price = prices[id] if prices and id in prices else None
            cart.add_item(Product.load(id), campaign_id, quantity, price)

        order = cust.add_order(cart, user, Site.load(self.session['site_id']), Campaign.load(campaign_id), incl_tax)
        order.flush()
        return order.order_id


    """ KB: [2012-02-12]: Cancel the order internally and make calls to billing
    if there is a recurring product to cancel """
    def _cancel_order_impl(self, customer_id, order_id, reason, by_customer=False):
        co = CustomerOrder.load(order_id)
        self.forbid_if(not co)
        cust = co.customer
        bill = cust.billing
        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        if api:
            if api.cancel_order(co, bill):
                Status.add(cust, cust, Status.find_event(cust, 'NOTE'), 'Billing Cancelled at gateway')
        co.cancel(reason, by_customer)
        self.db_flush()

