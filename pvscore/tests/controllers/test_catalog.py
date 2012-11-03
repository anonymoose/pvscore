from pvscore.tests import TestController
from pvscore.model.crm.product import Product
from pvscore.model.crm.company import Enterprise
import logging


log = logging.getLogger(__name__)

# bin/Tfull pvscore.tests.controllers.test_catalog

class TestCatalog(TestController):
    def _get_prods(self):
        ent = Enterprise.find_all()[0]
        prods = Product.find_all(ent.enterprise_id)
        assert len(prods) > 0
        return prods


    def _get_prod(self, idx=0):
        return self._get_prods()[idx]


    def test_product_page(self):
        prod = self._get_prod()
        R = self.get('/product/%s/%s/catalog_product' % (prod.name, prod.product_id))
        assert R.status_int == 200
        R.mustcontain('product_id=%s' % prod.product_id)
        R.mustcontain('product_name=%s' % prod.name)


    def test_products_new(self):
        #prod0 = self._get_prod(0)
        #prod1 = self._get_prod(1)
        R = self.get('/products/new/catalog_products')
        assert R.status_int == 200
        #R.mustcontain('product_id=%s' % prod0.product_id)
        #R.mustcontain('product_name=%s' % prod0.name)
        #R.mustcontain('product_id=%s' % prod1.product_id)
        #R.mustcontain('product_name=%s' % prod1.name)


    def test_products_featured(self):
        R = self.get('/products/featured/catalog_products')
        assert R.status_int == 200
        prods = self._get_prods()
        prods = [prod for prod in prods if prod.featured]
        assert prods is not None
        assert len(prods) > 0
        prod = prods[0]
        R.mustcontain('product_id=%s' % prod.product_id)
        R.mustcontain('product_name=%s' % prod.name)

        
    def test_products_specials(self):
        R = self.get('/products/specials/catalog_products')
        assert R.status_int == 200
        # no specials in test db.  fix this.


    def test_clear_cart(self):
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        R = self.get('/ecom/cart/clear')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        

    def test_add_to_cart(self):
        R = self.get('/ecom/cart/clear')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        prod = self._get_prod()
        R = self.get('/ecom/cart/add/%s/2' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body


    def test_remove_from_cart(self):
        R = self.get('/ecom/cart/clear')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        prod = self._get_prod()
        R = self.get('/ecom/cart/add/%s/2' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body
        R = self.get('/ecom/cart/remove/%s' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id not in R.body
        
