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
    @secure
    def test_product_page(self):
        ent = Enterprise.find_all()[0]
        prods = Product.find_all(ent.enterprise_id)
        product_id = prods[0].product_id

        R = self.get('/product/%s' % product_id)
        assert R.status_int == 200
        R.mustcontain('product_id=%s' % product_id)
        R.mustcontain('product_name=%s' % prods[0].name)




