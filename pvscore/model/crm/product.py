#pylint: disable-msg=E1101,C0103,R0913
import math
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, DateTime, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.crm.pricing import ProductPricing
from pvscore.model.crm.company import Company
from pvscore.model.core.asset import Asset
import pvscore.lib.db as db
from pvscore.thirdparty.dbcache import FromCache, invalidate
from sqlalchemy.orm.collections import attribute_mapped_collection
import pvscore.lib.util as util
import uuid
from pvscore.lib.sqla import GUID

class Product(ORMBase, BaseModel):
    __tablename__ = 'crm_product'
    __pk__ = 'product_id'

    product_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    company_id = Column(GUID, ForeignKey('crm_company.company_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    vendor_id = Column(GUID, ForeignKey('crm_vendor.vendor_id'))
    name = Column(String(200))
    detail_description = Column(Text)
    description = Column(Text)
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)
    mod_dt = Column(DateTime, server_default=text('now()'))
    type = Column(String(20), server_default=text('Parent or Child'))
    manufacturer = Column(String(100))
    unit_cost = Column(Float)
    sku = Column(String(20))
    third_party_id = Column(String(30))
    handling_price = Column(Float)
    weight = Column(Float)
    enabled = Column(Boolean, default=True)
    singleton = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    special = Column(Boolean, default=False)
    web_visible = Column(Boolean, default=True)
    inventory_par = Column(Float)
    show_negative_inventory = Column(Boolean, default=False)
    seo_title = Column(String(512))
    seo_keywords = Column(String(1000))
    seo_description = Column(String(1000))
    subscription = Column(Boolean, default=False)
    inventory = Column(Integer) # this is derived from InventoryJournal and updated in "create_new"

    company = relation('Company', lazy='joined', backref=backref('products', order_by='Product.name'))
    status = relation('Status')
    vendor = relation('Vendor')

    campaign_prices = relation("ProductPricing", lazy="joined",
                               collection_class=attribute_mapped_collection('campaign_id'))

    _pricing = None
    _images = None

    @staticmethod
    def find_names_by_name(enterprise_id, name, limit):
        sql = """select p.product_id, p.name,
                p.unit_cost, pp.retail_price, pp.wholesale_price, pp.discount_price
                from
                crm_product p, crm_company com, crm_enterprise ent, crm_campaign cmp, crm_product_pricing pp
                where lower(p.name) like '%%{n}%%'
                and p.delete_dt is null
                and p.company_id = com.company_id
                and cmp.campaign_id = com.default_campaign_id
                and pp.campaign_id = cmp.campaign_id
                and pp.product_id = p.product_id
                and com.enterprise_id = '{ent_id}'
                order by p.name limit {lim}""".format(n=name.lower(),
                                                      lim=limit,
                                                      ent_id=enterprise_id)
        return db.get_result_dict(['product_id', 'name', 'unit_cost', 'retail_price', 'wholesale_price', 'discount_price'], sql)


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Product).options(FromCache('Product.find_all', enterprise_id)) \
            .join((Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                         Company.enterprise_id == enterprise_id
                         )) \
                         .order_by(Product.name) \
                         .all()


    @staticmethod
    def find_by_vendor(enterprise_id, vendor):
        return Session.query(Product) \
            .join((Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                         Company.enterprise_id == enterprise_id,
                         Product.vendor_id == vendor.vendor_id)) \
                         .order_by(Product.name) \
                         .all()


    @staticmethod
    def find_by_manufacturer(enterprise_id, mfr_name, for_web=True):
        return Session.query(Product) \
            .options(FromCache('Product.find_by_manufacturer', '%s/%s' % (mfr_name, enterprise_id))) \
            .join((Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                         Product.enabled == True,
                         Product.manufacturer.like('%'+mfr_name+'%'),
                         Company.enterprise_id == enterprise_id,
                         or_(Product.web_visible == True, Product.web_visible==for_web)
                         )) \
                         .order_by(Product.name).all()


    @staticmethod
    def find_all_except(product):
        return Session.query(Product).join((Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                         Company.enterprise_id == product.company.enterprise_id,
                         Product.product_id != product.product_id)).order_by(Product.name).all()


    def find_eligible_children(self):
        """ KB: [2011-02-07]: Don't cache this because everytime we add a product, we have to invalidate ALL
        product's caches.  Thats too gross for an admin function.
        """
        if self.product_id:
            return Session.query(Product) \
                .join((Company, Product.company_id == Company.company_id)) \
                .filter(and_(Product.delete_dt == None,
                             Company.enterprise_id == self.company.enterprise_id,
                             Product.product_id != self.product_id,
                             Product.enabled == True,
                             or_(Product.type == 'Top Level', Product.type == 'Parent or Child'))).order_by(Product.name).all()
        else: return []


    @staticmethod
    def find_new_by_campaign(campaign, offset=0, limit=10):
        return Session.query(Product) \
            .options(FromCache("Product.Campaign_new", campaign.campaign_id)) \
            .join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                          Product.enabled == True,
                          Company.enterprise_id == campaign.company.enterprise_id,
                          ProductPricing.delete_dt == None,
                          ProductPricing.campaign == campaign,
                          Product.web_visible == True,
                          ProductPricing.retail_price != None,
                          ProductPricing.retail_price > 0)).order_by(Product.create_dt.desc()).offset(offset).limit(limit).all()


    @staticmethod
    def find_by_campaign(campaign, for_catalog=False):
        return Product._find_by_campaign_impl(campaign, for_catalog)


    @staticmethod
    def find_specials_by_campaign(campaign, for_catalog=True):
        return Product._find_by_campaign_impl(campaign, for_catalog, True, False)


    @staticmethod
    def find_featured_by_campaign(campaign, for_catalog=True):
        return Product._find_by_campaign_impl(campaign, for_catalog, False, True)


    @staticmethod
    def _find_by_campaign_impl(campaign, for_catalog, specials=False, featured=False):
        enterprise_id = campaign.company.enterprise_id
        ckey = 'Product.Campaign'
        clause = and_(Product.delete_dt == None,
                      Product.enabled == True,
                      Company.enterprise_id == enterprise_id,
                      ProductPricing.delete_dt == None,
                      ProductPricing.campaign == campaign)
        if specials:
            ckey = 'Product.Campaign_Specials'
            clause = and_(Product.delete_dt == None,
                          Product.enabled == True,
                          Product.special == True,
                          Company.enterprise_id == enterprise_id,
                          ProductPricing.delete_dt == None,
                          ProductPricing.campaign == campaign,
                          and_(ProductPricing.discount_price != None, ProductPricing.discount_price > 0),
                          Product.web_visible == True)
        elif featured:
            ckey = 'Product.Campaign_Featured'
            clause = and_(Product.delete_dt == None,
                          Product.enabled == True,
                          Product.featured == True,
                          Company.enterprise_id == enterprise_id,
                          ProductPricing.delete_dt == None,
                          ProductPricing.campaign == campaign,
                          Product.web_visible == True)
        if for_catalog:
            ckey += '_for_catalog'
            clause = and_(clause,
                          #or_(Product.inventory == None, Product.inventory > 0, Product.show_negative_inventory == True),
                          ProductPricing.retail_price != None,
                          ProductPricing.retail_price > 0)
        return Session.query(Product) \
            .options(FromCache(ckey, campaign.campaign_id)) \
            .join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
            .filter(clause).order_by(Product.name) \
            .all()


    @staticmethod
    def catalog_search(enterprise_id, search):
        # SWAP THIS OUT FOR SPHINX.
        srch = '%'+search.lower().replace("\'", '').replace("\\", '')+'%'
        res = Session.query(Product)\
            .join((Company, Product.company_id == Company.company_id))\
            .filter(and_(Product.web_visible == True,
                         Company.enterprise_id == enterprise_id,
                         or_(Product.description.ilike(srch),
                             Product.seo_title.ilike(srch),
                             Product.seo_keywords.ilike(srch),
                             Product.seo_description.ilike(srch),
                             Product.name.ilike(srch),
                             Product.sku.ilike(srch))))\
                         .all()
        return res


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Product.find_all', self.company.enterprise_id)
        invalidate(self, 'Product.find_all_for_web', self.company.enterprise_id)
        invalidate(self, 'ProductChild.find_children', self.product_id)
        invalidate(self, 'Product.find_by_manufacturer', '%s/%s' % (self.manufacturer, self.company.enterprise_id))
        invalidate(self, 'Product.find_by_sku', '%s/%s' % (self.manufacturer, self.company.enterprise_id))
        if len(self.images) > 0:
            for img in self.images:
                img.invalidate_caches()
        if kwargs and 'vendor_id' in kwargs:
            invalidate(self, 'Product.find_by_vendor', '%s/%s' % (self.company.enterprise_id, kwargs['vendor_id']))
        for pri in self.prices:
            pri.invalidate_caches()
            campaign_id = pri.campaign_id
            invalidate(self, 'Product.Campaign_new', campaign_id)
            invalidate(self, 'Product.Campaign_Featured', campaign_id)
            invalidate(self, 'Product.Campaign_Specials', campaign_id)
            invalidate(self, 'Product.Campaign', campaign_id)
            invalidate(self, 'Product.Campaign_Featured_for_catalog', campaign_id)
            invalidate(self, 'Product.Campaign_Specials_for_catalog', campaign_id)
            invalidate(self, 'Product.Campaign_for_catalog', campaign_id)
            invalidate(self, 'Product.BestSellers', campaign_id)
            invalidate(self, 'Product.WebReady', campaign_id)
            invalidate(self, 'Product.WebReadyUnpriced', campaign_id)
            invalidate(self, 'Product.HasPicture', campaign_id)


    @property
    def prices(self):
        return ProductPricing.find_all(self)


    @staticmethod
    def find_by_name(campaign, name):  #, for_web=True):
        enterprise_id = campaign.company.enterprise_id
        return Session.query(Product).join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
            .filter(and_(Product.delete_dt == None,
                         Product.enabled == True,
                         Product.name == name,
                         Company.company_id == campaign.company_id,
                         Company.enterprise_id == enterprise_id,
                         ProductPricing.delete_dt == None)).first()


    @staticmethod
    def find_by_sku(enterprise_id, campaign, sku, for_web=True):
        return Session.query(Product).join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
            .options(FromCache('Product.find_by_sku', '%s/%s' % (sku, enterprise_id))) \
            .filter(and_(Product.delete_dt == None,
                         Product.enabled == True,
                         Product.sku == sku,
                         Company.company_id == campaign.company_id,
                         Company.enterprise_id == campaign.company.enterprise_id,
                         or_(Product.web_visible == True, Product.web_visible==for_web),
                         ProductPricing.delete_dt == None)).first()


    @property
    def primary_image(self):
        imgs = self.images
        if imgs and len(imgs) > 0:
            return imgs[0]


    def get_sales_report(self):
        """ KB: [2011-03-02]: daily sales total by product. """
        return db.get_result_set(('create_dt', 'campaign', 'quantity', 'revenue', 'cost', 'profit'),
            """select o.create_dt, cmp.name as campaign,
                               sum(oi.quantity) as quantity,
                               sum(oi.unit_price*oi.quantity) as revenue,
                               sum(oi.unit_cost*oi.quantity) as cost,
                               sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit
                               from
                               crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p
                               where
                               o.customer_id = cust.customer_id and
                               o.order_id = oi.order_id and
                               o.campaign_id = cmp.campaign_id and
                               cmp.company_id = '{company_id}'
                               and oi.product_id = p.product_id
                               and p.product_id = '{product_id}'
                               and o.delete_dt is null
                               and oi.delete_dt is null
                               group by o.create_dt, cmp.name
                               order by o.create_dt desc""".format(company_id=self.company_id,
                                                                   product_id=self.product_id))


    def get_orders_report(self):
        return db.get_result_set(('order_id', 'create_dt', 'customer_id', 'email', 'campaign', 'quantity', 'revenue', 'cost', 'profit'),
                  """select o.order_id, o.create_dt, cust.customer_id, cust.email, cmp.name as campaign,
                     oi.quantity,
                     oi.unit_price*oi.quantity as revenue,
                     oi.unit_cost*oi.quantity as cost,
                     (oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity) as profit
                     from
                     crm_customer_order o, crm_customer cust, crm_order_item oi, crm_campaign cmp, crm_product p
                     where
                     o.customer_id = cust.customer_id and
                     o.order_id = oi.order_id and
                     o.campaign_id = cmp.campaign_id and
                     cmp.company_id = '{company_id}'
                     and oi.product_id = p.product_id
                     and p.product_id = '{product_id}'
                     and o.delete_dt is null
                     and oi.delete_dt is null
                     order by o.create_dt desc""".format(company_id=self.company_id,
                                                         product_id=self.product_id))



    @property
    def images(self):
        if not self._images:
            self._images = Asset.find_for_object(self)
        return self._images


    def get_max_retail_price(self):
        ppri = ProductPricing.find_max_retail_price(self)
        return ppri.retail_price if ppri else 0.0


    def get_price(self, campaign):
        """ KB: [2011-02-02]: Returns the discounted price if there is one, otherwise returns retail price """
        if not campaign.campaign_id in self.campaign_prices:
            return -1
        pri = self.campaign_prices[campaign.campaign_id]
        return pri.discount_price if pri.discount_price else pri.retail_price


    def get_retail_price(self, campaign):
        """ KB: [2011-02-02]: Returns the retail price regardless of discount """
        if not campaign.campaign_id in self.campaign_prices:
            return -1
        return self.campaign_prices[campaign.campaign_id].retail_price


    def get_discount_price(self, campaign):
        """ KB: [2011-02-02]: Returns the discount price """
        if not campaign.campaign_id in self.campaign_prices:
            return -1
        return self.campaign_prices[campaign.campaign_id].discount_price


    def set_price(self, campaign, price, discount=None):
        ppri = ProductPricing.find(campaign, self)
        if ppri == None:
            ppri = ProductPricing()
        ppri.campaign = campaign
        ppri.product = self
        ppri.retail_price = price
        ppri.discount_price = discount
        ppri.save()
        ppri.invalidate_caches()


    def set_price_only(self, campaign, price):
        """ KB: [2011-08-27]: Set price, but dont bother with discount """
        ppri = ProductPricing.find(campaign, self)
        if ppri == None:
            ppri = ProductPricing()
        ppri.campaign = campaign
        ppri.product = self
        ppri.retail_price = price
        ppri.save()


    def remove_price(self, campaign):
        if campaign.campaign_id in self.campaign_prices:
            del self.campaign_prices[campaign.campaign_id]


    @staticmethod
    def get_types():
        return ['Top Level', 'Parent or Child', 'Child Only']


    def can_have_children(self):
        return (self.type and (self.type == 'Top Level' or self.type == 'Parent or Child'))


    def clear_children(self):
        if self.product_id:
            ProductChild.clear_by_parent(self.product_id)


    def add_child(self, other_product_id, other_product_quantity=1):
        return ProductChild.create_new(self.product_id, other_product_id, other_product_quantity)


    def get_children(self):
        return ProductChild.find_children(self.product_id)


    @staticmethod
    def full_delete(product_id):
        """ KB: [2011-01-28]: This only works for products that have never been purchased. """
        Session.execute("delete from crm_product_child where parent_id = '%s' or child_id = '%s'" % (product_id, product_id))
        Session.execute("delete from crm_product_pricing where product_id = '%s'" % product_id)
        Session.execute("delete from crm_product_inventory_journal where product_id = '%s'" % product_id)
        Session.execute("delete from crm_product where product_id = '%s'" % product_id)


