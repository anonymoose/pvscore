#pylint: disable-msg=E1101
#pylint: disable-msg=C0103
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Float, Text
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
import app.lib.util as util

class Journal(ORMBase, BaseModel):
    __tablename__ = 'crm_journal'
    __pk__ = 'journal_id'

    journal_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey('crm_customer.customer_id'))
    order_id = Column(Integer, ForeignKey('crm_customer_order.order_id'))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    user_created = Column(String(50), ForeignKey('core_user.username'))
    type = Column(String(30))
    note = Column(Text)
    method = Column(String(25))
    amount = Column(Float)

    customer = relation('Customer')
    creator = relation('Users')
    order = relation('CustomerOrder')


    def cancel(self):
        self.delete_dt = util.today()
        self.save()


    @staticmethod
    def get_types():
        return ['FullPayment', 'PartialPayment', 'Refund', 'CreditIncrease', 'CreditDecrease', 'Discount']


    @staticmethod
    def get_payment_methods():
        return ['Credit Card (offline)', 'Credit Card', 'Cash', 'Apply Balance', 'Check', 'Wire', 'Discount'] # , 'Credit Card (on-file)' is added if there is one on file.


    @staticmethod
    def create_new(amount, customer, order, creator, typ='FullPayment', payment_method='Credit Card', note=None):   #pylint: disable-msg=R0913
        jrnl = Journal()
        jrnl.type = typ
        jrnl.note = note
        jrnl.customer = customer
        jrnl.creator = creator
        jrnl.order = order
        jrnl.amount = amount
        jrnl.method = payment_method
        jrnl.save()
        return jrnl


    @staticmethod
    def find_all_by_customer(customer):
        return Session.query(Journal).filter(and_(Journal.customer==customer,
                                                  Journal.delete_dt == None))\
                                                  .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_all_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
               	                                  Journal.order==order,
                                                  Journal.delete_dt == None))\
                                                  .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_total_applied_to_order(order):
        """ KB: [2011-03-08]: This could be done in the DB but we may want to have different handling by type,
        which is easier to express in python.
        """

        jes = Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                 Journal.order==order,
                                                 Journal.delete_dt == None,
                                                 or_(Journal.type=='PartialPayment',
                                                     Journal.type=='FullPayment',
                                                     Journal.type=='Discount',
                                                     Journal.type=='Refund')))\
                                                 .order_by(Journal.create_dt.desc()).all()
        total = 0.0

        for j in jes:
            if j.type in ('FullPayment', 'PartialPayment', 'CreditIncrease', 'Discount'):
                total += j.amount
        return total


    @staticmethod
    def find_total_refunds_applied_to_order(order):
        """ KB: [2011-03-08]: This could be done in the DB but we may want to have different handling by type,
        which is easier to express in python.
        """
        jes = Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                 Journal.order==order,
                                                 Journal.delete_dt == None,
                                                 Journal.type=='Refund'))\
                                                 .order_by(Journal.create_dt.desc()).all()
        total = 0.0
        for j in jes:
            total += j.amount
        return total

    @staticmethod
    def find_discounts_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                  Journal.order==order,
                                                  Journal.delete_dt == None,
                                                  Journal.type=='Discount'))\
                                                  .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_total_discounts_applied_to_order(order):
        jes = Journal.find_discounts_by_order(order)
        total = 0.0
        for j in jes:
            total += j.amount
        return total


    @staticmethod
    def find_total_credits_applied_to_order(order):
        jes = Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                 Journal.order==order,
                                                 Journal.delete_dt == None,
                                                 Journal.type=='CreditDecrease'))\
                                                 .order_by(Journal.create_dt.desc()).all()
        total = 0.0
        for j in jes:
            total += j.amount
        return total


    @staticmethod
    def find_total_applied_to_customer(customer):
        jes = Session.query(Journal).filter(and_(Journal.customer==customer,
                                                  Journal.delete_dt == None))\
                                                  .order_by(Journal.create_dt.desc()).all()
        total = 0.0
        for j in jes:
            if 'FullPayment' == j.type or 'PartialPayment' == j.type or 'CreditIncrease' == j.type:
                total += j.amount
            else:
                total -= j.amount
        return total


    @staticmethod
    def find_balance_for_customer(customer):
        total_payments = Journal.find_total_applied_to_customer(customer)
        total_price = customer.get_total_order_value()
        bal = total_price - total_payments
        return bal if bal == 0.0 else -1*(bal)


