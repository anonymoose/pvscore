from pvscore.tests import TestController, secure
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.customerorder import CustomerOrder
from pvscore.model.crm.orderitem import OrderItem
from pvscore.model.core.status import Status

# T pvscore.tests.controllers.test_crm_customer

TEST_CUSTOMER_ID = 220

class TestCrmCustomer(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/crm/customer/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['fname'].value, '')


    def _create_new(self):  #pylint: disable-msg=R0915
        # create the customer and ensure he's editable.
        R = self.get('/crm/customer/new')
        self.assertEqual(R.status_int, 200)
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
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_customer']
        R.mustcontain('Edit Customer')
        customer_id = f['customer_id'].value
        self.assertNotEqual(f['customer_id'].value, '')

        # order 3 things and make sure they are there.
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Add Order')
        R = self.post('/crm/customer/add_order/%s' % str(customer_id),
                      {'products[1451]' : '1.0',
                       'products[1450]' : '2.0',
                       'products[2090]' : '1.0'})  # <-- this one has inventory = 0
        self.assertEqual(R.status_int, 200)
        order_id = R.body
        order = CustomerOrder.load(order_id)
        self.assertNotEqual(order, None)
        oids = []
        for item in order.items:
            self.assertEqual(item.product_id in (1451, 1450, 2090), True)
            oids.append(item.order_item_id)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Order (%s)' % order_id)
        total = order.total_price()

        # KB: [2012-09-08]: pay for it. we can't hit the button because
        # it does JS magic.  so, simulate the JS magic and add something.
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Finalize Order')
        for oid in oids:
            R.mustcontain('quantity%s' % oid)
        R.mustcontain('$%.2f' % total)
        
        # add something to the order
        product_to_add = {'shipping_total' : '0.00', 'create_dt' : '2011-07-23'}
        for oid in oids:
            oitem = OrderItem.load(oid)
            product_to_add['order_items[%s][unit_price]' % oitem.order_item_id] = oitem.unit_price
            product_to_add['order_items[%s][quantity]' % oitem.order_item_id] = oitem.quantity
        product_to_add['order_items[999_][unit_price]'] = 25
        product_to_add['order_items[999_][quantity]'] = 1.00
        product_to_add['order_items[999_][product_id]'] = 1451
        R = self.post('/crm/customer/edit_order/%s/%s' % (str(customer_id), str(order_id)), product_to_add)
        order.invalidate_self()
        order = CustomerOrder.load(order_id)
        total = order.total_price()

        R = self.get('/crm/customer/apply_payment_dialog/%s/%s' % (customer_id, order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Apply Payment to Order')
        f = R.forms['frm_apply_payment']
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('FullPayment applied: $%.2f' % total)
        return customer_id


    def _delete_new(self, customer_id):
        Customer.full_delete(int(str(customer_id)))
        self.commit()


    @secure
    def test_create_new(self):
        customer_id = self._create_new()
        self._delete_new(customer_id)


    @secure
    def test_show_history(self):
        customer_id = TEST_CUSTOMER_ID
        R = self.get('/crm/customer/edit/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R = self.get('/crm/customer/show_history/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Customer History')
        R.mustcontain('CustomerOrder Payment Applied')


    @secure
    def test_show_billing(self):
        customer_id = TEST_CUSTOMER_ID
        R = self.get('/crm/customer/edit/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R = self.get('/crm/customer/show_billings/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Customer Billing Activity')
        R.mustcontain('FullPayment')
        R.mustcontain('CreditDecrease')


    @secure
    def test_show_attributes(self):
        customer_id = TEST_CUSTOMER_ID
        R = self.get('/crm/customer/edit/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R = self.get('/crm/customer/show_attributes/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Customer Attributes')


    @secure
    def test_search(self):
        customer_id = self._create_new()
        R = self.get('/crm/customer/show_search')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Customer Search')
        f = R.forms['frm_customer_search']
        f.set('phone', '9041112222')
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Customer')
        self._delete_new(customer_id)


    @secure
    def test_save_existing(self):
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
        self.assertEqual(R.status_int, 200)
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
        customer_id = self._create_new()
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Add Order')

        R = self.post('/crm/customer/add_order/%s' % str(customer_id),
                      {'products[1451]' : '1.0',
                       'products[1450]' : '2.0',
                       'products[2090]' : '1.0'})  # <-- this one has inventory = 0
        self.assertEqual(R.status_int, 200)
        order_id = R.body
        order = CustomerOrder.load(order_id)
        self.assertNotEqual(order, None)
        for item in order.items:
            self.assertEqual(item.product_id in (1451, 1450, 2090), True)

        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Order (%s)' % order_id)

        self._delete_new(customer_id)

    @secure
    def test_show_billing_dialog(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/show_billings/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Customer Billing Activity')
        journal_entry = cust.get_active_orders()[0].journal_entries[0]
        R = self.get('/crm/customer/show_billing_dialog/%s/%s?dialog=1' % (customer_id, journal_entry.journal_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('%.2f' % journal_entry.amount)
        self._delete_new(customer_id)


    @secure
    def test_cancel_order(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Order List')
        ordr = cust.get_active_orders()[0]
        url = '/crm/customer/cancel_order_dialog/%s/%s' % (customer_id, ordr.order_id)
        R.mustcontain(url)
        R = self.get(url)
        self.assertEqual(R.status_int, 200)
        R.mustcontain("Cancel Order from")
        f = R.forms['frm_cancel']
        f.set('cancel_reason', 'This is a cancel reason')
        R = f.submit('btn_cancel')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        assert url not in R.body
        self._delete_new(customer_id)

    
    def _test_return_impl(self, return_type, customer_id):
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Order List')
        ordr = cust.get_active_orders()[0]
        jslink = 'customer_edit_order(%s)' % ordr.order_id
        R.mustcontain(jslink)
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, ordr.order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain("Finalize Order for")
        oitem = ordr.active_items[0]
        R = self.get('/crm/customer/return_item_dialog/%s/%s/%s' % (customer_id, ordr.order_id, oitem.order_item_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Return <i><b>%s</b></i>' % oitem.product.name)
        f = R.forms['frm_return_item']
        f.set('rt_refund_type', return_type)
        R = f.submit('btn_return')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain("&#39;%s&#39; returned.  $%.2f refunded by %s" % (oitem.product.name, oitem.total(), return_type))


    @secure
    def test_return_item_credit(self):
        customer_id = self._create_new()
        self._test_return_impl('CreditIncrease', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_return_item_refund(self):
        customer_id = self._create_new()
        self._test_return_impl('Refund', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_return_single_item(self):
        R = self.get('/crm/customer/new')
        self.assertEqual(R.status_int, 200)
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
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_customer']
        R.mustcontain('Edit Customer')
        customer_id = f['customer_id'].value
        self.assertNotEqual(f['customer_id'].value, '')
        R = self.get('/crm/customer/add_order_dialog/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Add Order')
        R = self.post('/crm/customer/add_order/%s' % str(customer_id), {'products[1451]' : '1.0'})
        self.assertEqual(R.status_int, 200)
        order_id = R.body
        order = CustomerOrder.load(order_id)
        self.assertNotEqual(order, None)
        item = order.items[0]
        self.assertEqual(item.product_id, 1451)
        R = self.get('/crm/customer/show_orders/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Order (%s)' % order_id)
        total = order.total_price()
        R = self.get('/crm/customer/edit_order_dialog/%s/%s' % (customer_id, order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Finalize Order')
        R.mustcontain('quantity%s' % item.order_item_id)
        R.mustcontain('$%.2f' % total)
        R = self.get('/crm/customer/apply_payment_dialog/%s/%s' % (customer_id, order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Apply Payment to Order')
        f = R.forms['frm_apply_payment']
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('FullPayment applied: $%.2f' % total)
        self._test_return_impl('Refund', customer_id)
        self._delete_new(customer_id)


    @secure
    def test_check_duplicate_email(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/check_duplicate_email/%s' % cust.email)
        self.assertEqual(R.status_int, 200)
        self.assertEqual(R.body, 'True')
        R = self.get('/crm/customer/check_duplicate_email/thisemailisnothere@test.com')
        self.assertEqual(R.status_int, 200)
        self.assertEqual(R.body, 'False')
        self._delete_new(customer_id)
        
        
    @secure
    def test_customer_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        R = self.get('/crm/customer/status_dialog/%s?dialog=1' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Frobdicate')  # our pre-canned test status that changes customer status
        event = Status.find_event(cust.campaign.company.enterprise_id, cust, 'FROBDICATE')
        f = R.forms['frm_dialog']
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Statused Customer to Frobdicate')
        self._delete_new(customer_id)


    @secure
    def test_order_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        order = cust.orders[0]
        R = self.get('/crm/customer/status_dialog/%s?order_id=%s&dialog=1' % (customer_id, order.order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Foobaz')
        event = Status.find_event(cust.campaign.company.enterprise_id, order, 'FOOBAZ')
        f = R.forms['frm_dialog']
        self.assertEqual(f['order_id'].value, str(order.order_id))
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Statused Order to Foobaz')
        self._delete_new(customer_id)


    @secure
    def test_order_item_status(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        order = cust.orders[0]
        order_item = order.active_items[0]
        R = self.get('/crm/customer/status_dialog/%s?order_item_id=%s&dialog=1' % (customer_id, order_item.order_item_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Derf')
        event = Status.find_event(cust.campaign.company.enterprise_id, order_item, 'DERF')
        f = R.forms['frm_dialog']
        self.assertEqual(f['order_item_id'].value, str(order_item.order_item_id))
        f.set('event_id', event.event_id)
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Statused Item to Derf')
        self._delete_new(customer_id)


    @secure
    def test_customer_status_dialog(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        hist = Status.find_by_customer(cust, 0)[0]
        R = self.get('/crm/customer/show_status_dialog/%s/%s' % (cust.customer_id, hist.status_id))
        self.assertEqual(R.status_int, 200)
        self._delete_new(customer_id)


    @secure
    def test_customer_delete(self):
        customer_id = self._create_new()
        cust = Customer.load(customer_id)
        self.assertEqual(cust.delete_dt, None)
        R = self.get('/crm/customer/edit/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R = self.get('/crm/customer/delete/%s' % customer_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('True')
        cust.invalidate_caches()
        cust = Customer.load(customer_id)
        self.assertNotEqual(cust.delete_dt, None)
        self._delete_new(customer_id)



        




