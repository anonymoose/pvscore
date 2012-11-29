#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import String, DateTime, Float, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
import logging
import pvscore.lib.util as util
import uuid
from pvscore.lib.sqla import GUID

log = logging.getLogger(__name__)

class OrderItem(ORMBase, BaseModel):
    __tablename__ = 'crm_order_item'
    __pk__ = 'order_item_id'

    order_item_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    order_id = Column(GUID, ForeignKey('crm_customer_order.order_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    product_id = Column(GUID, ForeignKey('crm_product.product_id'))
    parent_id = Column(GUID, ForeignKey('crm_order_item.order_item_id'))
    name = Column(String(100))
    unit_cost = Column(Float)
    unit_price = Column(Float)
    unit_discount_price = Column(Float)
    unit_retail_price = Column(Float)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    quantity = Column(Float)
    tax = Column(Float, default=0.0)
    third_party_id = Column(String(100))

    order = relation('CustomerOrder', lazy="joined")
    creator = relation('Users')
    product = relation('Product', lazy="joined")
    status = relation('Status')


    def total(self):
        """ KB: [2012-11-28]: TODO: Change this to where handling_price is an attribute """
        pretax = (util.nvl(self.product.handling_price, 0.0) + util.nvl(self.unit_price, 0.0)) * util.nvl(self.quantity, 1.0)
        return pretax + (pretax * self.tax)


    @property
    def children(self):
        return Session.query(OrderItem).filter(OrderItem.parent_id == self.order_item_id).all()



class OrderItemTermsAcceptance(ORMBase, BaseModel):
    __tablename__ = 'crm_oi_terms_acceptance'
    __pk__ = 'oi_terms_acceptance_id'

    oi_terms_acceptance_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    order_id = Column(GUID, ForeignKey('crm_customer_order.order_id'))
    order_item_id = Column(GUID, ForeignKey('crm_order_item.order_item_id'))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    signature = Column(String(100))


    @staticmethod
    def find_by_order_item_id(order_item_id):
        if not order_item_id:
            return None
        return Session.query(OrderItemTermsAcceptance)\
            .filter(and_(OrderItemTermsAcceptance.order_item_id == order_item_id,
                         OrderItemTermsAcceptance.delete_dt == None)).first()


    @staticmethod
    def is_order_item_id_accepted(order_item_id):
        return OrderItemTermsAcceptance.find_by_order_item_id(order_item_id) != None



    # @staticmethod
    # def find_all_by_order_id(order_id):
    #     return Session.query(OrderItemTermsAcceptance)\
    #         .filter(and_(OrderItemTermsAcceptance.order_id == order_id,
    #                      OrderItemTermsAcceptance.delete_dt == None)).all()


    # @staticmethod
    # def find_by_order(order):
    #     return Session.query(OrderItem).filter(OrderItem.order_id == order.order_id).order_by(OrderItem.create_dt.asc())

    # def has_status(self, event):
    #     from pvscore.model.core.status import Status
    #     sts = Status.find_by_event(self.order.customer, self, event)
    #     return (sts and len(sts) > 0)
