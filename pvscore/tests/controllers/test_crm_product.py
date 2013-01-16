from pvscore.tests import TestController, secure, secure_as_root
from pvscore.model.core.asset import Asset
from pvscore.model.crm.company import Enterprise, Company
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.product import Product, InventoryJournal
from pvscore.model.core.statusevent import StatusEvent
import simplejson as json
import os

# T pvscore.tests.controllers.test_crm_product

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
        ent = Enterprise.find_by_name('Healthy U Store')
        comp = Company.find_all(ent.enterprise_id)[0]
        R = self.get('/crm/product/new')
        assert R.status_int == 200
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

        for camp in Campaign.find_by_company(comp):
            f.set('campaign_price[%s]' % camp.campaign_id, 20.0)
            f.set('campaign_discount[%s]' % camp.campaign_id, 10.0)

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')
        product_id = f['product_id'].value
        self.assertNotEqual(f['product_id'].value, '')
        return product_id


    def _delete_new(self, product_id):
        Product.full_delete(product_id)
        self.commit()


    @secure
    def test_save_status(self):
        self._test_save_status()


    @secure_as_root
    def test_save_status_as_root(self):
        self._test_save_status()


    def _test_save_status(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        product_id = self._create_new()
        product = Product.load(product_id)
        events = StatusEvent.find_all_applicable(ent.enterprise_id, product)
        R = self.post('/crm/product/save_status',
                     {'product_id': product_id,
                      'note' : 'Test Note %s' % product_id,
                      'event_id' : events[0].event_id})
        assert R.status_int == 200
        R.mustcontain('Product Event History')
        R.mustcontain('Test Note %s' % product_id)
        # assert that the edit page has the name of the event in green
        # at the top.
        R = self.get('/crm/product/edit/%s' % product_id)
        assert R.status_int == 200
        R.mustcontain('Edit Product')
        R.mustcontain(events[0].short_name)
        self._delete_new(product_id)


    @secure
    def test_show_orders(self):
        self._test_show_orders()


    @secure_as_root
    def test_show_orders_as_root(self):
        self._test_show_orders()


    def _test_show_orders(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_orders/%s' % product_id)
        assert R.status_int == 200
        self._delete_new(product_id)


    @secure
    def test_show_sales(self):
        self._test_show_sales()


    @secure_as_root
    def test_show_sales_as_root(self):
        self._test_show_sales()


    def _test_show_sales(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_sales/%s' % product_id)
        assert R.status_int == 200
        self._delete_new(product_id)


    @secure
    def test_show_purchases(self):
        self._test_show_purchases()


    @secure_as_root
    def test_show_purchases_as_root(self):
        self._test_show_purchases()


    def _test_show_purchases(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_purchases/%s' % product_id)
        assert R.status_int == 200
        self._delete_new(product_id)


    @secure
    def test_show_history(self):
        self._test_show_history()


    @secure_as_root
    def test_show_history_as_root(self):
        self._test_show_history()


    def _test_show_history(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_history/%s' % product_id)
        assert R.status_int == 200
        R.mustcontain('Product Event History')
        self._delete_new(product_id)


    @secure
    def test_show_returns(self):
        self._test_show_returns()


    @secure_as_root
    def test_show_returns_as_root(self):
        self._test_show_returns()


    def _test_show_returns(self):
        product_id = self._create_new()
        R = self.get('/crm/product/show_returns/%s' % product_id)
        assert R.status_int == 200
        self._delete_new(product_id)


    @secure
    def test_show_inventory(self):
        self._test_show_inventory()


    @secure_as_root
    def test_show_inventory_as_root(self):
        self._test_show_inventory()


    def _test_show_inventory(self):
        R = self.get('/crm/product/show_inventory')
        assert R.status_int == 200
        R.mustcontain('Product Quick Editor')


    @secure
    def test_save_inventory(self):
        self._test_save_inventory()


    @secure_as_root
    def test_save_inventory_as_root(self):
        self._test_save_inventory()


    def _test_save_inventory(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        cmpns = Campaign.find_all(ent.enterprise_id)

        R = self.get('/crm/product/inventory_list')
        assert R.status_int == 200
        prods = json.loads(R.body)
        self.assertGreater(prods['records'], 100)
        self.assertEqual(prods['records'], len(prods['rows']))
        # get the first product ID
        prod = prods['rows'][1]['cell']         # ['', '1451', '5-HTP 100 mg- Pharmax', 'SUP-1003', 'Seroyal', '123', '8.0', '15.0', '25.00', '', '25.00', '25.00']
        pid = prod[1]
        name = prod[2]
        #sku = prod[3]
        #manu = prod[4]
        inventory = int(prod[5])
        inventory_par = prod[6]
        unitcost = prod[7]
        R = self.post('/crm/product/save_inventory',
                      {'id' : pid,
                       'inventory' : inventory + 10,
                       'inventory_par' : inventory_par,
                       'name' : name + ' xxx',
                       'unit_cost' : unitcost,
                       'cmp_%s' % cmpns[0].campaign_id : '999',
                       'cmp_%s' % cmpns[1].campaign_id : ''})

        self.assertEquals(R.body, 'True')
        prod = Product.load(pid)
        tot = InventoryJournal.total(prod)
        self.assertEqual(tot, inventory + 10)
        self.assertEqual(999, prod.campaign_prices[cmpns[0].campaign_id].retail_price)
        self.assertEqual(True, cmpns[1].campaign_id not in prod.campaign_prices.keys())

        R = self.get('/crm/product/edit/%s' % pid)
        assert R.status_int == 200
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')
        self.assertEqual(f['product_id'].value, pid)
        self.assertEqual(f['name'].value, name + ' xxx')


    @secure
    def test_save_existing(self):
        self._test_save_existing()


    @secure_as_root
    def test_save_existing_as_root(self):
        self._test_save_existing()


    def _test_save_existing(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        cmpns = Campaign.find_all(ent.enterprise_id)

        product_id = self._create_new()
        R = self.get('/crm/product/list')
        assert R.status_int == 200
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

        for prod in Product.find_all_except(Product.load(product_id))[:3]:
            f.set('child_incl_%s' % prod.product_id, prod.product_id)
            f.set('child_quantity_%s' % prod.product_id, 2)

        f.set('campaign_price[%s]' % cmpns[0].campaign_id, "123")
        f.set('campaign_price[%s]' % cmpns[1].campaign_id, None)

        f.set('prod_inventory', 25)

        #cat = ProductCategory.find_all(ent.enterprise_id)[0]
        #f.set('category_id', cat.category_id)

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')

        self.assertEqual(f['product_id'].value, product_id)
        self.assertEqual(f['name'].value, 'Test Product New')
        self.assertEqual(f['seo_keywords'].value, 'SEO Test New')
        self.assertEqual(f['campaign_price[%s]' % cmpns[0].campaign_id].value, "123.00")
        self.assertEqual(f['campaign_price[%s]' % cmpns[1].campaign_id].value, "")

        #self.assertEqual(f['category_id'].value, cat.category_id)

        prod = Product.load(product_id)
        self.assertEqual(25, InventoryJournal.total(prod))

        for prod in Product.find_all_except(Product.load(product_id))[:3]:
            self.assertEqual(int(f['child_quantity_%s' % prod.product_id].value), 2)

        #put pricing back.
        R = self.get('/crm/product/edit/%s' % product_id)
        R.mustcontain('Edit Product')
        f = R.forms['frm_product']
        self.assertEqual(f['product_id'].value, product_id)
        f.set('campaign_price[%s]' % cmpns[0].campaign_id, "123")
        f.set('campaign_price[%s]' % cmpns[1].campaign_id, "234")
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_product']
        R.mustcontain('Edit Product')
        self.assertEqual(f['product_id'].value, product_id)
        self.assertEqual(f['campaign_price[%s]' % cmpns[1].campaign_id].value, "234.00")
        self._delete_new(product_id)


    @secure
    def test_show_new(self):
        self._test_show_new()


    @secure_as_root
    def test_show_new_as_root(self):
        self._test_show_new()


    def _test_show_new(self):
        R = self.get('/crm/product/new')
        assert R.status_int == 200
        R.mustcontain('Edit Product')
        f = R.forms['frm_product']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_autocomplete_by_name(self):
        self._test_autocomplete_by_name()


    @secure_as_root
    def test_autocomplete_by_name_as_root(self):
        self._test_autocomplete_by_name()


    def _test_autocomplete_by_name(self):
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
    def test_create_new(self):
        self._test_create_new()


    @secure_as_root
    def test_create_new_as_root(self):
        self._test_create_new()


    def _test_create_new(self):
        product_id = self._create_new()
        self._delete_new(product_id)


    @secure
    def test_delete_picture(self):
        self._test_delete_picture()


    @secure_as_root
    def test_delete_picture_as_root(self):
        self._test_delete_picture()


    def _test_delete_picture(self):
        product_id = self._create_new()
        # http://stackoverflow.com/questions/2488978/nose-tests-file-uploads
        files = [("Filedata", "testimage.jpg", "not really a jpg")]
        R = self.app.post('/crm/product/upload_picture/%s' % str(product_id),
                          upload_files=files)
        assert R.status_int == 200
        asset_id = R.body
        ass = Asset.load(asset_id)
        assert ass is not None
        assert os.path.exists(ass.filesystem_path)
        R = self.app.get('/crm/product/delete_picture/%s/%s' % (str(product_id), str(ass.id)))
        R.mustcontain('True')
        assert not os.path.exists(ass.filesystem_path)
        self._delete_new(product_id)


    @secure
    def test_list_with_new(self):
        self._test_list_with_new()


    @secure_as_root
    def test_list_with_new_as_root(self):
        self._test_list_with_new()


    def _test_list_with_new(self):
        product_id = self._create_new()
        R = self.get('/crm/product/list')
        assert R.status_int == 200
        R.mustcontain('Test Product')
        self._delete_new(product_id)


    @secure
    def test_upload_picture(self):
        self._test_upload_picture()


    @secure_as_root
    def test_upload_picture_as_root(self):
        self._test_upload_picture()


    def _test_upload_picture(self):
        product_id = self._create_new()
        # http://stackoverflow.com/questions/2488978/nose-tests-file-uploads
        files = [("Filedata", "testimage.jpg", "not really a jpg")]
        R = self.app.post('/crm/product/upload_picture/%s' % str(product_id),
                          upload_files=files)
        assert R.status_int == 200
        asset_id = R.body
        ass = Asset.load(asset_id)
        assert ass is not None
        assert os.path.exists(ass.filesystem_path)
        ass.delete()
        assert not os.path.exists(ass.filesystem_path)
        self._delete_new(product_id)


    # @secure
    # def test_inventory_list(self):
    #     R = self.get('/crm/product/inventory_list')
    #     assert R.status_int == 200
    #     prods = json.loads(R.body)
    #     self.assertGreater(prods['records'], 100)
    #     self.assertEqual(prods['records'], len(prods['rows']))

