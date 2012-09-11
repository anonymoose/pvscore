from pvscore.tests import TestController, secure
from pvscore.model.crm.product import Product, ProductCategory
from pvscore.model.crm.company import Enterprise

# T pvscore.tests.controllers.test_crm_category

class TestCrmCategory(TestController):
    
    def _create_new(self):
        # probably a better way to get the preferred enterprise here.
        R = self.get('/crm/product/category/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Product Category')
        f = R.forms['frm_category']
        self.assertEqual(f['category_id'].value, '')
        f.set('name', 'Test Category')
        f.set('seo_keywords', 'SEO Test')
        f.set('description', 'Test Description')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_category']
        R.mustcontain('Edit Product Category')
        category_id = f['category_id'].value
        self.assertNotEqual(f['category_id'].value, '')
        return category_id


    def _delete_new(self, category_id):
        ProductCategory.full_delete(int(str(category_id)))
        self.commit()


    @secure
    def test_save_existing(self):
        ent = Enterprise.find_all()[0]

        category_id = self._create_new()
        R = self.get('/crm/product/category/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Category')
        R.mustcontain('Product Search')

        R = self.get('/crm/product/category/edit/%s' % category_id)
        R.mustcontain('Edit Product Category')
        f = R.forms['frm_category']
        self.assertEqual(f['category_id'].value, category_id)
        self.assertEqual(f['name'].value, 'Test Category')
        self.assertEqual(f['seo_keywords'].value, 'SEO Test')
        self.assertEqual(f['description'].value, 'Test Description')
        
        f.set('name', 'Test Category New')
        f.set('seo_keywords', 'SEO Test New')

        for prd in Product.find_all(ent.enterprise_id)[:3]:
            f.set('child_incl_%s' % prd.product_id, prd.product_id)

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_category']
        R.mustcontain('Edit Product Category')

        self.assertEqual(f['category_id'].value, category_id)
        self.assertEqual(f['name'].value, 'Test Category New')
        self.assertEqual(f['seo_keywords'].value, 'SEO Test New')

        for prd in Product.find_all(ent.enterprise_id)[:3]:
            self.assertEqual(f['child_incl_%s' % prd.product_id].checked, True)

        self._delete_new(category_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/product/category/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Product Category')
        f = R.forms['frm_category']
        self.assertEqual(f['name'].value, '')
        self.assertEqual(f['category_id'].value, '')


    @secure
    def test_create_new(self):
        category_id = self._create_new()
        self._delete_new(category_id)


    @secure
    def test_list_with_new(self):
        category_id = self._create_new()
        R = self.get('/crm/product/category/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Category')
        self._delete_new(category_id)

