from pvscore.tests import TestController, secure
from pvscore.model.crm.discount import Discount

# T pvscore.tests.controllers.test_crm_discount

def create_new_product_discount(testcase, automatic=False):
    R = testcase.get('/crm/discount/new')
    assert R.status_int == 200
    R.mustcontain('Edit Discount')
    f = R.forms['frm_discount']
    testcase.assertEqual(f['discount_id'].value, '')
    f.set('name', 'Test Discount')
    f.set('code', 'tst101')
    f.set('description', 'tst101 description')
    f.set('percent_off', '10')
    f['web_enabled'] = True
    f['cart_discount'] = False
    f['automatic'] = automatic
    prods = testcase.get_prods()
    for prd in prods[:10]:
        f['product_incl_%s' % str(prd.product_id)] = True
    R = f.submit('submit')
    testcase.assertEqual(R.status_int, 302)
    R = R.follow()
    assert R.status_int == 200
    f = R.forms['frm_discount']
    R.mustcontain('Edit Discount')
    discount_id = f['discount_id'].value
    testcase.assertNotEqual(f['discount_id'].value, '')
    for prd in prods[:10]:
        testcase.assertEqual(f['product_incl_%s' % str(prd.product_id)].checked, True)
    disc = Discount.load(discount_id)
    assert len(disc.get_products()) == 10
    assert disc is not None
    return discount_id


def delete_new_product_discount(testcase, discount_id):
    disc = Discount.load(discount_id)
    testcase.assertNotEqual(disc, None)
    prods = disc.get_products()
    assert len(prods) > 0
    for prd in prods:
        prd.delete()
    disc.delete()
    testcase.commit()

def create_new_cart_discount(testcase, automatic=False):
    R = testcase.get('/crm/discount/new')
    assert R.status_int == 200
    R.mustcontain('Edit Discount')
    f = R.forms['frm_discount']
    testcase.assertEqual(f['discount_id'].value, '')
    f.set('name', 'Test Discount')
    f.set('code', 'tst101')
    f.set('description', 'tst101 description')
    f.set('percent_off', '10')
    f['web_enabled'] = True
    f['cart_discount'] = True
    f['automatic'] = automatic
    R = f.submit('submit')
    testcase.assertEqual(R.status_int, 302)
    R = R.follow()
    assert R.status_int == 200
    f = R.forms['frm_discount']
    R.mustcontain('Edit Discount')
    discount_id = f['discount_id'].value
    testcase.assertNotEqual(f['discount_id'].value, '')
    disc = Discount.load(discount_id)
    assert disc is not None
    return discount_id


def delete_new_cart_discount(testcase, discount_id):
    camp = Discount.load(discount_id)
    testcase.assertNotEqual(camp, None)
    camp.delete()
    testcase.commit()


class TestCrmDiscount(TestController):

    @secure
    def test_show_new(self):
        R = self.get('/crm/discount/new')
        assert R.status_int == 200
        R.mustcontain('Edit Discount')
        f = R.forms['frm_discount']
        self.assertEqual(f['name'].value, '')


    @secure
    def testcreate_new_product_discount(self):
        discount_id = create_new_product_discount(self)
        delete_new_product_discount(self, discount_id)


    @secure
    def testcreate_new_cart_discount(self):
        discount_id = create_new_cart_discount(self)
        delete_new_cart_discount(self, discount_id)


    @secure
    def test_list_with_new(self):
        discount_id = create_new_cart_discount(self)
        R = self.get('/crm/discount/list')
        assert R.status_int == 200
        R.mustcontain('Test Discount')
        delete_new_cart_discount(self, discount_id)


    @secure
    def test_save_existing_cart_discount(self):
        discount_id = create_new_cart_discount(self)
        R = self.get('/crm/discount/list')
        assert R.status_int == 200
        R.mustcontain('Test Discount')
        R = self.get('/crm/discount/edit/%s' % discount_id)
        R.mustcontain('Edit Discount')
        f = R.forms['frm_discount']
        self.assertEqual(f['discount_id'].value, discount_id)
        self.assertEqual(f['name'].value, 'Test Discount')
        self.assertEqual(f['code'].value, 'tst101')
        self.assertEqual(f['web_enabled'].checked, True)
        f.set('name', 'Test Discount New')
        f.set('code', 'tst202')
        f['web_enabled'] = False
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_discount']
        R.mustcontain('Edit Discount')
        self.assertEqual(f['discount_id'].value, discount_id)
        self.assertEqual(f['name'].value, 'Test Discount New')
        self.assertEqual(f['code'].value, 'tst202')
        self.assertEqual(f['web_enabled'].checked, False)
        delete_new_cart_discount(self, discount_id)

        
