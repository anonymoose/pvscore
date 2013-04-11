#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, DateTime, Text, Float, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.crm.customerorder import CustomerOrder
from pvscore.model.core.users import Users
from pvscore.model.crm.journal import Journal
import pvscore.lib.db as db
import uuid
from pvscore.lib.sqla import GUID
from pvscore.model.core.status import Status
from pyramid.httpexceptions import HTTPForbidden


class Customer(ORMBase, BaseModel):

    __tablename__ = 'crm_customer'
    __pk__ = 'customer_id'

    customer_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    campaign_id = Column(GUID, ForeignKey('crm_campaign.campaign_id'))
    billing_id = Column(GUID, ForeignKey('crm_billing.billing_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    user_assigned = Column(GUID, ForeignKey('core_user.user_id'))
    fname = Column(String(50))
    lname = Column(String(50))
    title = Column(String(50))
    company_name = Column(String(50))
    password = Column(String(50))
    orig_campaign_id = Column(Integer)
    email = Column(String(50))
    delete_dt = Column(DateTime)
    email_optout_dt = Column(DateTime)
    create_dt = Column(DateTime, server_default = text('now()'))
    mod_dt = Column(DateTime, server_default=text('now()'))
    addr1 = Column(String(50))
    addr2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    country = Column(String(50))
    phone = Column(String(20))
    alt_phone = Column(String(20))
    fax = Column(String(20))
    notes = Column(Text)
    third_party_agent = Column(String(100))
    third_party_id = Column(String(100))
    default_latitude = Column(Float)
    default_longitude = Column(Float)
    phase_id = Column(GUID, ForeignKey('crm_customer_phase.phase_id'))

    cid_0 = Column(String(50))
    cid_1 = Column(String(50))
    cid_2 = Column(String(50))
    cid_3 = Column(String(50))
    cid_4 = Column(String(50))
    cid_5 = Column(String(50))
    cid_6 = Column(String(50))
    cid_7 = Column(String(50))
    cid_8 = Column(String(50))
    cid_9 = Column(String(50))
    ref_0 = Column(String(50))
    ref_1 = Column(String(50))
    ref_2 = Column(String(50))

    creator = relation('Users', primaryjoin=Users.user_id == user_created)
    assigned_to = relation('Users', primaryjoin=Users.user_id == user_assigned)
    orders = relation('CustomerOrder', lazy="joined", order_by="desc(CustomerOrder.create_dt)")
    campaign = relation('Campaign')
    status = relation('Status', primaryjoin=Status.status_id == status_id)
    billing = relation('Billing', lazy="joined")
    phase = relation('CustomerPhase', lazy="joined")

    def __repr__(self):
        return '%s : %s %s %s' % (self.customer_id, self.email, self.fname, self.lname)


    def account_key(self):
        """ KB: [2012-11-29]: This used to be a weird md5 of email and password.  now its just the customer id. """
        return self.customer_id


    def api_key(self):
        return self.account_key()


    @staticmethod
    def find_by_key(key):
        return Customer.load(key)


    @staticmethod
    def find(email, campaign):
        """ KB: [2010-12-15]: Find another customer that is in the same company. """
        from pvscore.model.crm.campaign import Campaign
        return Session.query(Customer).join((Campaign, Campaign.campaign_id == Customer.campaign_id)) \
            .filter(and_(Customer.delete_dt == None,
                         Campaign.company_id == campaign.company_id,
                         Customer.email.ilike(email))).first()


    @staticmethod
    def find_all_by_email(email):
        return Session.query(Customer) \
            .filter(and_(Customer.delete_dt == None,
                         Customer.email.ilike(email))).all()


    @staticmethod
    def find_last_names_autocomplete(enterprise_id, user_input, limit):
        return db.get_result_dict(['customer_id', 'name'], """select cust.customer_id,
                                            cust.lname || ', ' || cust.fname as "name"
                                                 from crm_customer cust, crm_campaign cam, crm_company com
                                                 where (lower(cust.lname) like '%%{l}%%' or cust.email = '{l}')
                                                 and cust.delete_dt is null
                                                 and cust.campaign_id = cam.campaign_id
                                                 and cam.company_id = com.company_id
                                                 and com.enterprise_id = '{ent_id}'
                                                 order by cust.lname, cust.fname limit {lim}""".format(l=user_input.lower(),
                                                                                           lim=limit,
                                                                                           ent_id=enterprise_id))


    @staticmethod
    def find_by_company(email, company):
        """ KB: [2010-12-15]: Find another customer that is in the same company. """
        from pvscore.model.crm.campaign import Campaign
        return Session.query(Customer).join((Campaign, Campaign.campaign_id == Customer.campaign_id)) \
            .filter(and_(Customer.delete_dt == None,
                         Campaign.company_id == company.company_id,
                         Customer.email.ilike(email))).first()


    @staticmethod
    def search(enterprise_id, company_name, fname, lname, email, phone, user_assigned):   #pylint: disable-msg=R0913
        cn_clause = f_clause = l_clause = e_clause = p_clause = a_clause = ''
        if company_name:
            cn_clause = "and lower(cc.company_name) like '%{desc}%'".format(desc=company_name.lower())
        if fname:
            f_clause = "and lower(cc.fname) like '%{desc}%'".format(desc=fname.lower())
        if lname:
            l_clause = "and lower(cc.lname) like '%{desc}%'".format(desc=lname.lower())
        if email:
            e_clause = "and lower(cc.email) like '%{desc}%'".format(desc=email.lower())
        if phone:
            p_clause = "and cc.phone = '%s'" % phone
        if user_assigned:
            a_clause = "and cc.user_assigned = '%s'" % user_assigned
        sql = """SELECT cc.* FROM crm_customer cc, crm_campaign cam, crm_company com
                 where cc.campaign_id = cam.campaign_id
                 and cam.company_id = com.company_id
                 and com.enterprise_id = '{ent_id}'
                 and cc.delete_dt is null
                 {cn} {f} {l} {e} {p} {a}
              """.format(cn=cn_clause, f=f_clause, l=l_clause, e=e_clause, p=p_clause, ent_id=enterprise_id, a=a_clause)
        return Session.query(Customer).from_statement(sql).all()


    def add_order(self, cart, user_created, enterprise_id, campaign, order_note=None, incl_tax=True):     #pylint: disable-msg=R0913
        return CustomerOrder.create_new(cart, self, enterprise_id, campaign, user_created,
                                        order_note=order_note, incl_tax=incl_tax)


    def get_order(self, order_id):
        return CustomerOrder.find_by_customer(self, order_id)


    @staticmethod
    def authenticate(username, pwd, company):
        """ KB: [2010-10-05]: See if there is a user that matches the UID and password supplied """
        val = Session.query('cnt')\
            .from_statement("""select count(0) cnt
                               from crm_customer c, crm_campaign cmp, crm_company comp
                               where lower(c.email) = lower(:email)
                               and c.password = :pwd
                               and c.campaign_id = cmp.campaign_id
                               and cmp.company_id = comp.company_id
                               and comp.company_id = :company_id""")\
                               .params(email=username, pwd=pwd, company_id=company.company_id).first()
        return val and len(val) == 1 and val[0] == 1
        # from pvscore.model.crm.campaign import Campaign
        # return None != Session.query(Customer) \
        #     .join((Campaign, Campaign.campaign_id == Customer.campaign_id)) \
        #     .filter(and_(Customer.delete_dt == None,
        #                  Campaign.company_id == company.company_id,
        #                  Customer.email.ilike(username),
        #                  Customer.password == pwd)).first()
        #                  #                             Customer.password == Customer.encode_password(pwd))).first()



    def get_active_orders(self):
        ords = []
        for order in self.orders:
            if order.delete_dt == None and order.cancel_dt == None:
                ords.append(order)
        return ords


    def get_current_balance(self):
        return Journal.total_balance_for_customer(self)


    def get_total_order_value(self):
        total = 0.0
        for order in self.get_active_orders():
            if order.delete_dt == None:
                total += order.total_price()
        return total


    @staticmethod
    def full_delete(customer_id):
        """ KB: [2010-10-21]: this is mostly for testing purposes and typically from paster shell.  Use with caution.
        from pvscore.model.crm.customer import Customer
        Customer.delete_newest_customer()
        """
        Session.execute("delete from core_asset where status_id in (select status_id from core_status where customer_id = '%s')" % customer_id)
        Session.execute("delete from crm_billing_history where customer_id = '%s'" % customer_id)
        Session.execute("delete from crm_product_inventory_journal where return_id in (select return_id from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s'))" % customer_id)
        Session.execute("delete from crm_product_return where journal_id in (select journal_id from crm_journal where customer_id = '%s')" % customer_id)
        Session.execute("delete from crm_journal where customer_id = '%s'" % customer_id)
        Session.execute("delete from crm_product_inventory_journal where order_item_id in (select order_item_id from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s'))" % customer_id)
        Session.execute("delete from crm_oi_terms_acceptance where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
        Session.execute("delete from crm_order_item where order_id in (select order_id from crm_customer_order where customer_id = '%s')" % customer_id)
        Session.execute("delete from crm_customer_order where customer_id = '%s'" % customer_id)
        Session.execute("delete from pvs_listing where customer_id = '%s'" % customer_id)
        Session.execute("update crm_customer set status_id = null where customer_id = '%s'" % customer_id)
        Session.execute("delete from core_status where customer_id = '%s'" % customer_id)
        Session.execute("delete from crm_billing_history where customer_id = '%s'" % customer_id)
        #Session.execute("delete from wm_portfolio where customer_id = '%s'" % customer_id)
        #Session.execute("delete from wm_customer_holding where customer_id = '%s'" % customer_id)
        #Session.execute("delete from wm_ireport_view_log where customer_id = '%s'" % customer_id)
        billing_ids = db.get_column("select billing_id from crm_customer where customer_id = '%s'" % customer_id)
        Session.execute("delete from crm_customer where customer_id = '%s'" % customer_id)
        for bill_id in billing_ids:
            Session.execute("delete from crm_billing where billing_id = '%s'" % bill_id)


def load_customer(request, default_to_new_customer=False):
    """ KB: [2012-09-12]: Get the customer_id from the various places it
    may be stashed.  session first."""
    customer_id = None
    if request.ctx.customer:
        return request.ctx.customer
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
    elif 'customer_id' in request.POST:
        customer_id = request.POST.get('customer_id')
    elif 'customer_id' in request.GET:
        customer_id = request.GET.get('customer_id')
    customer = Customer.load(customer_id)
    if customer_id and (not customer or customer.campaign.company.enterprise_id != request.ctx.enterprise.enterprise_id):
        raise HTTPForbidden()
    if customer:
        return customer
    elif default_to_new_customer:
        return Customer()


class CustomerPhase(ORMBase, BaseModel):
    __tablename__ = 'crm_customer_phase'
    __pk__ = 'phase_id'

    phase_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    enterprise_id = Column(GUID, ForeignKey('crm_enterprise'))
    short_name = Column(String(20))
    display_name = Column(String(20))
    description = Column(Text)
    sort_order = Column(Integer)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime, server_default=text('now()'))
    color = Column(String(20))

    @staticmethod
    def find_all(enterprise_id):
        return Session.query(CustomerPhase)\
            .filter(and_(or_(CustomerPhase.enterprise_id == enterprise_id,
                             CustomerPhase.enterprise_id == None),
                         CustomerPhase.delete_dt == None))\
                         .order_by(CustomerPhase.short_name.asc()).all()


    @staticmethod
    def full_delete(phase_id):
        Session.execute("update crm_customer set phase_id = null where phase_id = '%s'" % str(phase_id))
        Session.execute("delete from crm_customer_phase where phase_id = '%s'" % str(phase_id))




    # @staticmethod
    # def delete_newest_customer():
    #     maxid = Session.query("m").from_statement("SELECT max(customer_id) m FROM crm_customer").one()
    #     Customer.full_delete(maxid)


    # @staticmethod
    # def find_by_third_party_id(tpid, company):
    #     from pvscore.model.crm.campaign import Campaign
    #     return Session.query(Customer).join((Campaign, Campaign.campaign_id == Customer.campaign_id)) \
    #         .filter(and_(Customer.delete_dt == None,
    #                      Campaign.company_id == company.company_id,
    #                      Customer.third_party_id == tpid)).first()

    # @staticmethod
    # def find_by_attr(attr_name, attr_value):
    #     customer_id = AttributeValue.find_fk_id_by_value('Customer', attr_name, attr_value)
    #     if customer_id:
    #         return Customer.load(customer_id)


    # @staticmethod
    # def find_all_by_channel(cid_0, cid_1=None):
    #     return Session.query(Customer)\
    #         .filter(and_(Customer.cid_0==cid_0, cid_1==cid_1)).all()


    # @staticmethod
    # def find_by_api_key(key):
    #     return Session.query(Customer)\
    #         .from_statement("""select * from crm_customer where '%s' = md5(email||customer_id)
    #                         """ % key.lower()).first()


    # def ready_to_purchase(self):
    #     return (self.fname and self.lname and self.phone and self.addr1
    #             and self.city and self.state and self.zip and self.country)


    # @staticmethod
    # def find_all_by_campaign(campaign):
    #     from pvscore.model.crm.campaign import Campaign
    #     return Session.query(Customer).join((Campaign, Campaign.campaign_id == Customer.campaign_id)) \
    #         .filter(and_(Customer.delete_dt == None,
    #                      Campaign.company_id == campaign.company_id)).all()

    # def has_purchased_product(self, product):
    #     return CustomerOrder.has_customer_purchased_product(self, product)

    # @staticmethod
    # def encode_password(password):
    #     # return md5(password).hexdigest()
    #     return password



# class PeriodCustomerCountSummary(BaseAnalytic):
#     """ KB: [2011-11-02]: Google charts report for customer count over a period """

#     def __init__(self, request, days=7):
#         super(PeriodCustomerCountSummary, self).__init__()
#         self.request = request
#         self.days = days
#         self.run()


#     def link(self, height, width, i):
#         return "http://{i}.chart.apis.google.com/chart?chxl=1:{google_y_labels}&chxr={google_range}&chxt=y,x&chbh=a,10&chs={height}x{width}&cht=bvs&chco=A2C180,3D7930&chds={google_scale}&chd=t:{google_data}&chma=10,10,10,10&chtt=New+Customers+by+Day&chts=006699,12.167"\
#             .format(google_y_labels=self.google_y_labels,
#                     google_range=self.google_range,
#                     google_scale=self.google_scale,
#                     google_data=self.google_data,
#                     height=height,
#                     width=width, i=i)


#     @property
#     def google_range(self):
#         max_ = self.col_max('cnt')
#         interval = math.floor(max_/10)
#         return '0,%s,%s' % (interval, int(max_+(2*interval)))


#     @property
#     def google_data(self):
#         return ','.join([str(res.cnt) for res in self.results])


#     @property
#     def google_y_labels(self):
#         return '|%s|' % '|'.join([util.format_date(res.create_dt)[5:] for res in self.results])


#     @property
#     def google_scale(self):
#         max_ = self.col_max('cnt')
#         interval = int(math.floor(max_/10))
#         scale = '%s,%s' % (interval, int(max_+(2*interval)))
#         return '%s,%s' % (scale, scale)


#     @property
#     def columns(self):
#         return ("cnt", "create_dt")


#     @property
#     def query(self):
#         return """select count(0) as cnt, cust.create_dt
#                     from
#                     crm_customer cust, crm_campaign cmp, crm_company co
#                     where
#                     cust.campaign_id = cmp.campaign_id and
#                     cmp.company_id = co.company_id and
#                     co.enterprise_id = '{entid}' and
#                     cust.delete_dt is null and
#                     cust.create_dt between current_date - {d} and current_date
#                     group by cust.create_dt
#                     order by cust.create_dt asc""".format(d=self.days, entid=self.request.ctx.enterprise.enterprise_id)
