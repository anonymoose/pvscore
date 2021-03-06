#pylint: disable-msg=C0103,C0302
from pvscore.tests import TestController, secure, alternate_site, secure_as_root
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.customerorder import CustomerOrder
from pvscore.model.crm.orderitem import OrderItem
from pvscore.model.core.status import Status
from pvscore.model.crm.product import Product
from pvscore.lib.billing_api import StripeBillingApi
from pvscore.model.crm.company import Enterprise
from pvscore.model.crm.journal import Journal
import pvscore.lib.util as util

# bin/T pvscore.tests.controllers.test_crm_customer

class TestCrmCustomer(TestController):
    def test_misc(self):
        cust = self.get_customer()
        cust2 = Customer.load(str(cust.customer_id), False)
        assert cust2 is not None
        assert str(cust.customer_id) == str(cust2.customer_id)
        assert 'FullPayment' in Journal.get_types()
        assert 1 == Customer.count("where customer_id = '%s'" % str(cust.customer_id))
        assert cust.get_attr('BOGUS', 'defaultx') == 'defaultx'


    def test_customer_login_to_link(self):
        cust = self.get_customer()
        url = '/crm/customer_login_to_link/%s/%s' % (cust.customer_id, '%7C')  # go to '/'
        R = self.get(url)  #pylint: disable-msg=E1300
        assert R.status_int == 200
        R.mustcontain(cust.customer_id)


    def _create_new(self):  #pylint: disable-msg=R0915
        # create the customer and ensure he's editable.
        R = self.get('/crm/customer/new')
        assert R.status_int == 200
        R.mustcontain('New Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['customer_id'].value, '')
        f.set('fname', 'Fnametest')
        f.set('lname', 'Lnametest')
        f.set('company_name', 'Test Company')
        f.set('email', 'ken@testxyz.com')
        f.set('addr1', '123 Elm')
        f.set('city', 'Jacksonville')
        f.set('phone', '9041112222')
        f.set('password', 'password')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_customer']
        R.mustcontain('Edit Customer')
        customer_id = f['customer_id'].value
        self.assertNotEqual(f['customer_id'].value, '')

        cust = Customer.load(customer_id)
        assert cust != None and str(cust.customer_id) == customer_id
        prods = Product.find_by_campaign(cust.campaign)
        assert prods and len(prods) > 3

        # order 3 things and make sure they are there.
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Add Order')
        R = self.post('/crm/customer/add_order/%s' % str(customer_id),
                      {'products[%s]' % prods[0].product_id : '1.0',
                       'products[%s]' % prods[1].product_id : '2.0',
                       'products[%s]' % prods[2].product_id : '1.0'})  # <-- this one has inventory = 0
        assert R.status_int == 200
        order_id = R.body
        order = CustomerOrder.load(order_id)
        assert str(order.customer.customer_id) in str(order.customer)
        self.assertNotEqual(order, None)
        oids = []
        for item in order.items:
            self.assertEqual(item.product_id in (prods[0].product_id, prods[1].product_id, prods[2].product_id), True)
            oids.append(item.order_item_id)
            assert [] == item.children
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Edit Order (%s)' % order_id)
        total = order.total_price()

        # KB: [2012-09-08]: pay for it. we can't hit the button because
        # it does JS magic.  so, simulate the JS magic and add something.
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))
        assert R.status_int == 200
        R.mustcontain('Finalize Order')
        for oid in oids:
            R.mustcontain('quantity%s' % oid)
        R.mustcontain('$%.2f' % total)

        # add something to the order
        post_data = {'shipping_total' : '0.00', 'create_dt' : '2011-07-23'}
        for oid in oids:
            oitem = OrderItem.load(oid)
            post_data['order_items[%s][unit_price]' % oitem.order_item_id] = oitem.unit_price
            post_data['order_items[%s][quantity]' % oitem.order_item_id] = oitem.quantity + 1
        post_data['order_items[999_][unit_price]'] = 25
        post_data['order_items[999_][quantity]'] = 1.00
        post_data['order_items[999_][product_id]'] = prods[2].product_id
        post_data['order_items_to_delete[]'] = oids[0]
        R = self.post('/crm/customer/edit_order/%s/%s' % (str(customer_id), str(order_id)), post_data)
        order.invalidate_self()
        order = CustomerOrder.load(order_id)
        total = order.total_price()

        R = self.get('/crm/customer/apply_payment_dialog/%s/%s' % (customer_id, order_id))
        assert R.status_int == 200
        R.mustcontain('Apply Payment to Order')
        f = R.forms['frm_apply_payment']
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('FullPayment applied: $%.2f' % total)
        return customer_id


    def _delete_new(self, customer_id):
        Customer.full_delete(customer_id)
        Customer.delete_all("where customer_id = '%s'" % str(customer_id))  # this is just for coverage for the delete_all method in meta.py
        self.commit()


    @secure
    def test_show_new(self):
        self._test_show_new()


    @secure_as_root
    def test_show_new_as_root(self):
        self._test_show_new()


    def _test_show_new(self):
        R = self.get('/crm/customer/new')
        assert R.status_int == 200
        R.mustcontain('New Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['fname'].value, '')


    @secure
    def test_create_new(self):
        self._test_create_new()


    @secure_as_root
    def test_create_new_as_root(self):
        self._test_create_new()


    def _test_create_new(self):
        customer_id = self._create_new()
        self._delete_new(customer_id)


    @secure
    def test_show_history(self):
        self._test_show_history()


    @secure_as_root
    def test_show_history_as_root(self):
        self._test_show_history()


    def _test_show_history(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/edit/%s' % customer_id)
        assert R.status_int == 200
        R = self.get('/crm/customer/show_history/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Customer History')
        R.mustcontain('CustomerOrder Payment Applied')
        self._delete_new(customer_id)


    @secure
    def test_show_billing(self):
        self._test_show_billing()


    @secure_as_root
    def test_show_billing_as_root(self):
        self._test_show_billing()


    def _test_show_billing(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/edit/%s' % customer_id)
        assert R.status_int == 200
        R = self.get('/crm/customer/show_billings/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Customer Billing Activity')
        R.mustcontain('FullPayment')
        #R.mustcontain('CreditDecrease')
        self._delete_new(customer_id)


    @secure
    def test_show_attributes(self):
        self._test_show_attributes()


    @secure_as_root
    def test_show_attributes_as_root(self):
        self._test_show_attributes()


    def _test_show_attributes(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/edit/%s' % customer_id)
        assert R.status_int == 200
        R = self.get('/crm/customer/show_attributes/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Customer Attributes')
        self._delete_new(customer_id)


    @secure
    def test_search(self):
        self._test_search()


    @secure_as_root
    def test_search_as_root(self):
        self._test_search()


    def _test_search(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/show_search')
        assert R.status_int == 200
        R.mustcontain('Customer Search')
        f = R.forms['frm_customer_search']
        f.set('phone', '9041112222')
        f.set('fname', 'Fnametest')
        f.set('lname', 'Lnametest')
        f.set('email', 'ken@testxyz.com')
        f.set('company_name', 'Test Company')
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('Edit Customer')
        self._delete_new(customer_id)


    @secure
    def test_save_existing(self):
        self._test_save_existing()


    @secure_as_root
    def test_save_existing_as_root(self):
        self._test_save_existing()


    def _test_save_existing(self):
        customer_id = self._create_new()

        R = self.get('/crm/customer/edit/%s' % customer_id)
        R.mustcontain('Edit Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['customer_id'].value, customer_id)
        self.assertEqual(f['fname'].value, 'Fnametest')
        self.assertEqual(f['email'].value, 'ken@testxyz.com')

        f.set('fname', 'Fnametest new')
        f.set('lname', 'Lnametest new')
        f.set('email', 'ken@testxyz.com new')
        f.set('attr_name[0]', 'attr0key')
        f.set('attr_value[0]', 'attr0val')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_customer']
        R.mustcontain('Edit Customer')

        self.assertEqual(f['customer_id'].value, customer_id)
        self.assertEqual(f['fname'].value, 'Fnametest new')
        self.assertEqual(f['lname'].value, 'Lnametest new')
        self.assertEqual(f['email'].value, 'ken@testxyz.com new')
        self.assertEqual(f['attr_name[0]'].value, 'attr0key')
        self.assertEqual(f['attr_value[0]'].value, 'attr0val')
        self._delete_new(customer_id)


    @secure
    def test_autocomplete(self):
        self._test_autocomplete()


    @secure_as_root
    def test_autocomplete_as_root(self):
        self._test_autocomplete()


    def _test_autocomplete(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/autocomplete',
                      {'search_key': 'Bedw'})
        R.mustcontain('Bedwell, Ken')
        R.mustcontain('Bedwell, Zach')
        R = self.get('/crm/customer/autocomplete',
                      {'search_key': 'BEDW'})
        R.mustcontain('Bedwell, Ken')
        R.mustcontain('Bedwell, Zach')

        R = self.get('/crm/customer/autocomplete',
                      {'search_key': 'BedWeLL'})
        R.mustcontain('Bedwell, Ken')
        R.mustcontain('Bedwell, Zach')

        R = self.get('/crm/customer/autocomplete',
                      {'search_key': 'brookewell@gmail.com'})
        R.mustcontain('Bedwell, Zach')
        self._delete_new(customer_id)


    @secure
    def test_add_order(self):
        self._test_add_order()


    @secure_as_root
    def test_add_order_as_root(self):
        self._test_add_order()


    def _test_add_order(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Add Order')

        cust = Customer.load(customer_id)
        assert cust != None and str(cust.customer_id) == customer_id
        prods = Product.find_by_campaign(cust.campaign)
        assert prods and len(prods) > 3

        R = self.post('/crm/customer/add_order/%s' % str(customer_id),
                      {'products[%s]' % prods[0].product_id : '1.0',
                       'products[%s]' % prods[1].product_id : '2.0',
                       'products[%s]' % prods[2].product_id : '1.0'})  # <-- this one has inventory = 0
        assert R.status_int == 200
        order_id = R.body
        order = CustomerOrder.load(order_id)
        self.assertNotEqual(order, None)
        for item in order.items:
            self.assertEqual(item.product_id in (prods[0].product_id, prods[1].product_id, prods[2].product_id), True)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Edit Order (%s)' % order_id)
        self._delete_new(customer_id)


    @secure
    def test_show_billing_dialog(self):
        self._test_show_billing_dialog()


    @secure_as_root
    def test_show_billing_dialog_as_root(self):
        self._test_show_billing_dialog()


    def _test_show_billing_dialog(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/show_billings/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Customer Billing Activity')
        journal_entry = cust.get_active_orders()[0].journal_entries[0]
        assert str(journal_entry.journal_id) in str(journal_entry)
        R = self.get('/crm/customer/show_billing_dialog/%s/%s?dialog=1' % (customer_id, journal_entry.journal_id))
        assert R.status_int == 200
        R.mustcontain('%.2f' % journal_entry.amount)

        # some misc stuff here for coverage.
        order = CustomerOrder.load(cust.get_active_orders()[0].order_id)
        Journal.total_credit_increases(order)
        Journal.total_refunds(order)
        Journal.find_refunds_by_order(order)
        Journal.find_all_by_order(order)
        Journal.find_refunds_by_order(order)
        Journal.find_payments_by_order(order)
        Journal.find_discounts_by_order(order)
        Journal.find_credits_by_order(order)
        self._delete_new(customer_id)


    def _test_return_impl(self, return_type, customer_id):
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Order List')
        ordr = cust.get_active_orders()[0]
        jslink = "customer_edit_order('%s')" % ordr.order_id
        R.mustcontain(jslink)
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, ordr.order_id))
        assert R.status_int == 200
        R.mustcontain("Finalize Order for")
        oitem = ordr.active_items[0]
        R = self.get('/crm/customer/return_item_dialog/%s/%s/%s' % (customer_id, ordr.order_id, oitem.order_item_id))
        assert R.status_int == 200
        R.mustcontain('Return <i><b>%s</b></i>' % oitem.product.name)
        f = R.forms['frm_return_item']
        f.set('rt_refund_type', return_type)
        R = f.submit('btn_return')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain("&#39;%s&#39; returned.  $%.2f refunded by %s" % (oitem.product.name, oitem.total(), return_type))


    @secure
    def test_return_item_credit(self):
        self._test_return_item_credit()


    @secure_as_root
    def test_return_item_credit_as_root(self):
        self._test_return_item_credit()


    def _test_return_item_credit(self):
        customer_id = self._create_new()
        self._test_return_impl('CreditIncrease', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_return_item_refund(self):
        self._test_return_item_refund()


    @secure_as_root
    def test_return_item_refund_as_root(self):
        self._test_return_item_refund()


    def _test_return_item_refund(self):
        customer_id = self._create_new()
        self._test_return_impl('Refund', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_return_single_item(self):  #pylint: disable-msg=R0915
        self._test_return_single_item()


    @secure_as_root
    def test_return_single_item_as_root(self):  #pylint: disable-msg=R0915
        self._test_return_single_item()


    def _test_return_single_item(self):  #pylint: disable-msg=R0915
        R = self.get('/crm/customer/new')
        assert R.status_int == 200
        R.mustcontain('New Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['customer_id'].value, '')
        f.set('fname', 'Fnametest')
        f.set('lname', 'Lnametest')
        f.set('email', 'ken@testxyz.com')
        f.set('addr1', '123 Elm')
        f.set('city', 'Jacksonville')
        f.set('phone', '9041112222')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_customer']
        R.mustcontain('Edit Customer')
        customer_id = f['customer_id'].value
        self.assertNotEqual(f['customer_id'].value, '')
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Add Order')
        cust = Customer.load(customer_id)
        assert cust != None and str(cust.customer_id) == customer_id
        prods = Product.find_by_campaign(cust.campaign)
        assert prods and len(prods) > 3
        R = self.post('/crm/customer/add_order/%s' % str(customer_id), {'products[%s]' % prods[0].product_id : '1.0'})
        assert R.status_int == 200
        order_id = R.body
        order = CustomerOrder.load(order_id)
        self.assertNotEqual(order, None)
        item = order.items[0]
        self.assertEqual(item.product_id, prods[0].product_id)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Edit Order (%s)' % order_id)
        total = order.total_price()
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))
        assert R.status_int == 200
        R.mustcontain('Finalize Order')
        R.mustcontain('quantity%s' % item.order_item_id)
        R.mustcontain('$%.2f' % total)
        R = self.get('/crm/customer/apply_payment_dialog/%s/%s' % (customer_id, order_id))
        assert R.status_int == 200
        R.mustcontain('Apply Payment to Order')
        f = R.forms['frm_apply_payment']
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('FullPayment applied: $%.2f' % total)
        self._test_return_impl('Refund', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_check_duplicate_email(self):
        self._test_check_duplicate_email()


    @secure_as_root
    def test_check_duplicate_email_as_root(self):
        self._test_check_duplicate_email()


    def _test_check_duplicate_email(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/check_duplicate_email/%s' % cust.email)
        assert R.status_int == 200
        self.assertEqual(R.body, 'True')
        R = self.get('/crm/customer/check_duplicate_email/thisemailisnothere@test.com')
        assert R.status_int == 200
        self.assertEqual(R.body, 'False')
        self._delete_new(customer_id)


    @secure
    def test_customer_status(self):
        self._test_customer_status()


    @secure_as_root
    def test_customer_status_as_root(self):
        self._test_customer_status()


    def _test_customer_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/status_dialog/%s?dialog=1' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Frobdicate')  # our pre-canned test status that changes customer status
        cust = Customer.load(customer_id, False)
        event = Status.find_event(cust.campaign.company.enterprise_id, cust, 'FROBDICATE')
        f = R.forms['frm_dialog']
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('Statused Customer to Frobdicate')
        self._delete_new(customer_id)


    @secure
    def test_order_status(self):
        self._test_order_status()


    @secure_as_root
    def test_order_status_as_root(self):
        self._test_order_status()


    def _test_order_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        order = cust.orders[0]
        R = self.get('/crm/customer/status_dialog/%s?order_id=%s&dialog=1' % (customer_id, order.order_id))
        assert R.status_int == 200
        R.mustcontain('Foobaz')
        cust = Customer.load(customer_id, False)
        event = Status.find_event(cust.campaign.company.enterprise_id, order, 'FOOBAZ')
        f = R.forms['frm_dialog']
        self.assertEqual(f['order_id'].value, str(order.order_id))
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('Statused Order to Foobaz')
        self._delete_new(customer_id)


    @secure
    def test_order_item_status(self):
        self._test_order_item_status()


    @secure_as_root
    def test_order_item_status_as_root(self):
        self._test_order_item_status()


    def _test_order_item_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        order = cust.orders[0]
        order_item = order.active_items[0]
        R = self.get('/crm/customer/status_dialog/%s?order_item_id=%s&dialog=1' % (customer_id, order_item.order_item_id))
        assert R.status_int == 200
        R.mustcontain('Derf')
        cust = Customer.load(customer_id, False)
        event = Status.find_event(cust.campaign.company.enterprise_id, order_item, 'DERF')
        f = R.forms['frm_dialog']
        self.assertEqual(f['order_item_id'].value, str(order_item.order_item_id))
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        R.mustcontain('Statused Item to Derf')
        self._delete_new(customer_id)


    @secure
    def test_customer_status_dialog(self):
        self._test_customer_status_dialog()


    @secure_as_root
    def test_customer_status_dialog_as_root(self):
        self._test_customer_status_dialog()


    def _test_customer_status_dialog(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        hist = Status.find_by_customer(cust, 0)[0]
        R = self.get('/crm/customer/show_status_dialog/%s/%s' % (cust.customer_id, hist.status_id))
        assert R.status_int == 200
        self._delete_new(customer_id)


    @secure
    def test_customer_delete(self):
        self._test_customer_delete()


    @secure_as_root
    def test_customer_delete_as_root(self):
        self._test_customer_delete()


    def _test_customer_delete(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.assertEqual(cust.delete_dt, None)
        R = self.get('/crm/customer/edit/%s' % customer_id)
        assert R.status_int == 200
        R = self.get('/crm/customer/delete/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('True')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertNotEqual(cust.delete_dt, None)
        self._delete_new(customer_id)


    def test_signup(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_signup_and_purchase(self):
        R = self.post('/crm/customer/signup_and_purchase',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'product_sku' : 'T2-002',   # recurring prod
                       'confirmpassword' : 'password',
                       'bill_cc_num' : '4007000000027',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1),
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        prod = Product.find_by_sku(self.site.company.enterprise_id, cust.campaign, 'T2-002')
        custs = prod.get_customers()
        assert str(cust.customer_id) in [str(cust_.customer_id) for cust_ in custs]
        custs = prod.get_customers_created_today()
        assert str(cust.customer_id) in [str(cust_.customer_id) for cust_ in custs]
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        self._delete_new(customer_id)


    @secure
    def test_signup_exists(self):
        self._test_signup_exists()


    @secure_as_root
    def test_signup_exists_as_root(self):
        self._test_signup_exists()


    def _test_signup_exists(self):
        customer_id = self._create_new()
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'ken@testxyz.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        R.mustcontain('Email ken@testxyz.com already in use')
        self._delete_new(customer_id)

    @secure
    def test_get_balance(self):
        self._test_get_balance()


    @secure_as_root
    def test_get_balance_as_root(self):
        self._test_get_balance()


    def _test_get_balance(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/get_balance/%s' % customer_id)
        self.assertEqual(R.body, "0.0")
        self._delete_new(customer_id)


    @secure
    def test_self_get_balance(self):
        self._test_self_get_balance()


    @secure_as_root
    def test_self_get_balance_as_root(self):
        self._test_self_get_balance()


    def _test_self_get_balance(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.login_customer(cust.email, 'password')
        R = self.get('/crm/customer/self_get_balance/%s' % customer_id)
        self.assertEqual(R.body, "0.0")
        self.logout_customer()
        self._delete_new(customer_id)


    @secure
    def test_not_logged_in(self):
        self._test_not_logged_in()


    @secure_as_root
    def test_not_logged_in_as_root(self):
        self._test_not_logged_in()


    def _test_not_logged_in(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/self_get_balance/%s' % customer_id)
        self.assertEqual(R.request.url, 'http://%s/?path=/crm/customer/self_get_balance/%s&vars=' % (self.get_host(), customer_id))
        self._delete_new(customer_id)


    @secure
    def test_self_save(self):
        self._test_self_save()


    @secure_as_root
    def test_self_save_as_root(self):
        self._test_self_save()


    def _test_self_save(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_save',
                      {'customer_id' : customer_id,
                       'fname' : 'Fnametest new',
                       'lname' : 'Lnametest new',
                       'password' : '',
                       'email' : 'ken@testxyz.com new'})
        R.mustcontain('Successfully saved Fnametest new Lnametest new')
        self.logout_customer()
        self._delete_new(customer_id)


    @secure
    def test_self_cancel_invalid_password(self):
        self._test_self_cancel_invalid_password()


    @secure_as_root
    def test_self_cancel_invalid_password_as_root(self):
        self._test_self_cancel_invalid_password()


    def _test_self_cancel_invalid_password(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.login_customer(cust.email, cust.password)
        orders = cust.get_active_orders()
        pre_len = len(orders)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': 'bogus',
                       'order_id' : orders[0].order_id})
        assert R.status_int == 200
        R.mustcontain('Username or password incorrect.  Unable to cancel.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), pre_len)
        self.logout_customer()
        self._delete_new(customer_id)


    @secure
    def test_self_cancel_one(self):
        self._test_self_cancel_one()


    @secure_as_root
    def test_self_cancel_one_as_root(self):
        self._test_self_cancel_one()


    def _test_self_cancel_one(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.login_customer(cust.email, cust.password)
        order = cust.get_active_orders()[0]
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password,
                       'order_id' : order.order_id})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        self.logout_customer()
        self._delete_new(customer_id)


    @secure
    def test_self_cancel_all(self):
        self._test_self_cancel_all()


    @secure_as_root
    def test_self_cancel_all_as_root(self):
        self._test_self_cancel_all()


    def _test_self_cancel_all(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        self.logout_customer()
        self._delete_new(customer_id)


    def test_contact(self):
        custs = Customer.find_all_by_email('testcontact@test.com')
        assert len(custs) == 0
        R = self.post('/crm/customer/contact',
                      {'fname'   : 'Ken',
                       'lname'   : 'Bedwell',
                       'email'   : 'testcontact@test.com',
                       'phone'   : '1234567890',
                       'message' : 'This is the message',
                       'redir'   : '/crm'
                       })
        assert R.status_int == 200
        custs = Customer.find_all_by_email('testcontact@test.com')
        assert len(custs) == 0


    def test_contact_save(self):
        custs = Customer.find_all_by_email('testcontact@test.com')
        assert len(custs) == 0
        R = self.post('/crm/customer/contact',
                      {'fname'   : 'Ken',
                       'lname'   : 'Bedwell',
                       'email'   : 'testcontact@test.com',
                       'phone'   : '1234567890',
                       'message' : 'This is the message',
                       'save'    : '1',
                       'redir'   : '/crm'
                       })
        assert R.status_int == 200
        custs = Customer.find_all_by_email('testcontact@test.com')
        assert len(custs) == 1
        Customer.full_delete(custs[0].customer_id)


    @secure
    def test_stripe_cancel_order(self):
        self._test_stripe_cancel_order()


    @secure_as_root
    def test_stripe_cancel_order_as_root(self):
        self._test_stripe_cancel_order()


    def _test_stripe_cancel_order(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'NDN-VID-001',  # known test plan at stripe test account
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert api.get_last_status() == (None, None)
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        assert R.status_int == 200
        R.mustcontain('Order List')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        ordr = cust.get_active_orders()[0]
        url = '/crm/customer/cancel_order_dialog/%s/%s' % (customer_id, ordr.order_id)
        R.mustcontain(url)
        R = self.get(url)
        assert R.status_int == 200
        R.mustcontain("Cancel Order from")
        f = R.forms['frm_cancel']
        f.set('cancel_reason', 'This is a cancel reason')
        R = f.submit('btn_cancel')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        assert url not in R.body
        self._delete_new(customer_id)


    def test_stripe_save_and_purchase(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        products = Product.find_by_campaign(self.site.default_campaign)
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : products[0].sku,
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        self._delete_new(customer_id)


    def test_stripe_save_and_purchase_invalid_sku(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'crapcrap',
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert R.status_int == 200
        R.mustcontain("No such product sku: crapcrap")
        self._delete_new(customer_id)


    def test_stripe_save_and_purchase_invalid_cc(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        products = Product.find_by_campaign(self.site.default_campaign)
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : products[0].sku,
                       'bill_cc_token' : api.create_token('4000000000000002', '12', '2019', '123')
                       })
        assert R.status_int == 200
        R.mustcontain("Unable to bill credit card:")
        self._delete_new(customer_id)


    def test_stripe_self_save_billing(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        products = Product.find_by_campaign(self.site.default_campaign)
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : products[0].sku,
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        R = self.post('/crm/customer/self_save_billing',
                      {'fname' : 'Ken Test',
                       'bill_cc_token' : api.create_token('4012888888881881', '12', '2019', '123')
                       })
        assert R.status_int == 200
        R.mustcontain("Successfully saved billing information.")
        self._delete_new(customer_id)


    def test_stripe_self_save_billing_invalid(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        products = Product.find_by_campaign(self.site.default_campaign)
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : products[0].sku,
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        R = self.post('/crm/customer/self_save_billing',
                      {'fname' : 'Ken Test',
                       'bill_cc_token' : api.create_token('4000000000000002', '12', '2019', '123')
                       })
        assert R.status_int == 200
        R.mustcontain("Unable to save credit card information")
        self._delete_new(customer_id)

    @secure
    def test_stripe_self_cancel_at_gateway(self):
        self._test_stripe_self_cancel_at_gateway()


    @secure_as_root
    def test_stripe_self_cancel_at_gateway_as_root(self):
        self._test_stripe_self_cancel_at_gateway()


    def _test_stripe_self_cancel_at_gateway(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        products = Product.find_by_campaign(self.site.default_campaign)
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : products[0].sku,
                       'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        cust = Customer.load(customer_id)
        #self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        #self.logout_customer()
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_authnet_purchase_nrc(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'addr1' : '123 Elm',
                       'city' : 'Ponte Vedra',
                       'state' : 'FL',
                       'zip' : '32081',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-001',   # non-recurring prod
                       'bill_cc_num' : '4007000000027',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_authnet_purchase_nrc_invalid(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'addr1' : '123 Elm',
                       'city' : 'Ponte Vedra',
                       'state' : 'FL',
                       'zip' : '32081',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-001',   # non-recurring prod
                       'bill_cc_num' : '40070000bogus',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        R.mustcontain("Unable to bill credit card:")
        self._delete_new(customer_id)


    # T2-001      | Test 2 Product
    # T2-002      | Test 2 Recurring
    @alternate_site('test2.com')
    def test_authnet_self_save_billing_invalid(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-002',   # recurring prod
                       'bill_cc_num' : '4007000000027',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        R = self.post('/crm/customer/self_save_billing',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'bill_cc_num' : '4012888818bogus',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        R.mustcontain("Unable to save credit card information: Credit Card Number must be a numeric value.")
        cust = Customer.load(customer_id)
        #self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        #self.logout_customer()
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_authnet_self_save_billing(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-002',   # recurring prod
                       'bill_cc_num' : '4007000000027',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        R = self.post('/crm/customer/self_save_billing',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'bill_cc_num' : '4012888818888',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        R.mustcontain("Successfully saved billing information.")
        cust = Customer.load(customer_id)
        #self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        #self.logout_customer()
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_authnet_save_and_purchase_invalid_cc(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-002',   # recurring prod
                       'bill_cc_num' : '4007000BOGUS',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        R.mustcontain("Unable to bill credit card:")
        self._delete_new(customer_id)


    @alternate_site('test2.com')
    def test_authnet_self_cancel_at_gateway(self):
        R = self.post('/crm/customer/signup',
                      {'fname' : 'Ken',
                       'lname' : 'Bedwell',
                       'email' : 'test@test.com',
                       'password' : 'password',
                       'confirmpassword' : 'password',
                       'redir' : '/'
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        customer_id = R.request.params['customer_id']
        cust = Customer.load(customer_id)
        self.assertEqual(str(cust.customer_id), str(customer_id))
        self.assertEqual(cust.fname, 'Ken')
        self.assertEqual(cust.lname, 'Bedwell')
        self.assertEqual(cust.email, 'test@test.com')
        R = self.post('/crm/customer/save_and_purchase',
                      {'fname' : 'Ken Test',
                       'accept_terms' : '1',
                       'product_sku' : 'T2-002',   # recurring prod
                       'bill_cc_num' : '4007000000027',
                       'bill_cc_cvv' : '123',
                       'bill_exp_month' : '02',
                       'bill_exp_year' : str(util.this_year()+1)
                       })
        assert R.status_int == 200
        assert 'customer_id' in R.request.params
        self.assertEqual(str(R.request.params['customer_id']), str(customer_id))
        cust = Customer.load(customer_id)
        #self.login_customer(cust.email, cust.password)
        R = self.post('/crm/customer/self_cancel_order',
                      {'username': cust.email,
                       'password': cust.password})
        assert R.status_int == 200
        R.mustcontain('Order cancelled.')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertEqual(len(cust.get_active_orders()), 0)
        #self.logout_customer()
        self._delete_new(customer_id)


