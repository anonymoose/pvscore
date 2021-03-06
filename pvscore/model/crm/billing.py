#pylint: disable-msg=R0902,E1002
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel
from pvscore.model.core.users import Users
import uuid
from pvscore.lib.sqla import GUID


class Billing(ORMBase, BaseModel):
    __tablename__ = 'crm_billing'
    __pk__ = 'billing_id'

    billing_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    note = Column(String(50))
    type = Column(String(50), server_default='Credit Card')
    account_holder = Column(String(50))
    account_addr = Column(String(50))
    account_city = Column(String(50))
    account_state = Column(String(50))
    account_country = Column(String(50))
    account_zip = Column(String(50))
    third_party_id = Column(String(50))
    cc_token = Column(String(50))
    cc_last_4 = Column(Integer)
    cc_exp = Column(String(7))
    is_primary = Column(Boolean, default = True)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    creator = relation('Users', primaryjoin=Users.user_id == user_created)
    status = relation('Status')

    _cc_num = None
    _cc_cvv = None


    def set_cc_info(self, num, cvv):
        self._cc_num = num
        self._cc_cvv = cvv

    def get_cc_num(self):
        return self._cc_num

    def get_cc_cvv(self):
        return self._cc_cvv
        
    @staticmethod
    def create(cust, save=True):
        bill = Billing()
        bill.type = 'Credit Card'
        bill.account_holder = '%s %s' % (cust.fname, cust.lname)
        bill.account_addr = cust.addr1
        bill.account_city = cust.city
        bill.account_state = cust.state
        bill.account_country = cust.country
        bill.account_zip = cust.zip
        cust.billing = bill
        if save:
            cust.save()
            bill.save()
        return bill

    
    def save(self):
        return super(Billing, self).save()


class BillingHistory(ORMBase, BaseModel):
    __tablename__ = 'crm_billing_history'
    __pk__ = 'billing_history_id'

    billing_history_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    billing_id = Column(GUID, ForeignKey('crm_billing.billing_id'))
    order_id = Column(GUID, ForeignKey('crm_customer_order.order_id'))
    customer_id = Column(GUID, ForeignKey('crm_customer.customer_id'))
    status_msg = Column(String(50))
    parent = Column(String(50))
    reference = Column(String(50))
    notes = Column(String(100))
    amount = Column(String(50))
    authorized = Column(String(50))
    date = Column(String(50))
    transaction = Column(String(20))
    uid = Column(String(40))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    billing = relation('Billing')
    order = relation('CustomerOrder')
    customer = relation('Customer')




    # @staticmethod
    # def get_billing_types():
    #     return ['Credit Card']


    # def bind(self, dic, clear=False, prefix=None):
    #     super(Billing, self).bind(dic, clear, prefix)
    #     # KB: [2010-10-20]: If the user has provided a credit card number, go to the billing api and set up the new CC 
    #     if self._cc_num:
    #         self.cc_last_4 = self._cc_num[-4:]

    # def get_credit_card_number(self):
    #     return self._cc_num

    # def get_credit_card_cvv(self):
    #     return self._cc_cvv

    # def delete_billing(self, customer):
    #     #pylint: disable-msg=E1101
    #     customer.billing = None
    #     customer.save()
    #     Session.execute('delete from crm_billing_history where billing_id = %s' % self.billing_id)
    #     Session.delete(self)
