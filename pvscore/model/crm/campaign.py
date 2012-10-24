from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Float
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.crm.company import Company
from pvscore.lib.dbcache import FromCache, invalidate
from pvscore.lib.mail import MailInfo
import uuid
from pvscore.lib.sqla import GUID


class Campaign(ORMBase, BaseModel):
    __tablename__ = 'crm_campaign'
    __pk__ = 'campaign_id'

    campaign_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    company_id = Column(GUID, ForeignKey('crm_company.company_id'))
    comm_post_purchase_id = Column(GUID, ForeignKey('crm_communication.comm_id'))
    comm_post_cancel_id = Column(GUID, ForeignKey('crm_communication.comm_id'))
    comm_packing_slip_id = Column(GUID, ForeignKey('crm_communication.comm_id'))
    comm_forgot_password_id = Column(GUID, ForeignKey('crm_communication.comm_id'))
    name = Column(String(100))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    type = Column(String(50))
    default_url = Column(String(50))
    tax_rate = Column(Float)
    email = Column(String(50))
    smtp_server = Column(String(50))
    smtp_username = Column(String(50))
    smtp_password = Column(String(50))
    imap_server = Column(String(50))
    imap_username = Column(String(50))
    imap_password = Column(String(50))

    company = relation('Company', lazy='joined', primaryjoin=Company.company_id == company_id)

    def __repr__(self):
        return '%s : %s' % (self.campaign_id, self.name)


    def get_email_info(self):
        if self.smtp_server is not None and self.smtp_username is not None:
            return MailInfo(self)
        if self.company:
            return self.company.get_email_info()  #pylint: disable-msg=E1101
    

    @staticmethod
    def find_all(enterprise_id):
        #pylint: disable-msg=E1101
        return Session.query(Campaign) \
            .options(FromCache('Campaign.find_all', enterprise_id)) \
            .join((Company, Campaign.company_id == Company.company_id)).filter(and_(Campaign.delete_dt == None,
                                                                                    Company.enterprise_id == enterprise_id)) \
                                                                                    .order_by(Company.default_campaign_id.desc(), Campaign.name).all()


    @staticmethod
    def find_by_company(company):
        #pylint: disable-msg=E1101
        return Session.query(Campaign) \
            .filter(and_(Campaign.delete_dt == None,
                         Campaign.company == company)) \
                         .order_by(Campaign.name.asc()).all()


    @staticmethod
    def search(enterprise_id, name, company_id):
        n_clause = cid_clause = ''
        if name:
            n_clause = "and cam.name like '%s%%'" % name
        if company_id:
            cid_clause = "and cam.company_id = '%s'" % company_id
        sql = """SELECT cam.* FROM crm_campaign cam, crm_company com
                 where cam.company_id = com.company_id
                 and com.enterprise_id = '{ent_id}'
                 {n} {cid}
              """.format(n=n_clause, cid=cid_clause, ent_id=enterprise_id)
        return Session.query(Campaign).from_statement(sql).all()  #pylint: disable-msg=E1101




    def _send_impl(self, customer, order, comm_id):
        if comm_id:
            from pvscore.model.crm.comm import Communication
            comm = Communication.load(comm_id)
            comm.send_to_customer(self, customer, order)
            

    def send_post_purchase_comm(self, order):
        return self._send_impl(order.customer, order, self.comm_post_purchase_id)


    def send_post_cancel_comm(self, customer):
        return self._send_impl(customer, None, self.comm_post_cancel_id)


    def send_forgot_password_comm(self, customer):
        return self._send_impl(customer, None, self.comm_forgot_password_id)


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Campaign.find_all', self.company.enterprise_id)    #pylint: disable-msg=E1101


    # def get_product_specials(self):
    #     from pvscore.model.crm.product import Product
    #     return Product.find_specials_by_campaign(self)


    # def get_product_features(self):
    #     from pvscore.model.crm.product import Product
    #     return Product.find_featured_by_campaign(self)


    # @staticmethod
    # def create(name, company):
    #     camp = Campaign()
    #     camp.company = company
    #     camp.name = name
    #     return camp

    # def get_products(self):
    #     from pvscore.model.crm.product import Product
    #     return Product.find_by_campaign(self)
