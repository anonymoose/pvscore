import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.purchase import PurchaseOrder, PurchaseOrderItem, Vendor
from app.model.crm.company import Company, Enterprise
from app.model.crm.campaign import Campaign

# T app.tests.controllers.test_crm_purchase

class TestCrmPurchase(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/crm/purchase/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Supplier Order')
        f = R.forms['frm_purchase']
        self.assertEqual(f['purchase_order_id'].value, '')


    @secure
    def test_list_with_new(self):
        report_id = self._create_new()
        R = self.get('/crm/purchase/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Purchase Order')
        self._delete_new(report_id)


    @secure
    def test_create_new(self):
        report_id = self._create_new()
        self._delete_new(report_id)


    @secure
    def test_save_existing(self):
        purchase_order_id = self._create_new()
        R = self.get('/crm/purchase/list')
        self.assertEqual(R.status_int, 200)
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
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_purchase']
        R.mustcontain('Edit Supplier Order')

        self.assertEqual(f['purchase_order_id'].value, purchase_order_id)
        self.assertEqual(f['note'].value, 'Test Purchase Order')
        self.assertEqual(str(f['shipping_cost'].value), '234.00')
        self.assertEqual(str(f['tax_cost'].value), '0.23')
        self._delete_new(purchase_order_id)


    def _create_new(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        vendors = Vendor.find_all(ent.enterprise_id)
        v = vendors[0]

        R = self.get('/crm/purchase/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Supplier Order')
        f = R.forms['frm_purchase']
        self.assertEqual(f['purchase_order_id'].value, '')
        f.set('vendor_id', v.vendor_id)
        f.set('shipping_cost', 123.45)
        f.set('note', 'Test Purchase Order')
        
        R = f.submit()
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_purchase']
        R.mustcontain('Edit Supplier Order')
        purchase_order_id = f['purchase_order_id'].value
        self.assertNotEqual(f['purchase_order_id'].value, '')
        return purchase_order_id


    def _delete_new(self, purchase_order_id):
        c = PurchaseOrder.load(purchase_order_id)
        self.assertNotEqual(c, None)
        c.delete()
        self.commit()

        