class ProductChild(ORMBase, BaseModel):
    __tablename__ = 'crm_product_child'
    __pk__ = 'product_child_id'

    product_child_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    parent_id = Column(GUID, ForeignKey('crm_product.product_id'))
    child_id = Column(GUID, ForeignKey('crm_product.product_id'))
    child_quantity = Column(Integer, server_default=text('1'))

    parent = relation('Product', primaryjoin=Product.product_id == parent_id)
    child = relation('Product', lazy='joined', primaryjoin=Product.product_id == child_id)

    @staticmethod
    def find_children(parent_id):
        return Session.query(ProductChild).options(FromCache('ProductChild.find_children', parent_id)) \
            .filter(and_(Product.delete_dt == None,
                         ProductChild.parent_id == parent_id)).all()


    @staticmethod
    def clear_by_parent(parent_id):
        Session.execute("delete from crm_product_child where parent_id = '%s'" % parent_id)
        invalidate(ProductChild(), 'ProductChild.find_children', parent_id) # not my finest moment.


    @staticmethod
    def create_new(parent_id, child_id, child_quantity=1):
        prdc = ProductChild()
        prdc.parent_id = parent_id
        prdc.child_id = child_id
        prdc.child_quantity = child_quantity if child_quantity else 1
        prdc.save()
        return prdc


    def invalidate_caches(self):
        invalidate(self, 'ProductChild.find_children', self.parent_id)


