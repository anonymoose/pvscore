import pvscore.lib.util as util
from pvscore.model.crm.product import Product, ProductCategory

class SmartCatalog(object):

    @staticmethod
    def category_list(campaign):
        return ProductCategory.find_by_campaign(campaign)


    @staticmethod
    def new_product_list(campaign, offset, limit):
        return Product.find_new_by_campaign(campaign, offset, limit)


    @staticmethod
    def specials_product_list(campaign, offset=None, limit=None):
        products = Product.find_specials_by_campaign(campaign)
        return util.page_list(products if len(products) > 0 else Product.find_new_by_campaign(campaign, 0, 10), offset, limit)


    @staticmethod
    def featured_product_list(campaign, offset=None, limit=None):
        products = Product.find_featured_by_campaign(campaign)
        return util.page_list(products if len(products) > 0 else Product.find_new_by_campaign(campaign, 0, 10), offset, limit)



class SmartSeo(object):

    @staticmethod
    def product_seo(product, site):
        title = util.nvl(product.seo_title, site.seo_title)
        keywords = util.nvl(product.seo_keywords, site.seo_title)
        description = util.nvl(product.seo_description, site.seo_title)
        return (title, keywords, description)


    @staticmethod
    def category_seo(category, site):
        title = util.nvl(category.seo_title, site.seo_title)
        keywords = util.nvl(category.seo_keywords, site.seo_title)
        description = util.nvl(category.seo_description, site.seo_title)
        return (title, keywords, description)


class SmartPricing(object):

    @staticmethod
    def product_price(product, campaign):
        return util.money(product.get_price(campaign))


