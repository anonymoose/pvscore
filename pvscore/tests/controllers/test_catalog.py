from pvscore.tests import TestController, secure
from pvscore.model.cms.site import Site
from pyramid.httpexceptions import HTTPForbidden
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.product import Product
from pvscore.model.crm.company import Enterprise
import logging
import uuid

log = logging.getLogger(__name__)

# T pvscore.tests.controllers.test_catalog

class TestCatalog(TestController):
    def _get_prod(self, idx=0):
        ent = Enterprise.find_all()[0]
        prods = Product.find_all(ent.enterprise_id)
        assert len(prods) > 0
        prod = prods[idx]


    @secure
    def test_product_page(self):
        prod = self._get_prod()
        R = self.get('/product/%s/%s/catalog_product' % (prod.name, prod.product_id))
        assert R.status_int == 200
        R.mustcontain('product_id=%s' % prod.product_id)
        R.mustcontain('product_name=%s' % prod.name)


    @secure
    def test_products_new(self):
        prod0 = self._get_prod(0)
        prod1 = self._get_prod(1)
        R = self.get('/products/new/catalog_products')
        assert R.status_int == 200
        R.mustcontain('product_id=%s' % prod.product_id)
        R.mustcontain('product_name=%s' % prod.name)
        
        



