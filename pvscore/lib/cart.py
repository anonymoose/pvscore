import datetime
import pvscore.lib.util as util

class Cart(object):
    #                    option['code'] = code.text
    #                    option['name'] = shipping_config['timeframe_choices'][code.text]
    #                    option['charges'] = charges
    #                    option['delivery_days'] = util.nvl(delivery_days)
    def __init__(self, site=None):
        self.items = []
        self.discount_id = None
        self.site_id = site.site_id if site else None
        self.shipping_options = None
        self.shipping_selection = None
        self.shipping_addr1 = None
        self.shipping_addr2 = None
        self.shipping_city = None
        self.shipping_state = None
        self.shipping_zip = None
        self.shipping_country = None
        self.shipping_phone = None


    @property
    def item_count(self):
        return len(self.items)


    def add_item(self, product, campaign, quantity=1, price=None, start_dt=None): #pylint: disable-msg=R0913
        if not price:
            price = product.get_price(campaign)
        price = float(price)
        quantity = float(quantity)
        self.shipping_options = None
        self.shipping_selection = None
        self.items.append({'product': product,
                           'quantity': quantity,
                           'campaign_id': campaign.campaign_id,
                           'dt': datetime.datetime.date(datetime.datetime.now()),
                           'unit_price':price,
                           'start_dt':util.parse_date_as_date(util.nvl(str(start_dt), util.str_today())),
                           'price': price*quantity,
                           'handling':(product.handling_price if product.handling_price else 0)*quantity,
                           'weight':(product.weight if product.weight else 0) * quantity})


    def remove_all(self):
        del self.items
        self.items = []
        self.shipping_options = None
        self.shipping_selection = None


    @property
    def shipping_selection_name(self):
        if self.shipping_options and self.shipping_selection:
            for opt in self.shipping_options:
                if opt['code'] == self.shipping_selection:
                    return opt['name']


    @property
    def shipping_total(self):
        if self.shipping_options and self.shipping_selection:
            for opt in self.shipping_options:
                if opt['code'] == self.shipping_selection:
                    return float(opt['charges'])
        return 0.0

    @property
    def total(self):
        return self.product_total + self.handling_total + self.shipping_total


    @property
    def product_total(self):
        return util.nvl(reduce(lambda x, y: x + y['price'], self.items, 0.0), 0.0)


    @property
    def handling_total(self):
        return util.nvl(reduce(lambda x, y: x + y['handling'], self.items, 0.0), 0.0)


    def has_product_id(self, product_id):
        return len([item for item in self.items if item['product'].product_id == product_id]) > 0


    def remove_item(self, product):
        found = False
        for i in range(len(self.items)-1, -1, -1):
            if str(self.items[i]['product'].product_id) == str(product.product_id):
                del(self.items[i])
                self.shipping_options = None
                self.shipping_selection = None
                found = True
        return found


    # def get_products_with_pictures(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_products_with_pictures_by_campaign(self.campaign)], offset, limit)


    # def get_web_ready_products(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_web_ready_by_campaign(self.campaign)], offset, limit)


    # def get_web_ready_unpriced_products(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_web_ready_unpriced_by_campaign(self.campaign)], offset, limit)


    # def get_specials(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_specials_by_campaign(self.campaign)], offset, limit)


    # def get_featured(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_featured_by_campaign(self.campaign)], offset, limit)


    # def get_best_sellers(self, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_best_sellers_by_campaign(self.campaign)], offset, limit)


    # def get_product_by_attr(self, attr_name, attr_value):
    #     prod = Product.find_by_attr(attr_name, attr_value)
    #     if prod:
    #         return ProductProxy(prod, self.campaign)


    # def get_manufacturer_products(self, mfr_name, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.find_by_manufacturer(self.enterprise_id, mfr_name)], offset, limit)


    # def get_search_results(self, search, offset=None, limit=None):
    #     return util.page_list([ProductProxy(prod, self.campaign) for prod in Product.catalog_search(search, self.campaign.company_id)], offset, limit)


    # def get_manufacturers(self):
    #     return Product.find_manufacturers_by_campaign(self.enterprise_id, self.campaign)


    #def set_cart_default_shipping_timeframe(self, cart):
    #    if not cart.timeframe:
    #        cart.set_shipping_timeframe(self.get_shipping_default_timeframe())
    #        cart.get_shipping_total(None, True)
    #        session.save()

#    def get_categories(self):
#        return ProductCategory.find_by_campaign(self.campaign)



#    def discount(self):
#        if self.discount_id:
#            Discount.load(self.discount_id)


#    def get_total(self):
#        return self.get_product_total() + self.get_handling_total() + self.get_shipping_total()


#    def get_product_total(self):
#        return reduce(lambda x, y: x + y['price'], self.items, 0.0)


#    def get_handling_total(self):
#        return reduce(lambda x, y: x + y['handling'], self.items, 0.0)


#    def get_shipping_total(self, timeframe=None, force_refresh=False):
#        from pvscore.model.cms.site import Site
#        if self.shipping_total != None and not force_refresh:
#            return self.shipping_total
#        if timeframe or self.timeframe or force_refresh:
#            site = Site.load(self.site_id)
#            shipping = site.get_shipping()
#            quote = shipping.get_quote(site, self, timeframe if timeframe else self.timeframe)
#            if quote:
#                self.shipping_total = float(quote[0])
#                session.save()
#                return self.shipping_total
#            else:
#                return 0.0
#        return self.shipping_total
#
#
#    def add_shipping_note(self, order, site=None):
#        if self.timeframe:
#            from pvscore.model.cms.site import Site
#            if not site:
#                if 'site_id' in session:
#                    site = Site.load(self.site_id)
#                else:
#                    return False
#            shipping = site.get_shipping()
#            shipping.add_shipping_note(site, self.timeframe, self.shipping_total, order)
#            order.save()
#            order.commit()
#            return True



# class Catalog(object):
#     def __init__(self, site, campaign):
#         self.site = site
#         self.campaign = campaign
#         self.enterprise_id = campaign.company.enterprise_id


#     def get_product_by_sku(self, sku):
#         return Product.find_by_sku(self.enterprise_id, self.campaign, sku)


#     def get_product(self, product_id):
#         return Product.load(product_id)


#     def get_products(self, offset=None, limit=None):
#         return util.page_list(Product.find_by_campaign(self.campaign, True), offset, limit)


#     def get_new_products(self, offset=None, limit=None):
#         return util.page_list(Product.find_by_campaign(self.campaign, True), offset, limit)


#     def get_category(self, category_id):
#         return ProductCategory.load(category_id)


#     def get_category_products(self, category_id, offset=None, limit=None):
#         pcat = ProductCategory.load(category_id)
#         if pcat:
#             return util.page_list(pcat.products, offset, limit)


#     def get_shipping_timeframe_options(self):
#         shipping = self.site.get_shipping()
#         return shipping.get_timeframe_options(self.site)


#     def get_shipping_default_timeframe(self):
#         shipping = self.site.get_shipping()
#         return shipping.get_default_timeframe(self.site)

