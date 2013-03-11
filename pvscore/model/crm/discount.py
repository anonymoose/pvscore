#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import String, DateTime, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.crm.product import Product
import pvscore.lib.util as util
import uuid
from pvscore.lib.sqla import GUID

class Discount(ORMBase, BaseModel):
    __tablename__ = 'crm_discount'
    __pk__ = 'discount_id'

    discount_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    enterprise_id = Column(GUID, ForeignKey('crm_enterprise.enterprise_id'))
    vendor_id = Column(GUID, ForeignKey('crm_vendor.vendor_id'))
    name = Column(String(200))
    code = Column(String(50))
    description = Column(Text)
    mod_dt = Column(DateTime, server_default=text('now()'))
    percent_off = Column(Float)
    amount_off = Column(Float)
    shipping_percent_off = Column(Float)
    which_item = Column(String(30))
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    web_enabled = Column(Boolean, default=True)
    store_enabled = Column(Boolean, default=True)
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)

    vendor = relation('Vendor')

    @staticmethod
    def get_which_item_types():
        return ['All Items', 'First Item', 'Most Expensive Item', 'Least Expensive Item']


    @staticmethod
    def find_all_active(enterprise_id):
        return Session.query(Discount) \
            .filter(and_(Discount.delete_dt == None, 
                         Discount.enterprise_id == enterprise_id,
                         or_(Discount.end_dt == None,
                             Discount.end_dt >= util.now())))\
                         .order_by(Discount.name) \
                     .all() 


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Discount) \
            .filter(and_(Discount.delete_dt == None, 
                         Discount.enterprise_id == enterprise_id))\
                         .order_by(Discount.name) \
                     .all() 


    def get_products(self):
        return DiscountProduct.find_products(self.discount_id)


    def add_product(self, product_id):
        if (not DiscountProduct.find_child(self.discount_id, product_id)):
            return DiscountProduct.create_new(self.discount_id, product_id)


    def clear_product(self, product_id):
        if self.discount_id:
            DiscountProduct.clear(self.discount_id, product_id)


class DiscountProduct(ORMBase, BaseModel):
    __tablename__ = 'crm_discount_product'
    __pk__ = 'discount_product_id'

    discount_product_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    discount_id = Column(GUID, ForeignKey('crm_discount.discount_id'))
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    create_dt = Column(DateTime, server_default=text('now()'))
    delete_dt = Column(DateTime)

    product = relation('Product', lazy='joined')
    discount = relation('Discount', lazy='joined')

    @staticmethod
    def find_products(discount_id):
        #.options(FromCache('Product.find_children', parent_id)) 
        return Session.query(DiscountProduct) \
            .join((Product, DiscountProduct.product_id == Product.product_id)) \
            .filter(and_(DiscountProduct.discount_id == discount_id,
                         Product.delete_dt == None,
                         Product.enabled == True,
                         Product.type != 'Attr')) \
                         .order_by(Product.name) \
                         .all()


    @staticmethod
    def find_child(discount_id, product_id):
        return Session.query(DiscountProduct) \
            .filter(and_(DiscountProduct.discount_id == discount_id,
                         DiscountProduct.product_id == product_id)).first()


    @staticmethod
    def clear(discount_id, product_id):
        Session.execute("delete from crm_discount_product where discount_id = '%s' and product_id = '%s'" % (discount_id, product_id))


    @staticmethod
    def create_new(discount_id, product_id):
        discp = DiscountProduct()
        discp.discount_id = discount_id
        discp.product_id = product_id
        discp.save()
        return discp




