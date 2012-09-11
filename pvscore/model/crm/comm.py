#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from webhelpers.html import literal
from pvscore.lib.dbcache import invalidate
import logging

log = logging.getLogger(__name__)

class Communication(ORMBase, BaseModel):
    __tablename__ = 'crm_communication'
    __pk__ = 'comm_id'

    comm_id = Column(Integer, primary_key = True)
    enterprise_id = Column(Integer, ForeignKey('crm_enterprise.enterprise_id'))
    name = Column(String(50))
    url = Column(String(256))
    data = Column(Text)
    type = Column(String(50), server_default='html')
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    user_created = Column(String(50), ForeignKey('core_user.username'))
    from_addr = Column(String(50))
    subject = Column(String(256))
    user_sendable = Column(Boolean, default=False)

    enterprise = relation('Enterprise')
    creator = relation('Users')

    _other_tokens = {}


    @staticmethod
    def create(name):
        com = Communication()
        com.name = name
        com.save()
        return com


    @staticmethod
    def find_all(enterprise_id, user_sendable_only=False):
        if user_sendable_only:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.user_sendable == True,
                             Communication.enterprise_id == enterprise_id)) \
                             .order_by(Communication.name).all()
        else:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.enterprise_id == enterprise_id)) \
                             .order_by(Communication.name).all()


    @staticmethod
    def find_by_company(name, company, user_sendable_only=False):
        if user_sendable_only:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.name == name,
                             Communication.user_sendable == True,
                             Communication.enterprise_id == company.enterprise_id)).order_by(Communication.name).first()

        else:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.name == name,
                             Communication.enterprise_id == company.enterprise_id)).order_by(Communication.name).first()


    @staticmethod
    def find_all_by_company(company, user_sendable_only=False):
        if user_sendable_only:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.user_sendable == True,
                             Communication.enterprise_id == company.enterprise_id)).order_by(Communication.name).all()
        else:
            return Session.query(Communication) \
                .filter(and_(Communication.delete_dt == None,
                             Communication.enterprise_id == company.enterprise_id)).order_by(Communication.name).all()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Communication.find_all', BaseModel.get_enterprise_id())
        invalidate(self, 'Communication.find_all_by_company', self.company_id)


    @staticmethod
    def search(enterprise_id, name):
        n_clause = ''
        if name:
            n_clause = "and comm.name like '%s%%'" % name

        sql = """SELECT comm.* FROM crm_communication comm, crm_company com
                 where comm.company_id = com.company_id
                 and com.enterprise_id = {ent_id} {n}""".format(n=n_clause, ent_id=enterprise_id)
        return Session.query(Communication).from_statement(sql).all()


    @staticmethod
    def get_types():
        return ["html", "url"]


    def render(self, customer, order, extra_message=None):
        if self.data:
            if 'html' == self.type:
                dat = self.data
                if extra_message:
                    dat = dat.replace('{message}', extra_message)
                dat = self.tokenize(dat, customer, order)
                for otok in self._other_tokens.keys():
                    dat = dat.replace(otok, self._other_tokens[otok])
                return literal(dat)
            elif 'url' == self.type:
                pass
            else:
                return 'NOT IMPLEMENTED'
        else:
            return ''

    def tokenize(self, dat, customer, order):
        #pylint: disable-msg=W0612,W0613
        campaign = customer.campaign
        company = campaign.company
        enterprise = company.enterprise
        for tok in Communication.get_tokens():
            eval_str = tok.replace('{', '').replace('}', '').replace('__', '.')
            try:
                replacement = eval(eval_str)
            except Exception as ex:
                log.debug(ex)
            dat = dat.replace(tok, str(replacement if replacement else ''))
        return dat

    def add_token(self, key, value):
        self._other_tokens[key] = value

#    def send_to_customer(self, sender, customer, order=None, extra_message=None, subject=None):
#        pass
#        """
#        output = self.render(customer, order, extra_message)
#        subject = subject if subject else self.tokenize(self.subject, customer, order)
#        mail = UserMail(sender)
#        mail.send(customer.email, subject, output)
#        Status.add(customer, self, Status.find_event(self, 'SENT'), 'Sent %s (%s)' % (self.name, subject)).commit()
#        return True
#        """
#
#    def send_internal(self, sender, customer, order=None, extra_message=None, subject=None):
#        pass
#        """
#        if not sender.email: return
#        output = self.render(customer, order, extra_message)
#        subject = subject if subject else self.tokenize(self.subject, customer, order)
#        mail = UserMail(sender)
#        mail.send_internal(customer.email,
#                           sender.email,
#                           subject, output)
#        return True

    @staticmethod
    def get_tokens():
        return ['{customer__customer_id}',
                '{customer__fname}',
                '{customer__lname}',
                '{customer__title}',
                '{customer__company_name}',
                '{customer__password}',
                '{customer__campaign_id}',
                '{customer__orig_campaign_id}',
                '{customer__status_id}',
                '{customer__email}',
                '{customer__create_dt}',
                '{customer__delete_dt}',
                '{customer__user_created}',
                '{customer__user_assigned}',
                '{customer__addr1}',
                '{customer__addr2}',
                '{customer__city}',
                '{customer__state}',
                '{customer__zip}',
                '{customer__country}',
                '{customer__phone}',
                '{customer__alt_phone}',
                '{customer__fax}',
                '{customer__cid_0}',
                '{customer__cid_1}',
                '{customer__cid_2}',
                '{customer__ref_0}',
                '{customer__ref_1}',
                '{customer__ref_2}',
                '{customer__creator__username}',
                '{customer__creator__fname}',
                '{customer__creator__lname}',
                '{customer__creator__email}',
                '{customer__assigned_to__username}',
                '{customer__assigned_to__fname}',
                '{customer__assigned_to__lname}',
                '{customer__assigned_to__email}',
                '{order__total}',
                '{order__summary}',
                '{order__order_id}',
                '{order__payment_history}',
                '{order__create_dt}',
                '{order__cancel_dt}',
                '{company__name}',
                '{company__company_id}',
                '{campaign__name}',
                '{campaign__campaign_id}',
                '{campaign__default_url}',
                '{datetime.datetime.today()}',
                '{message}']


    @staticmethod
    def full_delete(comm_id):
        Session.execute('delete from crm_communication where comm_id = %s' % comm_id)
