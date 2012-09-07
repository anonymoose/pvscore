import logging, re
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.validate import validate
from app.lib.decorators.authorize import authorize
from app.lib.auth_conditions import IsLoggedIn, IsCustomerLoggedIn
from app.model.core.users import Users
from app.model.crm.customer import Customer
from app.model.crm.billing import Billing
from app.model.crm.product import Product, ProductReturn, InventoryJournal
from app.model.crm.campaign import Campaign
from app.model.crm.journal import Journal
from app.model.crm.customerorder import CustomerOrder
from app.model.crm.orderitem import OrderItem#, OrderItemTermsAcceptance
from app.model.core.status import Status
from app.model.core.statusevent import StatusEvent
from app.model.cms.site import Site
import simplejson as json
import app.lib.util as util
from app.lib.billing_api import BaseBillingApi
from app.lib.catalog import Cart

log = logging.getLogger(__name__)

class CustomerController(BaseController):
    @view_config(route_name='crm.customer.edit', renderer='/crm/customer.edit.mako')
    @authorize(IsLoggedIn())
    @validate((('customer_id', 'int'),
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
        cust = Customer.load(customer_id)
        if not cust:
            cust = Customer()
            cust.user_created = cust.user_assigned = username
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
    def autocomplete(self):
        if not 'search_key' in self.request.GET or not self.request.GET.get('search_key'):
            return
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
            'orders' : [order for order in customer.orders if order.delete_dt is None and order.cancel_dt is None]
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
            'orders' : CustomerOrder.find_by_customer(Customer.load(customer_id), None, start_dt, end_dt)
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



    @view_config(route_name='crm.customer.edit_billing_dialog', renderer='/crm/customer.edit_billing.mako')
    @authorize(IsLoggedIn())
    def edit_billing_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        if not customer.billing:
            customer.billing = Billing.create(customer, False)
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
            cust.billing.user_created = self.request.ctx.user
        if self.request.POST.has_key('cc_num'):
            cust.billing._cc_num = self.request.POST.get('cc_num')
        cust.billing.bind(self.request.POST)
        cust.billing.save()
        return 'True'


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
        bill = cust.billing
        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
        if api:
            if api.cancel_order(codr, bill):
                Status.add(cust, cust, Status.find_event(self.enterprise_id, cust, 'NOTE'), 'Billing Cancelled at gateway')
        codr.cancel(reason, by_customer)
        cust.invalidate_caches()


    @view_config(route_name='crm.customer.cancel_billing', renderer='string')
    @authorize(IsLoggedIn())
    def cancel_billing(self):
        customer_id = self.request.matchdict.get('customer_id')
        journal_id = self.request.matchdict.get('journal_id')
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        jrnl = Journal.load(journal_id)
        self.forbid_if(not jrnl or jrnl.customer_id != cust.customer_id)
        jrnl.cancel()
        self.flash('Billing record cancelled.')
        return HTTPFound('/crm/customer/show_billings/%s' % cust.customer_id)


    @view_config(route_name='crm.customer.add_order_dialog', renderer='/crm/customer.add_order.mako')
    @authorize(IsLoggedIn())
    def add_order_dialog(self):
        customer_id = self.request.matchdict.get('customer_id')
        return self._prep_add_order_dialog(customer_id)


    @view_config(route_name='crm.customer.add_order_and_apply', renderer='string')
    @authorize(IsLoggedIn())
    def add_order_and_apply(self):
        """ KB: [2011-10-21]:
        If an email thats not POS@ was specified, then send them a receipt.
        otherwise, just save it and move on to the next order.
        """
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
        cust = Customer.load(customer_id)
        self.forbid_if(not cust)
        product_ids = {}
        for key in self.request.POST.keys():
            if key.startswith('products'):
                match = re.search(r'^.*\[(.*)\]', key)
                if match:
                    pid = match.group(1)
                    quant = float(self.request.POST.get(key))
                    if pid in product_ids:
                        product_ids[pid] += quant
                    else:
                        product_ids[pid] = quant

        order_id = self._add_order_impl(customer_id, product_ids,
                                        None, self.request.ctx.user,
                                        self.request.POST.get('discount_id'),
                                        self.request.POST.get('campaign_id', self.request.GET.get('campaign_id')),
                                        self.incl_tax)
        cust.invalidate_caches()
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
            'customer' : customer,
            'order' : order,
            'comm_packing_slip_id' : order.campaign.comm_packing_slip_id,
            'total_price' : order.total_price(),
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

        import pdb; pdb.set_trace()
        return_type = self.request.POST.get('rt_refund_type')
        quantity_returned = float(self.request.POST.get('quantity_returned'))
        credit_amount = float(self.request.POST.get('credit_amount'))

        jrnl = Journal.create_new(credit_amount, customer, order, user, return_type)
        ret = ProductReturn.create_new(order_item.product, order_item.order, quantity_returned, credit_amount, jrnl, user)
        status_note = "'%s' returned.  $%s refunded by %s" % (order_item.product.name, credit_amount, return_type)
        Status.add(customer, order_item, Status.find_event(self.enterprise_id, order_item, 'RETURN'), status_note)

        order_item.quantity -= quantity_returned
        if order_item.quantity == 0:
            order_item.delete_dt = util.today()
        order_item.save()
        if self.request.POST.get('update_inventory') == '1':
            InventoryJournal.create_new(order_item.product, 'Return', quantity_returned, order_item, None, None, ret)
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
            'payment_methods' : Journal.get_payment_methods(),
            'total_payments_applied' : order.total_payments_applied(),
            'total_discounts_applied' : order.total_discounts_applied(),
            'total_due' : total_due,
            'pre_order_balance' : pre_order_balance,
            'total_due_after_balance' : total_due+pre_order_balance if (total_due+pre_order_balance) > 0 else 0
            }


    @view_config(route_name='crm.customer.apply_payment')
    @authorize(IsLoggedIn())
    def apply_payment(self):
        customer_id = self.request.matchdict.get('customer_id')
        order_id = self.request.matchdict.get('order_id')
        self._apply_payment(customer_id, order_id)
        return HTTPFound('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))


    def _apply_payment(self, customer_id, order_id, pmt_type_param=None, pmt_method_param=None, pmt_amt_param=None):
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
        prior_payments_applied = order.total_payments_applied()
        prior_total_due = order.total_payments_due()
        balance_amount_to_apply = float(self.request.POST.get('pmt_balance_amount_to_apply', 0.0))
        amt = float(self.request.POST.get('pmt_amount', pmt_amt_param))
        method = self.request.POST.get('pmt_method', pmt_method_param)
        note = self.request.POST.get('pmt_note')

        if (amt + balance_amount_to_apply) > prior_total_due:
            raise Exception("amt + balance_amount_to_apply > prior_total_due")
        if current_customer_balance > 0 and balance_amount_to_apply > current_customer_balance:
            raise Exception("balance_amount_to_apply > current_customer_balance")

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
            oitem = OrderItem.load(oid)
            Status.add(customer, oitem, Status.find_event(self.enterprise_id, oitem, 'DELETED'), 'OrderItem deleted ')
            prod = oitem.product
            InventoryJournal.create_new(prod, 'Cancelled Item', oitem.quantity, oitem)
            oitem.delete_dt = util.today()
            oitem.save()

        # extract order_items[27][quantity] to set those properties.
        order_items = {}
        for key in self.request.POST.keys():
            if key.startswith('order_items'):
                match = re.search(r'^.*\[(.*)\]\[(.*)\]', key)
                if match:
                    order_item_id = match.group(1)
                    attr = match.group(2)
                    new_val = float(self.request.POST.get(key))
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
                        if 'quantity' == attr:
                            new_val = float(new_val)
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
            redir = '/crm/customer/edit_order/%s/%s' % (customer_id, order_item.order_id)
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
        self.forbid_if(not event or not self.request.POST.get('event_id') or (not event.is_system and event.enterprise_id != self.enterprise_id))
        order = None
        note = self.request.POST.get('note')

        if self.request.POST.get('order_id'):
            order = CustomerOrder.load(self.request.POST.get('order_id'))
            self.forbid_if(not order or order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order, event, note)
            self.flash('Statused Order to %s' % event.display_name)
        elif self.request.POST.get('order_item_id'):
            order_item = OrderItem.load(self.request.POST.get('order_item_id'))
            self.forbid_if(not order_item or order_item.order.campaign.company.enterprise_id != self.enterprise_id)
            Status.add(customer, order_item, event, note)
            self.flash('Statused Item to %s' % event.display_name)
        else:
            Status.add(customer, customer, event, note)
            self.flash('Statused Customer to %s' % event.display_name)
        customer.invalidate_caches()
        return HTTPFound(self.request.POST.get('redir'))


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


    @authorize(IsCustomerLoggedIn())
    @validate((('password', 'required'),
               ('confirmpassword', 'required')))
    def self_change_password(self):
        """ KB: [2012-01-31]: Called from end site customer self-edit section. """
        self.forbid_if('customer_id' not in self.session)
        cust = Customer.load(self.session['customer_id'])
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)

        cust.password = self.request.POST.get('password')
        cust.save()
        self.flash('Password changed.')
        if self.request.POST.get('redir'):
            return HTTPFound(self.request.POST.get('redir'))
        else:
            return HTTPFound(self.request.referrer)


#    @authorize(IsCustomerLoggedIn())
#    def self_save_billing(self):
#        """ KB: [2012-01-31]: Called from end site customer self-edit section. """
#        self.forbid_if('customer_id' not in self.session or 'redir' not in self.request.POST)
#        cust = Customer.load(self.session['customer_id'])
#        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
#        bill = cust.billing
#        if not bill:
#            bill = Billing.create(cust, True)
#
#        bill._cc_num = self.request.POST.get('bill_cc_num')
#        bill._cc_cvv = self.request.POST.get('bill_cc_cvv')
#        bill.cc_exp = self.request.POST.get('bill_cc_exp')
#        bill.cc_token = self.request.POST.get('bill_cc_token')
#        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
#            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')
#
#        bill.bind(self.request.POST, False, 'bill')
#        bill.save()
#        cust.save()
#        self.db_flush()
#        
#        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
#        if api:
#            if api.update_billing(cust, bill):
#                Status.add(cust, cust, Status.find_event(self.enterprise_id, cust, 'NOTE'), 'Billing Updated at gateway')
#
#        self.flash('Successfully saved billing information.')
#        return HTTPFound(self.request.POST.get('redir'))


#    @authorize(IsCustomerLoggedIn())
#    def self_cancel_order(self):
#        """ KB: [2011-04-07]: If the order id is specified, then cancel that order, otherwise, cancel every active order.
#        User has to specify username and password to confirm cancellation.
#        """
#        self.forbid_if('customer_id' not in self.session)
#        cust = Customer.load(self.session['customer_id'])
#        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
#        self.forbid_if('username' not in self.request.POST or 'password' not in self.request.POST)
#
#        if cust.email.lower() != self.request.POST.get('username').lower() or cust.password != self.request.POST.get('password'):
#            self.flash('Username or password incorrect.  Unable to cancel.')
#            return HTTPFound(self.request.referrer)
#
#        if self.request.POST.get('order_id'):
#            self._cancel_order_impl(self.session['customer_id'],
#                                    self.request.POST.get('order_id'),
#                                    None, True)
#        else:
#            for cord in cust.get_active_orders():
#                self._cancel_order_impl(cust.customer_id,
#                                        cord.order_id,
#                                        None, True)
#        self.flash('Order cancelled.')
#
#        cust.campaign.send_post_cancel_comm(cust)
#        if self.request.POST.get('redir'):
#            return HTTPFound(self.request.POST.get('redir'))
#        else:
#            return HTTPFound(self.request.referrer)


#    def save_and_purchase(self):
#        """ KB: [2012-02-05]: Useful for multi-step signup processes where the
#        customer is saved after step 1, and at the end you buy something. """
#        self._save(self.request.POST['customer_id'], False) # don't let it redirect
#        cust = self._site_purchase(False)
#        return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(cust.customer_id))

#    def signup_and_purchase(self):
#        """ KB: [2011-04-26]:
#        Sign up just like in self.signup.
#        Add the product ID's to the cart.
#        Create all the requisite billing information from the info in POST.
#        Add a real order and save everything
#        Hit the configured BillingApi and bill through it.
#        - If everything comes back ok then send the customer a post_purchase comm and redirect to POST['redir']
#        - If not, set a self.flash as to the reason why it failed.
#        - Delete the billing we just created and the order we just created.
#        - Redirect back from where we came.
#        Send the customer the post_purchase comm as configured for the campaign.
#        Redirect to POST['redir']
#        """
#        if not self._signup():
#            return HTTPFound('{url}?msg=signup_failed'.format(url=self.request.POST.get('url_path'))))
#        cust = self._site_purchase(False)
#        return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(cust.customer_id))

#    def _site_purchase(self, do_redir=True):
#        cust = Customer.load(self.session['customer_id'])
#        bill = Billing.create(cust)
#        bill._cc_num = self.request.POST.get('bill_cc_num')
#        bill._cc_cvv = self.request.POST.get('bill_cc_cvv')
#        bill.cc_exp = self.request.POST.get('bill_cc_exp')
#        bill.cc_token = self.request.POST.get('bill_cc_token')
#        if 'bill_exp_month' in self.request.POST and 'bill_exp_year' in self.request.POST:
#            bill.cc_exp = self.request.POST.get('bill_exp_month') + '/' + self.request.POST.get('bill_exp_year')
#        bill.bind(self.request.POST, False, 'bill')
#        cust.billing = bill
#        cust.save()
#        bill.save()
#        campaign = Campaign.load(cust.campaign_id)
#
#        cart = Cart()
#        # KB: [2012-02-12]: You can add it by product ID or by sku (which is
#        # less error prone when moving to production.
#        product_ids = self.request.POST.getall('prod_product_id')
#        for id in product_ids:
#            p = Product.load(id)
#            if p:
#                cart.add_item(p, cust.campaign_id)
#            else:
#                self.flash('No such product id = %s' % id)
#                return HTTPFound(self.request.referrer)
#
#        product_skus = self.request.POST.getall('prod_sku')
#        for sku in product_skus:
#            p = Product.find_by_sku(campaign, sku)
#            if p:
#                cart.add_item(p, cust.campaign_id)
#            else:
#                self.flash('No such product sku = %s' % sku)
#                return HTTPFound(self.request.referrer)
#
#        order = cust.add_order(cart,
#                               None,
#                               Site.load(self.session['site_id']),
#                               campaign)
#
#        api = BaseBillingApi.create_api(cust.campaign.company.enterprise)
#        api.set_coupon(self.request.POST.get('coupon_code'))
#        if not api or api.purchase(order, bill, self.cc_response_handler, util.self.request_ip()):
#            # accept terms if they sent accept_terms as positive across (checkbox)
#            if ('accept_terms' in self.request.POST and self.request.POST['accept_terms'] == '1'):
#                accept = OrderItemTermsAcceptance()
#                accept.order_id = order.order_id
#                accept.signature = cust.email
#                accept.save()
#                accept.flush()
#
#            self._apply_payment(cust.customer_id, order.order_id, 'FullPayment', api.payment_method, order.total_price())
#            try:
#                campaign.send_post_purchase_comm(order)
#            except:
#                pass
#            if do_redir:
#                return HTTPFound(self.request.POST.get('redir'))
#            else:
#                return cust
#        else:
#            (last_status, last_note) = api.get_last_status()
#            self.flash('Unable to bill credit card: %s' % last_note)
#            bill.delete_billing(cust)
#            order.delete()
#            bill.flush()
#            #BaseController.cancel_self.session()
#            return HTTPFound(self.request.referrer)


#    @validate((('fname', 'string'), ('fname', 'required'),
#               ('lname', 'string'), ('lname', 'required'),
#               ('email', 'string'), ('email', 'required'),
#               ('password', 'required'), ('confirmpassword', 'required')
#               ))
#    def _signup(self):
#        """ KB: [2011-04-26]:
#        Customer can't exist.  Fail if there is a customer_id param
#        The customer should never be able to get here if he's logged in.  Forbid if there is a self.session open.
#        Try to find the customer by the email provided.
#        - If found by email, redirect back to the calling page (POST['url_path'] with msg = already_exists
#        Save the customer object and store in the self.session as though the customer has logged in.
#        
#        If something goes wrong, redirect back to the calling page with msg = signup_failed
#        """
#        self.forbid_if(self.request.POST.get('customer_id') or 'customer_id' in self.session or 'campaign_id' not in self.session)
#
#        campaign = Campaign.load(self.session['campaign_id'])
#        cust = Customer.find(self.request.POST.get('email'), campaign)
#        if cust:
#            return HTTPFound('/?msg=already_exists')
#
#        cust = Customer()
#        cust.campaign = campaign
#        cust.bind(self.request.POST)
#        g = self.get_geoip()
#        if g and 'latitude' in g and 'longitude' in g:
#            cust.default_latitude = g['latitude']
#            cust.default_longitude = g['longitude']
#        cust.save()
#        self.db_commit()
#        self.session['customer_id'] = cust.customer_id
#        self.session['customer_logged_in'] = True
#        self.session.save()
#        c.customer = cust
#        return True

#    def signup(self):
#        if self._signup():
#            return HTTPFound(self.request.POST.get('redir') + '?customer_id=' + str(c.customer.customer_id))

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

    def check_duplicate_email(self, email):
        if not 'site_id' in self.session:
            return ''
        site = Site.load(self.session['site_id'])
        cust = Customer.find(email, site.company)
        return 'True' if cust else 'False'


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


    def _prep_add_order_dialog(self, customer_id):
        customer = Customer.load(customer_id)
        self.forbid_if(not customer or customer.campaign.company.enterprise_id != self.enterprise_id)
        products = Product.find_by_campaign(customer.campaign)
        return {
            'customer' : customer,
            'products' : products
            }


    def _add_order_impl(self, customer_id, product_ids, prices, user, discount_id, campaign_id, incl_tax=True):
        cust = Customer.load(customer_id)
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != self.enterprise_id)
        cart = Cart()
        campaign_id = campaign_id if campaign_id else cust.campaign_id
        cart.discount_id = discount_id
        for pid in product_ids.keys():
            quantity = product_ids[pid]
            price = prices[pid] if prices and pid in prices else None
            cart.add_item(Product.load(pid), cust.campaign, quantity, price)
        order = cust.add_order(cart, user, self.request.ctx.site, cust.campaign, incl_tax)
        order.flush()
        return order.order_id
