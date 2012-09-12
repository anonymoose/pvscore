#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
import pvscore.lib.util as util

class Discount(ORMBase, BaseModel):
    __tablename__ = 'crm_discount'
    __pk__ = 'discount_id'

    discount_id = Column(Integer, primary_key = True)
    name = Column(String(200))
    code = Column(String(50))
    description = Column(Text)
    enterprise_id = Column(Integer, ForeignKey('crm_enterprise.enterprise_id'))
    mod_dt = Column(DateTime, server_default=text('now()'))
    percent_off = Column(Float)
    amount_off = Column(Float)
    which_item = Column(String(30))
    end_dt = Column(Date)
    web_enabled = Column(Boolean, default=True)
    store_enabled = Column(Boolean, default=True)
    vendor_id = Column(Integer, ForeignKey('crm_vendor.vendor_id'))
    product_id = Column(Integer, ForeignKey('crm_product.product_id'))
    create_dt = Column(Date, server_default=text('now()'))
    delete_dt = Column(Date)
    start_dt = Column(Date)

    vendor = relation('Vendor')
    product = relation('Product')


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

