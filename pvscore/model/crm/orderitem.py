#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Float, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
import logging

log = logging.getLogger(__name__)

class OrderItem(ORMBase, BaseModel):
    __tablename__ = 'crm_order_item'
    __pk__ = 'order_item_id'

    order_item_id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey('crm_customer_order.order_id'))
    name = Column(String(100))
    unit_cost = Column(Float)
    unit_price = Column(Float)
    unit_discount_price = Column(Float)
    unit_retail_price = Column(Float)
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    quantity = Column(Float)
    status_id = Column(Integer, ForeignKey('core_status.status_id'))
    user_created = Column(String(50), ForeignKey('core_user.username'))
    product_id = Column(Integer, ForeignKey('crm_product.product_id'))
    parent_id = Column(Integer, ForeignKey('crm_order_item.order_item_id'))
    tax = Column(Float, default=0.0)

    order = relation('CustomerOrder', lazy="joined")
    creator = relation('Users')
    product = relation('Product', lazy="joined")
    status = relation('Status')

    def total(self):
        try:
            return self.unit_price * self.quantity
        except Exception as exc:
            log.debug(exc)
            return 0.0


    # @staticmethod
    # def find_by_order(order):
    #     return Session.query(OrderItem).filter(OrderItem.order_id == order.order_id).order_by(OrderItem.create_dt.asc())


    @property
    def children(self):
        return Session.query(OrderItem).filter(OrderItem.parent_id == self.order_item_id).all()


    # def has_status(self, event):
    #     from pvscore.model.core.status import Status
    #     sts = Status.find_by_event(self.order.customer, self, event)
    #     return (sts and len(sts) > 0)


class OrderItemTermsAcceptance(ORMBase, BaseModel):
    __tablename__ = 'crm_oi_terms_acceptance'
    __pk__ = 'oi_terms_acceptance_id'

    oi_terms_acceptance_id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey('crm_customer_order.order_id'))
    order_item_id = Column(Integer, ForeignKey('crm_order_item.order_item_id'))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(Date)
    signature = Column(String(100))


    # @staticmethod
    # def find_all_by_order_id(order_id):
    #     return Session.query(OrderItemTermsAcceptance)\
    #         .filter(and_(OrderItemTermsAcceptance.order_id == order_id,
    #                      OrderItemTermsAcceptance.delete_dt == None)).all()


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