class ProductCategory(ORMBase, BaseModel):
    __tablename__ = 'crm_product_category'
    __pk__ = 'category_id'

    category_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    company_id = Column(GUID, ForeignKey('crm_company.company_id'))
    name = Column(String(200))
    description = Column(Text)
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)
    mod_dt = Column(DateTime, server_default=text('now()'))
    seo_title = Column(String(512))
    seo_keywords = Column(String(1000))
    seo_description = Column(String(1000))

    company = relation('Company', lazy='joined')

    def clear_products(self):
        if self.category_id:
            ProductCategoryJoin.clear_by_category(self)


    @property
    def products(self):
        if not self.category_id:
            return []
        return Session.query(Product)\
            .options(FromCache("ProductCategory.Products.%s" % self.category_id))\
            .join((ProductCategoryJoin, Product.product_id == ProductCategoryJoin.product_id),
                  (ProductCategory, ProductCategoryJoin.category_id == ProductCategory.category_id),
                  (Company, ProductCategory.company_id == Company.company_id))\
                  .filter(ProductCategory.category_id == self.category_id).all()


    def add_product(self, product_id):
        return ProductCategoryJoin.create_new(self.category_id, product_id)


    @staticmethod
    def find_by_product(product):
        return Session.query(ProductCategory)\
            .join((ProductCategoryJoin, ProductCategory.category_id == ProductCategoryJoin.category_id),
                  (Product, ProductCategoryJoin.product_id == Product.product_id),
                  (Company, ProductCategory.company_id == Company.company_id))\
                  .filter(and_(ProductCategoryJoin.product == product,
                               Company.company_id == product.company_id)).all()


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(ProductCategory) \
            .join((Company, ProductCategory.company_id == Company.company_id)) \
            .filter(and_(ProductCategory.delete_dt == None,
                         Company.enterprise_id == enterprise_id)) \
                         .order_by(ProductCategory.name) \
                         .all()


    @staticmethod
    def find_by_campaign(campaign):
        return Session.query(ProductCategory) \
            .options(FromCache('Product.find_all', campaign.company.enterprise_id)) \
            .join((Company, ProductCategory.company_id == Company.company_id)) \
            .filter(and_(ProductCategory.delete_dt == None,
                         Company.company_id == campaign.company_id)) \
                         .order_by(ProductCategory.name) \
                         .all()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'ProductCategory.find_all', self.company.enterprise_id)
        invalidate(self, 'ProductCategory.find_by_campaign', '%s' % (self.company.default_campaign_id))


    @staticmethod
    def full_delete(category_id):
        """ KB: [2011-01-28]: This only works for products that have never been purchased. """
        Session.execute("delete from crm_product_category_join where category_id = '%s'" % category_id)
        Session.execute("delete from crm_product_category where category_id = '%s'" % category_id)


