import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.company import Company, Enterprise
from app.model.crm.campaign import Campaign
from app.model.core.statusevent import StatusEvent
import transaction
from zope.sqlalchemy import mark_changed
from app.model.crm.product import Product, InventoryJournal, ProductCategory

# T app.tests.controllers.test_crm_product

class TestCrmProduct(TestController):
    
    """
    def test_ref(self):
        for e in Enterprise.find_all():
            for p in Product.find_all(e.enterprise_id):
                p.inventory = InventoryJournal.total(p)
                p.save()
        self.commit()
    """

    def _create_new(self):
        # probably a better way to get the preferred enterprise here.
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]

        R = self.get('/crm/product/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Product')
        f = R.forms['frm_product']
        self.assertEqual(f['product_id'].value, '')
        f.set('name', 'Test Product')
        f.set('seo_keywords', 'SEO Test')
        f.set('unit_cost', '10.00')
        f.set('sku', 'TEST-SKU-123')
        f.set('manufacturer', 'Test Manufacturer')
        f.set('attr_name[0]', 'attr0key')
        f.set('attr_value[0]', 'attr0val')
        f.set('attr_name[1]', 'attr1key')
        f.set('attr_value[1]', 'attr1val')

        for c in Campaign.find_by_company(comp):
            f.set('campaign_price[%s]' % c.campaign_id, c.campaign_id)
            f.set('campaign_discount[%s]' % c.campaign_id, round(float(c.campaign_id * 0.50), 2))

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')
        product_id = f['product_id'].value
        self.assertNotEqual(f['product_id'].value, '')
        return product_id


    def _delete_new(self, product_id):
        Product.full_delete(int(str(product_id)))
        self.commit()


    @secure
    def test_save_status(self):
        ent = Enterprise.find_all()[0]
        product_id = self._create_new()
        product = Product.load(product_id)
        events = StatusEvent.find_all_applicable(ent.enterprise_id, product)
        R = self.post('/crm/product/save_status',
                     {'product_id': product_id,
                      'note' : 'Test Note %s' % product_id,
                      'event_id' : events[0].event_id})
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Product Event History')
        R.mustcontain('Test Note %s' % product_id)
        # assert that the edit page has the name of the event in green
        # at the top.
        R = self.get('/crm/product/edit/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Product')
        R.mustcontain(events[0].short_name)
        self._delete_new(product_id)


    @secure
    def test_show_orders(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_orders/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        self._delete_new(product_id)


    @secure
    def test_show_sales(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_sales/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        self._delete_new(product_id)


    @secure
    def test_show_purchases(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_purchases/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        self._delete_new(product_id)


    @secure
    def test_show_history(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_history/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Product Event History')
        self._delete_new(product_id)


    @secure
    def test_show_returns(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_returns/%s' % product_id)
        self.assertEqual(R.status_int, 200)
        self._delete_new(product_id)


    @secure
    def test_show_inventory(self):
        R = self.get('/crm/product/show_inventory')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Product Quick Editor')


    @secure
    def test_inventory_list(self):
        R = self.get('/crm/product/inventory_list')
        self.assertEqual(R.status_int, 200)
        ps = json.loads(R.body)
        self.assertGreater(ps['records'], 100)
        self.assertEqual(ps['records'], len(ps['rows']))


    @secure
    def test_save_inventory(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        cmpn = comp.default_campaign

        R = self.get('/crm/product/inventory_list')
        self.assertEqual(R.status_int, 200)
        ps = json.loads(R.body)
        self.assertGreater(ps['records'], 100)
        self.assertEqual(ps['records'], len(ps['rows']))
        # get the first product ID
        p = ps['rows'][0]['cell']         # ['', '1451', '5-HTP 100 mg- Pharmax', 'SUP-1003', 'Seroyal', '123', '8.0', '15.0', '25.00', '', '25.00', '25.00']
        pid = p[1]
        name = p[2]
        sku = p[3]
        manu = p[4]
        inventory = int(p[5])
        inventory_par = p[6]
        uc = p[7]
        R = self.post('/crm/product/save_inventory',
                      {'id' : pid,
                       'inventory' : inventory + 10,
                       'inventory_par' : inventory_par,
                       'name' : name + ' xxx',
                       'unit_cost' : uc,
                       'cmp_%s' % cmpn.campaign_id : '999'})

        self.assertEquals(R.body, 'True')
        pr = Product.load(pid)
        tot = InventoryJournal.total(pr)
        self.assertEqual(tot, inventory + 10)
        self.assertEqual(999, pr.campaign_prices[cmpn.campaign_id].retail_price)

        R = self.get('/crm/product/edit/%s' % pid)
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')
        self.assertEqual(f['product_id'].value, pid)
        self.assertEqual(f['name'].value, name + ' xxx')

    
    @secure
    def test_save_existing(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        c = Campaign.find_by_company(comp)[0]
        test_price = round(float(c.campaign_id * 0.50), 2)

        product_id = self._create_new()
        R = self.get('/crm/product/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Product')
        R.mustcontain('Product Search')   # make sure product search is in 2 places

        R = self.get('/crm/product/edit/%s' % product_id)
        R.mustcontain('Edit Product')
        f = R.forms['frm_product']
        self.assertEqual(f['product_id'].value, product_id)
        self.assertEqual(f['name'].value, 'Test Product')
        self.assertEqual(f['seo_keywords'].value, 'SEO Test')

        f.set('name', 'Test Product New')
        f.set('seo_keywords', 'SEO Test New')

        for p in Product.find_all_except(Product.load(product_id))[:3]:
            f.set('child_incl_%s' % p.product_id, p.product_id)
            f.set('child_quantity_%s' % p.product_id, p.product_id)

        f.set('prod_inventory', 25)

        #cat = ProductCategory.find_all(ent.enterprise_id)[0]
        #f.set('category_id', cat.category_id)

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')

        self.assertEqual(f['product_id'].value, product_id)
        self.assertEqual(f['name'].value, 'Test Product New')
        self.assertEqual(f['seo_keywords'].value, 'SEO Test New')
        #self.assertEqual(f['category_id'].value, cat.category_id)

        prod = Product.load(product_id)
        self.assertEqual(25, InventoryJournal.total(prod))

        for p in Product.find_all_except(Product.load(product_id))[:3]:
            self.assertEqual(int(f['child_quantity_%s' % p.product_id].value), p.product_id)

        self._delete_new(product_id)


    @secure
    def test_autocomplete_by_name(self):
        product_id = self._create_new()
        R = self.get('/crm/product/autocomplete_by_name',
                      {'search_key': 'test'})
        R.mustcontain('Test Product')
        R = self.get('/crm/product/autocomplete_by_name',
                      {'search_key': 'TEST'})
        R.mustcontain('Test Product')
        R = self.get('/crm/product/autocomplete_by_name',
                      {'search_key': 'tEsT'})
        R.mustcontain('Test Product')
        R = self.get('/crm/product/autocomplete_by_name',
                      {'search_key': 'tEsT'})
        R.mustcontain('Test Product')
        R = self.get('/crm/product/autocomplete_by_name',
                     {'search_key': 'a'})
        R.mustcontain('Activated Charcoal')
        R.mustcontain('Alpha')

        self._delete_new(product_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/product/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Product')
        f = R.forms['frm_product']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_create_new(self):
        product_id = self._create_new()
        self._delete_new(product_id)


    @secure
    def test_list_with_new(self):
        product_id = self._create_new()
        R = self.get('/crm/product/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Product')
        self._delete_new(product_id)

