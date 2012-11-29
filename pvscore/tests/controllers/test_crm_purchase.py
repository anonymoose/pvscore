from pvscore.tests import TestController, secure
from pvscore.model.crm.company import Enterprise
from pvscore.model.crm.product import Product
from pvscore.model.crm.purchase import Vendor, PurchaseOrder
from pvscore.model.core.statusevent import StatusEvent
import simplejson as json

# T pvscore.tests.controllers.test_crm_purchase

class TestCrmPurchase(TestController):

    @secure
    def test_show_new_vendor(self):
        R = self.get('/crm/purchase/vendor/new')
        assert R.status_int == 200
        R.mustcontain('Edit Vendor')
        f = R.forms['frm_vendor']
        self.assertEqual(f['vendor_id'].value, '')


    @secure
    def test_list_with_new_vendor(self):
        vendor_id = self._create_new_vendor()
        R = self.get('/crm/purchase/vendor/list')
        assert R.status_int == 200
        R.mustcontain('Test Vendor')
        self._delete_new_vendor(vendor_id)


    @secure
    def test_create_new_vendor(self):
        vendor_id = self._create_new_vendor()
        self._delete_new_vendor(vendor_id)


    @secure
    def test_save_existing_vendor(self):
        vendor_id = self._create_new_vendor()
        R = self.get('/crm/purchase/vendor/list')
        assert R.status_int == 200
        R.mustcontain('Test Vendor')

        R = self.get('/crm/purchase/vendor/edit/%s' % vendor_id)
        R.mustcontain('Edit Vendor')
        f = R.forms['frm_vendor']
        self.assertEqual(f['vendor_id'].value, vendor_id)
        self.assertEqual(f['name'].value, 'Test Vendor')
        self.assertEqual(f['addr1'].value, '123 Elm')

        f.set('note', 'Test Note New')

        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_vendor']
        R.mustcontain('Edit Vendor')

        self.assertEqual(f['vendor_id'].value, vendor_id)
        self.assertEqual(f['note'].value, 'Test Note New')
        self._delete_new_vendor(vendor_id)


    def _create_new_vendor(self):
        R = self.get('/crm/purchase/vendor/new')
        assert R.status_int == 200
        R.mustcontain('Edit Vendor')
        f = R.forms['frm_vendor']
        self.assertEqual(f['vendor_id'].value, '')
        f.set('name', 'Test Vendor')
        f.set('addr1', '123 Elm')
        f.set('note', 'Test Note')
        
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_vendor']
        R.mustcontain('Edit Vendor')
        vendor_id = f['vendor_id'].value
        self.assertNotEqual(f['vendor_id'].value, '')
        self.assertEqual(str(f['name'].value), 'Test Vendor')
        return vendor_id


    def _delete_new_vendor(self, vendor_id):
        ven = Vendor.load(vendor_id)
        self.assertNotEqual(ven, None)
        ven.delete()
        self.commit()


    @secure
    def test_show_history(self):
        purchase_order_id = self._create_new()
        R = self.get('/crm/purchase/complete/%s' % purchase_order_id)
        assert R.status_int == 200
        R.mustcontain('True')
        R = self.get('/crm/purchase/edit/%s' % purchase_order_id)
        assert R.status_int == 200
        R.mustcontain('Completed:')
        R = self.get('/crm/purchase/show_history/%s' % purchase_order_id)
        assert R.status_int == 200
        R.mustcontain('PurchaseOrder Completed')
        self._delete_new(purchase_order_id)


    @secure
    def test_search(self):
        R = self.get('/crm/purchase/show_search')
        assert R.status_int == 200
        R.mustcontain('Purchase Order Search')
        
        f = R.forms['frm_purchase_search']
        #f.set('vendor_id', 21)
        f.set('from_dt', '2000-01-01')
        f.set('to_dt', '2040-01-01')
        R = f.submit()
        R.mustcontain('Purchase Order Search')
        R.mustcontain('2011-06-21')
        R.mustcontain('180.0')


    @secure
    def test_show_new(self):
        R = self.get('/crm/purchase/new')
        assert R.status_int == 200
        R.mustcontain('Edit Supplier Order')
        f = R.forms['frm_purchase']
        self.assertEqual(f['purchase_order_id'].value, '')


    @secure
    def test_list_with_new(self):
        purchase_order_id = self._create_new()
        R = self.get('/crm/purchase/list')
        assert R.status_int == 200
        R.mustcontain('Test Purchase Order')
        self._delete_new(purchase_order_id)


    @secure
    def test_create_new(self):
        purchase_order_id = self._create_new()
        self._delete_new(purchase_order_id)


    @secure
    def test_order_item_add_delete(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        purchase_order_id = self._create_new()
        prods = Product.find_all(ent.enterprise_id)
        product_id = prods[0].product_id

        # add a new one
        R = self.post('/crm/purchase/save_purchase_order_item/%s?product_id=%s' % (str(purchase_order_id), product_id),
                      {'order_note' : 'Note Note',
                       'quantity' : 10,
                       'unit_cost' : 123})
        oitem = json.loads(R.body)
        assert R.status_int == 200
        order_item_id = oitem['id']

        # get the json from it
        R = self.get('/crm/purchase/order_item_json/%s/%s' % (purchase_order_id, order_item_id))
        assert R.status_int == 200
        oitem = json.loads(R.body)
        self.assertEqual(oitem['order_item_id'], order_item_id)
        self.assertEqual(oitem['note'], 'Note Note')
        self.assertEqual(int(oitem['unit_cost']), 123)
        self.assertEqual(int(oitem['quantity']), 10)

        # complete the item
        R = self.get('/crm/purchase/complete_item/%s/%s' % (purchase_order_id, order_item_id))
        assert R.status_int == 200
        R.mustcontain('True')

        #R = self.get('/crm/purchase/show_history/%s' % purchase_order_id)
        #assert R.status_int == 200
        #R.mustcontain('PurchaseOrder Completed')

        # delete the oi
        R = self.get('/crm/purchase/delete_purchase_order_item/%s/%s' % (purchase_order_id, order_item_id))
        assert R.status_int == 200
        R.mustcontain('True')
        
        self._delete_new(purchase_order_id)


    @secure
    def test_complete_po(self):
        purchase_order_id = self._create_new()

        ent = Enterprise.find_by_name('Healthy U Store')
        prods = Product.find_all(ent.enterprise_id)
        product_id = prods[0].product_id

        # add a new one
        R = self.post('/crm/purchase/save_purchase_order_item/%s?product_id=%s' % (str(purchase_order_id), product_id),
                      {'order_note' : 'Note Note',
                       'quantity' : 10,
                       'unit_cost' : 123})
        json.loads(R.body)
        assert R.status_int == 200

        R = self.get('/crm/purchase/complete/%s' % purchase_order_id)
        assert R.status_int == 200
        R.mustcontain('True')
        R = self.get('/crm/purchase/edit/%s' % purchase_order_id)
        assert R.status_int == 200
        R.mustcontain('Completed:')
        self._delete_new(purchase_order_id)


    @secure
    def test_save_status(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        evt = StatusEvent.find(ent.enterprise_id, 'PurchaseOrder', 'TESTEVENT_PO')
        purchase_order_id = self._create_new()

        R = self.post(str('/crm/purchase/save_status/%s' % purchase_order_id),
                      {'event_id' : evt.event_id,
                       'note' : 'Note Note'})
        assert R.status_int == 200
        self._delete_new(purchase_order_id)
        

    @secure
    def test_save_existing(self):
        purchase_order_id = self._create_new()
        R = self.get('/crm/purchase/list')
        assert R.status_int == 200
        R.mustcontain('Test Purchase Order')

        R = self.get('/crm/purchase/edit/%s' % purchase_order_id)
        R.mustcontain('Edit Supplier Order')
        f = R.forms['frm_purchase']
        self.assertEqual(f['purchase_order_id'].value, purchase_order_id)
        self.assertEqual(f['note'].value, 'Test Purchase Order')

        f.set('tax_cost', 0.23)
        f.set('shipping_cost', 234)

        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_purchase']
        R.mustcontain('Edit Supplier Order')

        self.assertEqual(f['purchase_order_id'].value, purchase_order_id)
        self.assertEqual(f['note'].value, 'Test Purchase Order')
        self.assertEqual(str(f['shipping_cost'].value), '234.00')
        self.assertEqual(str(f['tax_cost'].value), '0.23')
        self._delete_new(purchase_order_id)


    def _create_new(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        vendors = Vendor.find_all(ent.enterprise_id)
        ven = vendors[0]

        R = self.get('/crm/purchase/new')
        assert R.status_int == 200
        R.mustcontain('Edit Supplier Order')
        f = R.forms['frm_purchase']
        self.assertEqual(f['purchase_order_id'].value, '')
        f.set('vendor_id', ven.vendor_id)
        f.set('shipping_cost', 123.45)
        f.set('note', 'Test Purchase Order')
        
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_purchase']
        R.mustcontain('Edit Supplier Order')
        purchase_order_id = f['purchase_order_id'].value
        self.assertNotEqual(f['purchase_order_id'].value, '')
        return purchase_order_id


    def _delete_new(self, purchase_order_id):
        pord = PurchaseOrder.load(purchase_order_id)
        self.assertNotEqual(pord, None)
        pord.delete()
        self.commit()

        