class ProductCategoryJoin(ORMBase, BaseModel):
    __tablename__ = 'crm_product_category_join'
    __pk__ = 'pcj_id'

    pcj_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    category_id = Column(GUID, ForeignKey('crm_product_category.category_id'))

    product = relation('Product')
    category = relation('ProductCategory', lazy='joined')

    @staticmethod
    def create_new(category_id, product_id):
        pcj = ProductCategoryJoin()
        pcj.category_id = category_id
        pcj.product_id = product_id
        pcj.save()
        return pcj


    @staticmethod
    def clear_by_category(category):
        Session.execute("delete from crm_product_category_join where category_id = '%s'" % category.category_id)



class ProductReturn(ORMBase, BaseModel):
    __tablename__ = 'crm_product_return'
    __pk__ = 'return_id'

    return_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    order_id = Column(GUID, ForeignKey('crm_customer_order.order_id'))
    journal_id = Column(GUID, ForeignKey('crm_journal.journal_id'))
    quantity = Column(Float, server_default=text('0.0'))
    credit_amount = Column(Float, server_default=text('0.0'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)

    product = relation('Product')
    order = relation('CustomerOrder')
    creator = relation('Users')
    journal_entry = relation('Journal')

    @staticmethod
    def find(product):
        return Session.query(ProductReturn) \
            .filter(and_(ProductReturn.product == product,
                         ProductReturn.delete_dt == None)) \
                         .order_by(ProductReturn.create_dt.desc()) \
                         .all()


    @staticmethod
    def create_new(product, order, quantity, credit_amount, journal_entry, user):
        pret = ProductReturn()
        pret.product = product
        pret.order = order
        pret.quantity = quantity
        pret.credit_amount = credit_amount
        pret.creator = user
        pret.journal_entry = journal_entry
        pret.save()
        return pret


class InventoryJournal(ORMBase, BaseModel):
    __tablename__ = 'crm_product_inventory_journal'
    __pk__ = 'inv_journal_id'

    inv_journal_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    return_id = Column(GUID, ForeignKey('crm_product_return.return_id'))
    order_item_id = Column(GUID, ForeignKey('crm_order_item.order_item_id'))
    quantity = Column(Float, server_default=text('0.0'))
    type = Column(String(20), default='Sale')
    note = Column(String(150))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)

    product = relation('Product')
    order_item = relation('OrderItem')
    creator = relation('Users')
    ret = relation('ProductReturn')

    @staticmethod
    def total(product):
        ret = Session.query("c").from_statement("SELECT sum(quantity) c FROM crm_product_inventory_journal where product_id = '%s'" % product.product_id).one()
        return ret[0] if ret != None else 0.0


    @staticmethod
    def cleanup(order_item, tipe):
        Session.execute("delete from crm_product_inventory_journal where order_item_id = '%s' and type = '%s'" % (order_item.order_item_id, tipe))


    @staticmethod
    def create_new(product, tipe, quantity, order_item=None, note=None, creator=None, ret=None):
        jrnl = InventoryJournal()
        jrnl.type = tipe
        jrnl.note = note
        jrnl.product = product
        jrnl.creator = creator
        jrnl.order_item = order_item
        jrnl.ret = ret
        if 'Sale' == tipe:
            jrnl.quantity = -1*math.fabs(float(quantity))
        elif 'Inventory Adjust' == tipe:
            # user just manually adjusted inventory.  Add or subtract the difference.
            current = util.nvl(InventoryJournal.total(product), 0)
            #     -10  = 20      - 30
            #      10  = 30      - 20
            jrnl.quantity = float(quantity)-float(current)
        else:
            jrnl.quantity = math.fabs(float(quantity))
        jrnl.save()
        jrnl.flush()
        # while we are here, update the cached inventory column.
        product.inventory = InventoryJournal.total(product)
        product.save()
        return jrnl






        # if for_web:
        #     return Session.query(Product).join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
        #         .filter(and_(Product.delete_dt == None,
        #                      Product.enabled == True,
        #                      Product.name == name,
        #                      Company.company_id == campaign.company_id,
        #                      Company.enterprise_id == enterprise_id,
        #                      Product.web_visible == True,
        #                      ProductPricing.delete_dt == None)).first()
        # else:


    # @staticmethod
    # def find_manufacturers_by_campaign(enterprise_id, campaign, for_web=True):
    #     eid = enterprise_id
    #     cid = campaign.campaign_id
    #     mfrs = db.get_raw_value_list('mfr', """SELECT distinct(manufacturer) mfr
    #                                                      FROM crm_product_pricing pp,
    #                                                      crm_product p, crm_company c
    #                                                      where pp.product_id = p.product_id
    #                                                            and p.company_id = c.company_id
    #                                                            and (p.web_visible=true or p.web_visible = {wv})
    #                                                            and c.enterprise_id = {eid}
    #                                                            and pp.campaign_id = {cid}
    #                                                            and p.delete_dt is null
    #                                                            and p.manufacturer is not null
    #                                                            and pp.delete_dt is null order by mfr""".format(eid=eid,
    #                                                                                                            cid=cid,
    #                                                                                                            wv='true' if for_web else 'false'))
    #     return mfrs


    # @staticmethod
    # def find_next(enterprise_id, product_id):
    #     return Session.query(Product) \
    #         .join((Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Company.enterprise_id == enterprise_id,
    #                      Product.product_id > int(product_id))) \
    #                      .order_by(Product.product_id.asc()) \
    #                      .first()


    # @staticmethod
    # def find_previous(enterprise_id, product_id):
    #     return Session.query(Product) \
    #         .join((Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Company.enterprise_id == enterprise_id,
    #                      Product.product_id < int(product_id))) \
    #                      .order_by(Product.product_id.desc()) \
    #                      .first()

    # @staticmethod
    # def find_by_attr(attr_name, attr_value):
    #     product_id = AttributeValue.find_fk_id_by_value('Product', attr_name, attr_value)
    #     if product_id:
    #         return Product.load(product_id)


    # @staticmethod
    # def search(enterprise_id, name, description, company_id, sku, current_user):
    #     n_clause = cid_clause = d_clause = s_clause = v_clause = ''
    #     if name:
    #         n_clause = "and lower(p.name) like '%{name}%'".format(name=name.lower())
    #     if description:
    #         d_clause = "and lower(p.description) like '%{desc}%'".format(desc=description.lower())
    #     if company_id:
    #         cid_clause = "and p.company_id = %d" % int(company_id)
    #     if sku:
    #         s_clause = "and p.sku like '%{sku}%'".format(sku=sku)
    #     if current_user and current_user.is_vendor_user():
    #         v_clause = "and p.vendor_id = %s" % current_user.vendor_id

    #     sql = """SELECT p.* FROM crm_product p, crm_company com
    #              where  p.company_id = com.company_id
    #              and com.enterprise_id = {ent_id}
    #              {n} {d} {s} {v} {cid} order by p.name""".format(n=n_clause, d=d_clause,
    #                                          s=s_clause, cid=cid_clause, v=v_clause,
    #                                          ent_id=enterprise_id)
    #     return Session.query(Product).from_statement(sql).all()




    # def get_customers(self):
    #     from pvscore.model.crm.customer import Customer
    #     sql = """SELECT cu.*
    #              FROM crm_product p, crm_company com, crm_campaign cam, crm_customer cu, crm_customer_order co, crm_order_item oi
    #              where p.company_id = com.company_id
    #              and cam.company_id = com.company_id
    #              and cam.campaign_id = cu.campaign_id
    #              and cu.customer_id = co.customer_id
    #              and co.order_id = oi.order_id
    #              and oi.product_id = p.product_id
    #              and cam.delete_dt is null
    #              and co.cancel_dt is null
    #              and cu.delete_dt is null
    #              and oi.delete_dt is null
    #              and p.product_id = {prodid}
    #              and com.enterprise_id = {ent_id}
    #              and p.company_id={cid}""".format(prodid=self.product_id,
    #                                               cid=self.company_id,
    #                                               ent_id=self.company.enterprise_id)
    #     return Session.query(Customer) \
    #         .from_statement(sql).all()


    # def get_customers_created_today(self):
    #     from pvscore.model.crm.customer import Customer
    #     sql = """SELECT cu.*
    #              FROM crm_product p, crm_company com, crm_campaign cam, crm_customer cu, crm_customer_order co, crm_order_item oi
    #              where p.company_id = com.company_id
    #              and cam.company_id = com.company_id
    #              and cam.campaign_id = cu.campaign_id
    #              and cu.customer_id = co.customer_id
    #              and co.order_id = oi.order_id
    #              and oi.product_id = p.product_id
    #              and cam.delete_dt is null
    #              and cu.delete_dt is null
    #              and oi.delete_dt is null
    #              and p.product_id = {prodid}
    #              and com.enterprise_id = {ent_id}
    #              and p.company_id={cid}
    #              and oi.create_dt > now()::date - 1""".format(prodid=self.product_id,
    #                                               cid=self.company_id,
    #                                               ent_id=self.company.enterprise_id)
    #     return Session.query(Customer) \
    #         .from_statement(sql).all()

    # @staticmethod
    # def find_all(enterprise_id):
    #     if for_web:
    #         return Session.query(Product).options(FromCache('Product.find_all_for_web', enterprise_id)) \
    #             .join((Company, Product.company_id == Company.company_id)) \
    #             .filter(and_(Product.delete_dt == None,
    #                          Company.enterprise_id == enterprise_id,
    #                          Product.web_visible == True)) \
    #                          .order_by(Product.name) \
    #                          .all()
    #     else:
    #     return Session.query(Product).options(FromCache('Product.find_all', enterprise_id)) \
    #         .join((Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Company.enterprise_id == enterprise_id
    #                      )) \
    #                      .order_by(Product.name) \
    #                      .all()


    #@property
    #def inventory(self):
    #    try:
    #        return InventoryJournal.total(self)
    #    except:
    #        return 0.0


    # @staticmethod
    # def find_names_by_name_and_campaign(enterprise_id, name, limit, campaign):
    #     sql = """select p.product_id, p.name, p.unit_cost, pp.retail_price, pp.wholesale_price, pp.discount_price from
    #                                              crm_product p, crm_company com, crm_enterprise ent,
    #                                              crm_product_pricing pp
    #                                              where lower(p.name) like '%%{n}%%'
    #                                              and p.delete_dt is null
    #                                              and p.company_id = com.company_id
    #                                              and pp.campaign_id = {campaign_id}
    #                                              and pp.product_id = p.product_id
    #                                              and com.enterprise_id = {ent_id}
    #                                              order by p.name limit {lim}""".format(n=name.lower(),
    #                                                                                    lim=limit,
    #                                                                                    campaign_id=campaign.campaign_id,
    #                                                                                    ent_id=enterprise_id)
    #     return db.get_result_dict(['product_id', 'name', 'unit_cost', 'retail_price', 'wholesale_price', 'discount_price'], sql)


    # @staticmethod
    # def find_all_active(company):
    #     return Session.query(Product) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Product.company_id == company.company_id))\
    #                      .order_by(Product.vendor_id, Product.name) \
    #                  .all()


    # @staticmethod
    # def find_best_sellers_by_campaign(campaign, for_web=True):
    #     enterprise_id = campaign.company.enterprise_id
    #     return Session.query(Product) \
    #         .options(FromCache('Product.BestSellers', campaign.campaign_id)) \
    #         .join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Product.enabled == True,
    #                      Company.enterprise_id == enterprise_id, 
    #                      ProductPricing.delete_dt == None,
    #                      ProductPricing.campaign == campaign,
    #                      #or_(Product.inventory == None, Product.inventory > 0, Product.show_negative_inventory == True),
    #                      or_(Product.web_visible == True, Product.web_visible==for_web),
    #                      ProductPricing.retail_price != None,
    #                      ProductPricing.retail_price > 0)) \
    #                      .order_by(Product.name) \
    #                      .all()


    # @staticmethod
    # def find_web_ready_by_campaign(campaign):
    #     enterprise_id = campaign.company.enterprise_id
    #     return Session.query(Product) \
    #         .options(FromCache('Product.WebReady', campaign.campaign_id)) \
    #         .join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Product.enabled == True,
    #                      Company.enterprise_id == enterprise_id, 
    #                      ProductPricing.delete_dt == None,
    #                      ProductPricing.campaign == campaign,
    #                      Product.web_visible == True,
    #                      Product.detail_description != None,
    #                      ProductPricing.retail_price != None,
    #                      ProductPricing.retail_price > 0,
    #                      exists().where(and_(Asset.fk_type == 'Product', Asset.fk_id == Product.product_id)))) \
    #                      .order_by(Product.name) \
    #                      .all()


    # @staticmethod
    # def find_products_with_pictures_by_campaign(campaign):
    #     """ KB: [2011-09-28]: Just has a picture.  Fuck it. """
    #     enterprise_id = campaign.company.enterprise_id
    #     return Session.query(Product) \
    #         .options(FromCache('Product.HasPicture', campaign.campaign_id)) \
    #         .join((ProductPricing, ProductPricing.product_id == Product.product_id),(Company, Product.company_id == Company.company_id)) \
    #         .filter(and_(Product.delete_dt == None,
    #                      Product.enabled == True,
    #                      Company.enterprise_id == enterprise_id,
    #                      ProductPricing.delete_dt == None,
    #                      ProductPricing.campaign == campaign,
    #                      Product.web_visible == True,
    #                      exists().where(and_(Asset.fk_type == 'Product', Asset.fk_id == Product.product_id)))) \
    #                      .order_by(Product.name) \
    #                      .all()


    # def _init_pricing(self, campaign):
    #     if self._pricing == None:
    #         self._pricing = ProductPricing.find(campaign, self)
    #     return self._pricing != None


    # def get_default_price(self):
    #     return self.get_unit_price(self.company.default_campaign)


    # @staticmethod
    # def clear_by_product(product):
    #     ProductCategoryJoin.clear_by_product(product)


    # @staticmethod
    # def clear_by_product(product):
    #     Session.execute("delete from crm_product_category_join where product_id = %d" % int(product.product_id))

    # @staticmethod
    # def get_types():
    #     return ['Sale',              # customer purchased item
    #             'Item Receipt',      # item received after purchasing it from vendor
    #             'Inventory Adjust',  # manual inventory change.
    #             'Return',            # someone returned an item after having taken possession
    #             'Cancelled Order',   # user cancelled an entire order
    #             'Cancelled Item'     # user removed a single item from the order
    #             ]

    
