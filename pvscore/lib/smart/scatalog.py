import pvscore.lib.util as util
from pvscore.model.crm.product import Product, ProductCategory

class SmartCatalog(object):

    @staticmethod
    def category_list(campaign):
        return ProductCategory.find_ordered_list(campaign, 'revenue')
        #return ProductCategory.find_ordered_list(campaign, 'quantity')
        #return ProductCategory.find_ordered_list(campaign, 'profit')
        #return ProductCategory.find_by_campaign(campaign)


    @staticmethod
    def new_product_list(campaign, offset, limit):
        return Product.find_new_by_campaign(campaign, offset, limit)


    @staticmethod
    def specials_product_list(campaign, offset=None, limit=None):
        products = Product.find_ordered_list(campaign, 'specials', 'revenue')
        return util.page_list(products if len(products) > 0 else Product.find_ordered_list(campaign, 'new', 'revenue'), offset, limit)


    @staticmethod
    def featured_product_list(campaign, offset=None, limit=None):
        products = Product.find_ordered_list(campaign, 'featured', 'revenue')
        return util.page_list(products if len(products) > 0 else Product.find_new_by_campaign(campaign, 'new', 'revenue'), offset, limit)


    @staticmethod
    def category_product_list(campaign, category_id, offset=None, limit=None):
        category = ProductCategory.load(category_id)
        return util.page_list(category.products if len(category.products) > 0 else Product.find_new_by_campaign(campaign, 'new', 'revenue'), offset, limit)


    @staticmethod
    def also_liked_product_list(product, campaign, offset=None, limit=None):
        products = Product.find_ordered_list(campaign, 'specials', 'revenue')
        return util.page_list(products if len(products) > 0 else Product.find_ordered_list(campaign, 'new', 'revenue'), offset, limit)


    @staticmethod
    def related_product_list(product, campaign, offset=None, limit=None):
        products = Product.find_ordered_list(campaign, 'specials', 'revenue')
        return util.page_list(products if len(products) > 0 else Product.find_ordered_list(campaign, 'new', 'revenue'), offset, limit)


    @staticmethod
    def related_product_list_cart(cart, campaign, offset=None, limit=None):
        products = Product.find_ordered_list(campaign, 'specials', 'revenue')
        return util.page_list(products if len(products) > 0 else Product.find_ordered_list(campaign, 'new', 'revenue'), offset, limit)


class SmartSeo(object):

    @staticmethod
    def obj_seo(obj, site):
        title = util.nvl(obj.seo_title, site.seo_title)
        keywords = util.nvl(obj.seo_keywords, site.seo_title)
        description = util.nvl(obj.seo_description, site.seo_title)
        return (title, keywords, description)


    @staticmethod
    def product_seo(product, site):
        return SmartSeo.obj_seo(product, site)


    @staticmethod
    def category_seo(category, site):
        return SmartSeo.obj_seo(category, site)


class SmartPricing(object):

    @staticmethod
    def product_price(product, campaign):
        return util.money(product.get_price(campaign))


