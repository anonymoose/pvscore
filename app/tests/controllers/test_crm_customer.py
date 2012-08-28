import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.customer import Customer

# T app.tests.controllers.test_crm_customer

class TestCrmCustomer(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/crm/customer/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Customer')
        f = R.forms['frm_customer']
        self.assertEqual(f['fname'].value, '')


    def _create_new(self):
        R = self.get('/crm/customer/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Customer')
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
        return customer_id


    def _delete_new(self, customer_id):
        Customer.full_delete(int(str(customer_id)))
        self.commit()
        

    @secure
    def test_create_new(self):
        customer_id = self._create_new()
        self._delete_new(customer_id)


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
        product_id = self._create_new()
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
        self._delete_new(product_id)


