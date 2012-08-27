import pdb, math
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Numeric, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.crm.pricing import ProductPricing
from app.model.crm.company import Company
from app.model.core.attribute import Attribute, AttributeValue
from app.model.core.asset import Asset
import app.lib.db as db
from app.lib.dbcache import FromCache, invalidate
import app.lib.util as util

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
    def find_all_active(enterprise_id, company):
        return Session.query(Discount) \
            .filter(and_(Discount.delete_dt == None, 
                         Discount.enterprise_id == enterprise_id,
                         or_(Discount.end_dt == None,
                             Discount.end_dt >= util.now())))\
                         .order_by(Discount.name) \
                     .all() 

    @staticmethod
    def find_all(enterprise_id, for_web=False):
        return Session.query(Discount) \
            .filter(and_(Discount.delete_dt == None, 
                         Discount.enterprise_id == enterprise_id))\
                         .order_by(Discount.name) \
                     .all() 

    def invalidate_caches(self, **kwargs):
        pass

    @staticmethod
    def search(enterprise_id, name, description, company_id, sku, current_user):
        n_clause = cid_clause = d_clause = s_clause = v_clause = ''
        if name:
            n_clause = "and lower(p.name) like '%{name}%'".format(name=name.lower())

        sql = """SELECT d.* FROM crm_discount d, crm_company com
                 where
                 d.enterprise_id = {ent_id}
                 {n} order by p.name""".format(n=n_clause, ent_id=enterprise_id)
        return Session.query(Discount).from_statement(sql).all()
