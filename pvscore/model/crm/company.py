#pylint: disable-msg=E1101,R0801
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, DateTime, Text
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.lib.dbcache import FromCache, invalidate
import pvscore.lib.db as db
from pvscore.lib.mail import MailInfo
import uuid
from pvscore.lib.sqla import GUID


class Company(ORMBase, BaseModel):
    __tablename__ = 'crm_company'
    __pk__ = 'company_id'

    company_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    enterprise_id = Column(GUID, ForeignKey('crm_enterprise.enterprise_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    default_campaign_id = Column(GUID, ForeignKey('crm_campaign.campaign_id'))
    name = Column(String(50))
    paypal_id = Column(String(256))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    anon_customer_email = Column(String(75))

    
    addr1 = Column(String(50))
    addr2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    country = Column(String(50))
    phone = Column(String(20))
    alt_phone = Column(String(20))
    fax = Column(String(20))

    email = Column(String(50))
    smtp_server = Column(String(50))
    smtp_username = Column(String(50))
    smtp_password = Column(String(50))
    imap_server = Column(String(50))
    imap_username = Column(String(50))
    imap_password = Column(String(50))


    enterprise = relation('Enterprise', lazy="joined", backref=backref('companies', order_by='Company.name'))
    status = relation('Status')

    def __repr__(self):
        return '%s : %s' % (self.company_id, self.name)


    def get_email_info(self):
        if self.smtp_server is not None and self.smtp_username is not None:
            return MailInfo(self)
        if self.enterprise:
            return self.enterprise.get_email_info()


    @property
    def default_campaign(self):
        from pvscore.model.crm.campaign import Campaign
        return Session.query(Campaign) \
            .options(FromCache('Company.default_campaign', self.company_id)) \
            .filter(and_(Campaign.delete_dt == None,
                         Campaign.campaign_id == self.default_campaign_id)).first()


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Company) \
            .options(FromCache('Company.find_all', enterprise_id)) \
            .filter(and_(Company.delete_dt == None,
                         Company.enterprise_id == enterprise_id)).order_by(Company.name).all()


    @staticmethod
    def find_all_all():
        return Session.query(Company) \
            .options(FromCache('Company.find_all_all')) \
            .filter(Company.delete_dt == None).order_by(Company.name).all()


    @staticmethod
    def find_by_name(enterprise_id, name):
        return Session.query(Company) \
            .filter(and_(Company.name == name,
                         Company.enterprise_id == enterprise_id)).first()


    def invalidate_caches(self, **kwargs):
        from pvscore.model.cms.site import Site
        invalidate(self, 'Company.find_all_all')
        invalidate(self, 'Company.find_all', self.enterprise_id)
        invalidate(self, 'Company.find_by_name', self.name)
        invalidate(self, 'Company.default_campaign', self.company_id)
        for i in Site.find_all(self.enterprise_id):
            i.invalidate_caches()


    @staticmethod
    def search(name):
        n_clause = ''
        if name:
            n_clause = "and com.name like '%s%%'" % name

        sql = """SELECT com.* FROM crm_company com
                 where 1=1
                 {n}
              """.format(n=n_clause)
        return Session.query(Company).from_statement(sql).all()


class Enterprise(ORMBase, BaseModel):
    __tablename__ = 'crm_enterprise'
    __pk__ = 'enterprise_id'

    enterprise_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    name = Column(String(50))
    crm_style = Column(Text)
    # KB: [2011-12-04]: If this enterprise is created because of a customer relationship in another enterprise, put that FK here.
    customer_id = Column(Integer) # if this enterprise is created because of a
                                  # customer in another enterprise, put the FK here.
    order_item_id = Column(Integer) # if this enterprise is created because of a
                                    # customer in another enterprise, put the FK
                                    # to the order item here.
    terms_link = Column(String(75))
    copyright = Column(String(200))
    logo_path = Column(String(200))
    logo_path_pdf = Column(String(200))
    support_email = Column(String(50))
    support_phone = Column(String(20))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    billing_method = Column(String(50))

    email = Column(String(50))
    smtp_server = Column(String(50))
    smtp_username = Column(String(50))
    smtp_password = Column(String(50))
    imap_server = Column(String(50))
    imap_username = Column(String(50))
    imap_password = Column(String(50))

    def __repr__(self):
        return '%s : %s' % (self.enterprise_id, self.name)


    def get_email_info(self):
        return MailInfo(self)


    @staticmethod
    def get_billing_methods():
        return ['PayPal', 'CCEAccounts', 'Stripe', 'Invoice', 'Offline']


    @property
    def customer(self):
        from pvscore.model.crm.customer import Customer
        return Customer.load(self.customer_id)


    @property
    def order_item(self):
        from pvscore.model.crm.orderitem import OrderItem
        return OrderItem.load(self.order_item_id)


    @property
    def is_purchased(self):
        return bool((self.order_item_id or self.customer_id))


    @property
    def terms_required(self):
        return (self.order_item_id is not None and self.terms_link is not None)


    @property
    def terms_accepted(self):
        from pvscore.model.crm.orderitem import OrderItemTermsAcceptance
        return OrderItemTermsAcceptance.is_order_item_id_accepted(self.order_item_id)


    @staticmethod
    def find_all():
        return Session.query(Enterprise) \
            .filter(Enterprise.delete_dt == None).order_by(Enterprise.name).all()


    @staticmethod
    def find_by_name(name):
        return Session.query(Enterprise) \
            .filter(and_(Enterprise.delete_dt == None,
                         Enterprise.name == name)).first()


    @staticmethod
    def full_delete(enterprise_id):
        from pvscore.model.crm.customer import Customer
        company_ids = db.get_list("select company_id from crm_company where enterprise_id = '%s'" % enterprise_id)
        campaign_ids = db.get_list("""select campaign_id from crm_campaign where
                                      company_id in (select company_id from crm_company where enterprise_id = '%s')""" % enterprise_id)

        customer_ids = db.get_list("""select customer_id from crm_customer where
                                      campaign_id in (select campaign_id from crm_campaign where
                                          company_id in (select company_id from crm_company where enterprise_id = '%s'))""" % enterprise_id)
        product_ids = db.get_list("""select product_id from crm_product where
                                     company_id in (select company_id from crm_company where enterprise_id = '%s')""" % enterprise_id)

        for cid in customer_ids:
            Customer.full_delete(cid[0])

        for pid in product_ids:
            product_id = pid[0]
            Session.execute("delete from crm_product_return where product_id = '%s'" % product_id)
            Session.execute("delete from crm_product_category_join where product_id = '%s'" % product_id)
            Session.execute("delete from crm_product_child where parent_id = '%s'" % product_id)
            Session.execute("delete from crm_product_child where child_id = '%s'" % product_id)
            Session.execute("delete from crm_product_pricing where product_id = '%d'" % product_id)
            Session.execute("delete from crm_product_inventory_journal where product_id = '%d'" % product_id)
            Session.execute("delete from crm_purchase_order_item where product_id = '%d'" % product_id)
            Session.execute("delete from crm_order_item where product_id = '%d'" % product_id)
            Session.execute("delete from crm_product where product_id = '%d'" % product_id)

        for cid in campaign_ids:
            campaign_id = cid[0]
            Session.execute("delete from crm_product_pricing where campaign_id = '%s'" % campaign_id)

        for cid in company_ids:
            company_id = cid[0]
            Session.execute("delete from crm_product_category where company_id = '%s'" % company_id)
            Session.execute("delete from crm_report where company_id = '%s'" % company_id)
            Session.execute("""delete from cms_content where site_id in (select site_id from cms_site where company_id = '%s')""" % company_id)
            Session.execute("delete from cms_page where site_id in (select site_id from cms_site where company_id = '%s')" % company_id)
            Session.execute("delete from cms_site where company_id = '%s'" % company_id)
            Session.execute("update crm_company set default_campaign_id = null where company_id = '%s'" % company_id)
            Session.execute("delete from crm_campaign where company_id = '%s'" % company_id)
            Session.execute("delete from crm_purchase_order where company_id = '%s'" % company_id)

        Session.execute("delete from crm_communication where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from core_status where event_id in (select event_id from core_status_event where enterprise_id = '%s')" % enterprise_id)
        Session.execute("delete from core_status_event_reason where event_id in (select event_id from core_status_event where enterprise_id = '%s')" % enterprise_id)
        Session.execute("delete from core_status_event where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from cms_template where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from crm_company where enterprise_id = '%s'" % enterprise_id)
        #Session.execute('update core_user set enterprise_id = null where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from core_user where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from crm_vendor where enterprise_id = '%s'" % enterprise_id)
        Session.execute("delete from crm_enterprise where enterprise_id = '%s'" % enterprise_id)




    ############################## Company
    # def company_web_directory(self, subdir):
    #     """ KB: [2011-02-02]: The "companies" below corresponds to the /companies location in the nginx conf file """
    #     return "/companies/{dirname}/{subdir}".format(dirname=self.web_directory, subdir=subdir)


    # def store_asset(self, asset_data, folder, fk_type, fk_id):
    #     """ KB: [2010-11-18]:
    #     called from pvscore.controllers.cms.asset::upload_to_company()
    #     http://pylonsbook.com/en/1.1/working-with-forms-and-validators.html
    #     """

    #     fs_path = os.path.join(
    #         '%s%s' % (self.web_full_directory, folder),
    #         asset_data.filename.replace(os.sep, '_')
    #         )
    #     permanent_file = open(fs_path, 'wb')
    #     shutil.copyfileobj(asset_data.file, permanent_file)
    #     asset_data.file.close()
    #     permanent_file.close()
    #     # at this point everything is saved to disk. Create an asset object in
    #     # the DB to remember it.
    #     return Asset.create_new(asset_data.filename,
    #                          fs_path,
    #                          '{base}/{f}'.format(base=self.company_web_directory('images'),
    #                                              f=asset_data.filename),
    #                          fk_type, fk_id).flush()

    # def get_all_active_products(self):
    #     from pvscore.model.crm.product import Product
    #     return Product.find_all_active(self)


    # def is_email_ready(self):
    #     return (self.smtp_server and self.smtp_server.find(':') >= 0)


    # @staticmethod
    # def create(name):
    #     comp = Company()
    #     comp.name = name
    #     return comp

    ######################### Enterprise
    # @staticmethod
    # def find_by_customer(customer):
    #     """ KB: [2012-01-15]: If we are in one enterprise (the root [ie: wealthmakers]) and we want to find the customer's enterprise
    #     call this method
    #     """
    #     return Session.query(Enterprise)\
    #         .filter(and_(Enterprise.customer_id == customer.customer_id,
    #                      Enterprise.delete_dt == None)).first()


    # @staticmethod
    # def find_all_non_customer():
    #     return Session.query(Enterprise) \
    #         .filter(and_(Enterprise.delete_dt == None,
    #                      Enterprise.customer_id == None)).order_by(Enterprise.name).all()

        
    # @property
    # def web_full_directory(self):
    #     return "{root_dir}/{dirname}".format(root_dir=util.cache_get('pvs.company.web.root.dir'),
    #                                          dirname=self.web_directory)


    # @property
    # def web_directory(self):
    #     return str(self.company_id)


    # def create_dir_structure(self):
    #     dirname = self.web_full_directory
    #     util.mkdir_p(dirname)
    #     util.mkdir_p("%s/images" % dirname)
    #     util.mkdir_p("%s/script" % dirname)
    #     util.mkdir_p("%s/cache" % dirname)
