#pylint: disable-msg=E1101,C0103
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import String, DateTime, Float, Text
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.thirdparty.dbcache import invalidate
import uuid
from pvscore.lib.sqla import GUID

class Journal(ORMBase, BaseModel):
    """ KB: [2012-09-03]:
        Scenario 1
            Buy Something
            -------------------
            Item A = 10
            Item B = 20
            Order Tot = 30

            Customer Balance Pre Txn = 50

            Discount = 5
            **PartialPayment = 20

            Total Applied = Payments + Discount + CreditDecreases = (20 + 5 + 0) = 25
            Total Due = Order Total - Total Applied = 5

            Customer Balance = -1 * (Total Due - TotalCreditIncrease) = -5


            Return Item A
            -------------------
            Total Due = 5
            Refund Amount = Item A Price - Total Due = 5

        Scenario 2
            Buy Something
            -------------------
            Item A = 10
            Item B = 20
            Order Tot = 30

            Customer Balance Pre Txn = 50

            Discount = 0
            **Apply CreditDecrease = 30

            Total Applied = Payments + Discount + CreditDecreases = 0 + 0 + 30 = 30
            Total Due = Order Total - Total Applied = 0

            Return Item A
            -------------------
            Total Due = 0
            Refund Amount = Item A Price - Total Due = 10

    """
    __tablename__ = 'crm_journal'
    __pk__ = 'journal_id'

    journal_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    customer_id = Column(GUID, ForeignKey('crm_customer.customer_id'))
    order_id = Column(GUID, ForeignKey('crm_customer_order.order_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    type = Column(String(30))
    note = Column(Text)
    method = Column(String(25))
    amount = Column(Float)
    fk_type = Column(String(50))
    fk_id = Column(GUID)

    customer = relation('Customer')
    creator = relation('Users')


    def __repr__(self):
        return '%s %s %s = %s' % (self.journal_id, self.type, self.method, self.amount)


    @staticmethod
    def get_types():
        return ['FullPayment', 'PartialPayment', 'Refund', 'CreditIncrease', 'CreditDecrease', 'Discount', 'AutomaticDiscount']


    @staticmethod
    def get_payment_methods(enterprise):
        ccard = ['Credit Card'] if enterprise.is_credit_card_enabled() else []
        return ccard + ['Credit Card (offline)',
                        'Cash',
                        'Apply Balance',
                        'Check',
                        'Wire',
                        'Discount']
    

    @staticmethod
    def create_new(amount, customer, order, creator, typ='FullPayment', payment_method='Credit Card', note=None, attachment=None):   #pylint: disable-msg=R0913
        jrnl = Journal()
        jrnl.type = typ
        jrnl.note = note
        jrnl.customer = customer
        jrnl.creator = creator
        jrnl.order_id = order.order_id
        jrnl.amount = amount
        jrnl.method = payment_method
        if attachment:
            jrnl.fk_type = type(attachment).__name__
            jrnl.fk_id = getattr(attachment, attachment.__pk__)
        jrnl.save()
        return jrnl


    @staticmethod
    def total_balance_for_customer(customer):
        entries = Journal.find_all_by_customer(customer)
        total_entries = sum([ent.amount if ent.type in ('FullPayment', 'PartialPayment', 'CreditIncrease') else -ent.amount
                             for ent in entries if ent.type != 'AutomaticDiscount'])
        total_price = customer.get_total_order_value()
        bal = total_price - total_entries
        return bal if bal == 0.0 else -1*(bal)


    @staticmethod
    def total_due(order):
        return order.total_price() - Journal.total_applied(order)


    @staticmethod
    def total_applied(order):
        return Journal.total_payments(order) + Journal.total_discounts(order) + Journal.total_credit_decreases(order)


    @staticmethod
    def total_discounts(order):
        return sum([ent.amount for ent in Journal.filter_discounts(order)])


    @staticmethod
    def filter_discounts(order):
        return Journal._filter_by_types(order, ['Discount'])


    @staticmethod
    def total_automatic_discounts(order):
        return sum([ent.amount for ent in Journal.filter_automatic_discounts(order)])


    @staticmethod
    def filter_automatic_discounts(order):
        return Journal._filter_by_types(order, ['AutomaticDiscount'])


    @staticmethod
    def total_credit_decreases(order):
        return sum([ent.amount for ent in Journal.filter_credit_decreases(order)])


    @staticmethod
    def filter_credit_decreases(order):
        return Journal._filter_by_types(order, ['CreditDecrease'])


    @staticmethod
    def total_credit_increases(order):
        return sum([ent.amount for ent in Journal.filter_credit_increases(order)])


    @staticmethod
    def filter_credit_increases(order):
        return Journal._filter_by_types(order, ['CreditIncrease'])


    @staticmethod
    def total_payments(order):
        return sum([ent.amount for ent in Journal.filter_payments(order)])


    @staticmethod
    def filter_payments(order):
        return Journal._filter_by_types(order, ['PartialPayment', 'FullPayment'])


    @staticmethod
    def total_refunds(order):
        return sum([ent.amount for ent in Journal.filter_refunds(order)])


    @staticmethod
    def filter_refunds(order):
        return Journal._filter_by_types(order, ['Refund'])


    @staticmethod
    def _filter_by_types(order, types):
        return [entry for entry in order.journal_entries if entry.type in types and entry.delete_dt is None]


    @staticmethod
    def find_all_by_customer(customer, offset=0, limit=25):
        #.options(FromCache('Journal.find_all_by_customer', customer.campaign.company.enterprise_id)) \
        return Session.query(Journal)\
            .filter(and_(Journal.customer==customer,
                         Journal.delete_dt == None))\
                         .order_by(Journal.create_dt.desc()).offset(offset).limit(limit).all()


    @staticmethod
    def find_all_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
               	                                  Journal.order==order,
                                                  Journal.delete_dt == None))\
                                                  .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_refunds_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                  Journal.order==order,
                                                  Journal.delete_dt == None,
                                                  Journal.type=='Refund'))\
                                                 .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_payments_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                 Journal.order==order,
                                                 Journal.delete_dt == None,
                                                 or_(Journal.type=='PartialPayment',
                                                     Journal.type=='FullPayment')))\
                                                 .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_discounts_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                  Journal.order==order,
                                                  Journal.delete_dt == None,
                                                  Journal.type=='Discount'))\
                                                  .order_by(Journal.create_dt.desc()).all()


    @staticmethod
    def find_credits_by_order(order):
        return Session.query(Journal).filter(and_(Journal.customer==order.customer,
                                                  Journal.order==order,
                                                  Journal.delete_dt == None,
                                                  Journal.type=='CreditDecrease'))\
                                                  .order_by(Journal.create_dt.desc()).all()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Journal.find_all_by_customer', self.customer.campaign.company.enterprise_id)


