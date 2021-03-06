#pylint: disable-msg=C0103
import logging
from pvscore.tests.controllers.test_crm_discount import create_new_product_discount, delete_new_product_discount, create_new_cart_discount
from pvscore.tests import TestController, secure, customer_logged_in, PVS_ROOT_UID, PVS_ROOT_PWD
from pvscore.model.crm.company import Enterprise
from pvscore.model.crm.product import ProductCategory
from pvscore.model.crm.discount import Discount
from pvscore.tests.controllers.test_cms_content import content_create_new, content_delete_new
from pvscore.model.cms.content import Content
from pvscore.lib.billing_api import StripeBillingApi
from pvscore.lib.cart import Cart

log = logging.getLogger(__name__)

# bin/Tfull pvscore.tests.controllers.test_catalog

class TestCatalog(TestController):

    def test_misc(self):
        # really contrived example to get coverage in pvscore.lib.cart
        cust = self.get_customer()
        order = cust.get_active_orders()[0]
        cart = Cart(self.site)
        prod = self.get_prod()
        camp = cust.campaign
        prod = order.items[0].product
        # KB: [2013-02-20]: MOD ATTR TestCatalog.test_misc : Allow for attributes.
        cart.add_item(prod, cust.campaign)
        assert int(cart.total) == int(prod.get_price(camp))


    def test_search(self):
        prod = self.get_prod()
        R = self.get('/ecom/search/catalog_search_results?search=%s' % prod.name)
        assert R.status_int == 200
        R.mustcontain(prod.name)
        R = self.get('/ecom/search/catalog_search_results?search=BOGUSSSSS')
        assert R.status_int == 200


    @secure
    def test_page(self):
        content_id = content_create_new(self)
        cnt = Content.load(content_id)
        R = self.get('/ecom/page/content?content_name=%s' % cnt.name)
        assert R.status_int == 200
        R.mustcontain(cnt.name)
        R.mustcontain(self.site.site_id)
        content_delete_new(content_id)


    @secure
    def test_content(self):
        content_id = content_create_new(self)
        cnt = Content.load(content_id)
        R = self.get('/ecom/content/%s/catalog_content?content_name=%s' % (cnt.name, cnt.name))
        assert R.status_int == 200
        R.mustcontain(cnt.name)
        R.mustcontain(str(self.site.site_id))
        content_delete_new(content_id)


    def test_login(self):
        R = self.get('/ecom/login/catalog_login?nextlink=/ecom/page/catalog_login_follow')
        R.mustcontain('this is the login page')


    @customer_logged_in
    def test_already_logged_in(self):
        R = self.get('/ecom/login/catalog_login?nextlink=/ecom/page/catalog_login_follow')
        R.mustcontain('this is the second page')


    @customer_logged_in
    def test_purchase_cart(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)
        self._clear_cart()
        prod = self.get_prod()
        self._add_product(prod, 2)
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body
        assert 'quantity=%s/2.0' % prod.product_id in R.body
        R = self.get('/ecom/cart/update/%s/9' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body
        assert 'quantity=%s/9.0' % prod.product_id in R.body
        R = self.post("/crm/customer/purchase_cart",
                      {'redir' : '/ecom/page/catalog_thanks',
                      'accept_terms' : '1',
                      'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')})
        assert R.status_int == 200
        R.mustcontain('Thanks for your purchase')


    def test_product_page(self):
        prod = self.get_prod()
        R = self.get('/product/%s/%s/catalog_product' % (prod.name, prod.product_id))
        assert R.status_int == 200
        R.mustcontain('product_id=%s' % prod.product_id)
        R.mustcontain('product_name=%s' % prod.name)


    def test_products_new(self):
        #prod0 = self.get_prod(0)
        #prod1 = self.get_prod(1)
        R = self.get('/products/new/catalog_products')
        assert R.status_int == 200
        #R.mustcontain('product_id=%s' % prod0.product_id)
        #R.mustcontain('product_name=%s' % prod0.name)
        #R.mustcontain('product_id=%s' % prod1.product_id)
        #R.mustcontain('product_name=%s' % prod1.name)


    def test_products_featured(self):
        R = self.get('/products/featured/catalog_products')
        assert R.status_int == 200
        prods = self.get_prods()
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


    def test_category(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        campaign = ent.companies[0].default_campaign
        categories = ProductCategory.find_by_campaign(campaign)
        assert len(categories) > 0
        category = categories[0]
        products = category.get_web_products(campaign)
        R = self.get('/category/%s/%s/catalog_category' % (category.name, category.category_id))
        assert R.status_int == 200
        for prod in products:
            assert str(prod.product_id) in R.body


    def test_clear_cart(self):
        self._clear_cart()


    def test_add_to_cart(self):
        self._clear_cart()
        prod = self.get_prod()
        self._add_product(prod, 2)
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body


    def test_remove_from_cart(self):
        self._clear_cart()
        prod = self.get_prod()
        self._add_product(prod, 2)
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body
        R = self.get('/ecom/cart/remove/%s' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id not in R.body


    @customer_logged_in
    def test_shipping(self):
        self._clear_cart()
        prod = self.get_prod()
        self._add_product(prod, 2)
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id=%s' % prod.product_id in R.body
        self._select_shipping()


    def _select_shipping(self):
        R = self.get('/checkout/catalog_checkout_shipping')
        assert R.status_int == 200
        R.mustcontain('Ground')
        R.mustcontain('3 Day Select')
        R.mustcontain('Second Day Air')
        R.mustcontain('Next Day Air Saver')
        # this yields "03" by looking for Ground/03 in the returned string
        ground = [line.split('/')[1] for line in R.body.split("\n") if line.startswith('Ground/')][0]
        R = self.get('/ecom/cart/save_shipping', {'shipping_code' : ground, 'redir' : '/'})
        assert R.status_int == 200


    def test_alternate_product_search_by_name(self):
        #http://healthyustore.net/product/Saccharomyces%20Boulardii%20
        R = self.get('/product/Saccharomyces%20Boulardii%20')
        assert R.status_int == 200
        R.mustcontain('Saccharomyces')


    def test_full_checkout_with_product_discount(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)

        # set up the discount for the products
        self.login_crm(PVS_ROOT_UID, PVS_ROOT_PWD)
        discount_id = create_new_product_discount(self, True)
        discount = Discount.load(discount_id)
        assert discount is not None
        discounted_products = discount.get_products()
        assert len(discounted_products) > 0
        self.logout_crm_soft()

        self.login_customer()
        self._clear_cart()

        prod = discounted_products[0].product
        self._add_product(prod, 100)
        R = self.get('/cart/catalog_cart')
        R.mustcontain('total=2250.0')
        R.mustcontain('product_base_total=2500.0')
        R.mustcontain('product_total=2250.0')
        R.mustcontain('product_discounts=250.0')

        R = self.get('/ecom/cart/update/%s/10' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'

        R = self.get('/cart/catalog_cart')
        R.mustcontain('total=225.0')
        R.mustcontain('product_base_total=250.0')
        R.mustcontain('product_total=225.0')
        R.mustcontain('product_discounts=25.0')

        self._select_shipping()

        R = self.post("/crm/customer/purchase_cart",
                      {'redir' : '/ecom/page/catalog_thanks',
                      'accept_terms' : '1',
                      'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')})
        R.mustcontain('order total_discounts_applied = 25.0')
        R.mustcontain('order total_payments_due = 0.0')
        R.mustcontain('order total_item_price = 225.0')
        #R.mustcontain('order total_payments_applied = 374.82')
        #R.mustcontain('order total_price = 374.82')
        #R.mustcontain('order total_shipping_price = 14.824')

        self.logout_customer(False)

        self.login_crm(PVS_ROOT_UID, PVS_ROOT_PWD)
        delete_new_product_discount(self, discount_id)
        self.logout_crm_soft()


    def test_full_checkout_with_automatic_cart_discount(self):
        ent = Enterprise.find_by_name('Healthy U Store')
        api = StripeBillingApi(ent)

        # set up the discount for the products
        self.login_crm(PVS_ROOT_UID, PVS_ROOT_PWD)
        discount_id = create_new_cart_discount(self, True)
        discount = Discount.load(discount_id)
        assert discount is not None
        assert int(discount.percent_off) == 10
        self.logout_crm_soft()

        self.login_customer()
        self._clear_cart()

        prod = self.get_prod()
        self._add_product(prod, 100)
        R = self.get('/cart/catalog_cart')
        R.mustcontain('total=2500.0')
        R.mustcontain('product_base_total=2500.0')
        R.mustcontain('product_total=2500.0')
        R.mustcontain('product_discounts=0.0')

        R = self.get('/ecom/cart/update/%s/10' % prod.product_id)
        assert R.status_int == 200
        assert R.body == 'True'

        R = self.get('/cart/catalog_cart')
        R.mustcontain('total=250.0')
        R.mustcontain('product_base_total=250.0')
        R.mustcontain('product_total=250.0')
        R.mustcontain('product_discounts=0.0')

        self._select_shipping()

        R = self.post("/crm/customer/purchase_cart",
                      {'redir' : '/ecom/page/catalog_thanks',
                      'accept_terms' : '1',
                      'bill_cc_token' : api.create_token('4242424242424242', '12', '2019', '123')})

        R.mustcontain('order total_discounts_applied = 0')
        R.mustcontain('order total_payments_due = 0.0')
        R.mustcontain('order total_item_price = 250.0')
        #R.mustcontain('order total_payments_applied = 418.53')
        #R.mustcontain('order total_price = 418.53')
        #R.mustcontain('order total_shipping_price = 18.53')

        self.logout_customer(False)

        self.login_crm(PVS_ROOT_UID, PVS_ROOT_PWD)
        #delete_new_cart_discount(self, discount_id)
        self.logout_crm_soft()


    def _clear_cart(self):
        # clear out the cart and assert it's clear
        R = self.get('/ecom/cart/clear')
        assert R.status_int == 200
        assert 'product_id' not in R.body
        R = self.get('/cart/catalog_cart')
        assert R.status_int == 200
        assert 'product_id' not in R.body


    def _add_product(self, prod, quantity):
        R = self.get('/ecom/cart/add/%s/%s' % (prod.product_id, quantity))
        assert R.status_int == 200
        assert R.body == 'True'


