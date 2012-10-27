#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import String, Date, Float
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.lib.dbcache import FromCache, invalidate
import uuid
from pvscore.lib.sqla import GUID

class ProductPricing(ORMBase, BaseModel):
    __tablename__ = 'crm_product_pricing'
    __pk__ = 'product_pricing_id'

    product_pricing_id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    campaign_id = Column(GUID, ForeignKey('crm_campaign.campaign_id'))
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    wholesale_price = Column(Float)
    retail_price = Column(Float)
    discount_price = Column(Float)
    bill_method_type = Column(String(3))
    bill_freq_type = Column(String(3))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)

    campaign = relation('Campaign')
    product = relation('Product')

    @staticmethod
    def find(campaign, product):
        return Session.query(ProductPricing).options(FromCache('ProductPricing.find', '%s/%s' % (campaign.campaign_id, product.product_id))) \
            .filter(and_(ProductPricing.campaign == campaign, 
                         ProductPricing.product == product, 
                         ProductPricing.delete_dt == None)).first()

    @staticmethod
    def find_all(product):
        return Session.query(ProductPricing) \
            .filter(and_(ProductPricing.product == product, 
                         ProductPricing.delete_dt == None)).all()


    def invalidate_caches(self, **kwargs):
        pid = self.product_id if self.product_id else (self.product.product_id if self.product else None)
        if pid:
            invalidate(self, 'ProductPricing.find', '%s/%s' % (self.campaign_id, pid))
            invalidate(self, 'ProductPricing.find_max_retail_price', '%s' % pid)

    @staticmethod
    def find_max_retail_price(product):
        return Session.query(ProductPricing).options(FromCache('ProductPricing.find_max_retail_price', '%s' % product.product_id)) \
            .filter(and_(ProductPricing.product == product, 
                         ProductPricing.delete_dt == None)).order_by(ProductPricing.retail_price.desc()).first()

            
    # def delete(self):
    #     self.delete_dt = datetime.datetime.date(datetime.datetime.now()) 
    #     self.save()

