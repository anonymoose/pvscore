#pylint: disable-msg=E1101
# Zachary234 = 4476212f8f185ba416fc0708bebcc91b
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from hashlib import md5

class Users(ORMBase, BaseModel):
    __tablename__ = 'core_user'
    __pk__ = 'username'

    username = Column(String(50), primary_key=True)
    password = Column(String(75))
    password_len = Column(Integer, default=0)
    fname = Column(String(50))
    lname = Column(String(50))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    api_key = Column(String(50))
    type = Column(String(50))
    enterprise_id = Column(Integer, ForeignKey('crm_enterprise.enterprise_id'))
    priv_id = Column(Integer, ForeignKey('core_user_priv.priv_id'))
    vendor_id = Column(Integer, ForeignKey('crm_vendor.vendor_id'))
    tz_offset = Column(Integer, default=5)
    login_link = Column(String(100))

    email = Column(String(50))

    smtp_server = Column(String(50))
    smtp_username = Column(String(50))
    smtp_password = Column(String(50))
    imap_server = Column(String(50))
    imap_username = Column(String(50))
    imap_password = Column(String(50))

    enterprise = relation('Enterprise')
    priv = relation('UserPriv', lazy='joined')
    vendor = relation('Vendor')


    def get_email_info(self):
        if self.smtp_server is not None and self.smtp_username is not None:
            return self.email, self.smtp_server, self.smtp_username, self.smtp_password
        if self.enterprise:
            return self.enterprise.get_email_info


    def is_vendor_user(self):
        return self.vendor_id != None


    @staticmethod
    def get_user_types():
        return ["Internal", "External", "Reporting", "API", "Admin"]


    @staticmethod
    def authenticate(username, pwd):
        """ KB: [2010-10-05]: See if there is a user that matches the UID and password supplied 
        Also determine if this guy is allowed into the crm/cms area of the app.
        """        
        return None != Session.query(Users).filter(
            and_(Users.username == username, 
                 Users.password == Users.encode_password(pwd))).first()


    @staticmethod
    def find_by_uid(uid):
        return Session.query(Users).filter(Users.username == uid).first()


    @staticmethod
    def is_unique_username(username):
        return None == Session.query(Users).filter(Users.username == username).first()


    @staticmethod
    def encode_password(password):
        return md5(password).hexdigest()

    # def post_load(self):
    #     if not self.priv:
    #         self.priv = UserPriv()
    #         self.priv.view_customer = True
    #         self.priv.view_product = True
    #         self.priv.view_users = True
    #         self.priv.add_customer_order = True
    #         self.priv.add_customer_billing = True
    #         self.priv.save()
    #         self.save()
    #         self.commit()


    # @staticmethod
    # def create(fname, lname, email, username, password):
    #     usr = Users()
    #     usr.fname = fname
    #     usr.lname = lname
    #     usr.email = email
    #     usr.username = username
    #     usr.password = password
    #     return usr


    # @staticmethod
    # def search(enterprise_id, username, fname, lname, email):
    #     u_clause = f_clause = l_clause = e_clause = ''
    #     if username:
    #         u_clause = "and lower(username) like '%s%%'" % username.lower()
    #     if fname:
    #         f_clause = "and lower(fname) like '%s%%'" % fname.lower()
    #     if lname:
    #         l_clause = "and lower(lname) like '%s%%'" % lname.lower()
    #     if email:
    #         e_clause = "and lower(email) like '%s%%'" % email.lower()
    #     sql = """SELECT * FROM core_user where 1=1 
    #           and enterprise_id = {entid}
    #           {uname} {fname} {lname} {email} """.format(uname=u_clause, 
    #                                                      fname=f_clause, 
    #                                                      lname=l_clause, 
    #                                                      email=e_clause, 
    #                                                      entid=enterprise_id)
    #     return Session.query(Users).from_statement(sql).all()


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Users).filter(and_(Users.delete_dt == None,
                                                Users.enterprise_id == enterprise_id)).order_by(Users.lname).all()


    @staticmethod
    def full_delete(username):
        Session.execute("delete from core_user where username = '%s'" % username)



class UserPriv(ORMBase, BaseModel):
    __tablename__ = 'core_user_priv'
    __pk__ = 'priv_id'

    priv_id = Column(Integer, primary_key=True)
    view_customer = Column(Boolean, default=False)
    edit_customer = Column(Boolean, default=False)
    view_product = Column(Boolean, default=False)
    edit_product = Column(Boolean, default=False)
    view_users = Column(Boolean, default=False)
    edit_users = Column(Boolean, default=False)
    view_campaign = Column(Boolean, default=False)
    edit_campaign = Column(Boolean, default=False)
    view_event = Column(Boolean, default=False)
    edit_event = Column(Boolean, default=False)
    view_communication = Column(Boolean, default=False)
    edit_communication = Column(Boolean, default=False)
    view_report = Column(Boolean, default=False)
    edit_report = Column(Boolean, default=False)
    view_company = Column(Boolean, default=False)
    edit_company = Column(Boolean, default=False)
    view_enterprise = Column(Boolean, default=False)
    edit_enterprise = Column(Boolean, default=False)
    add_customer_order = Column(Boolean, default=False)
    add_customer_billing = Column(Boolean, default=False)
    send_customer_emails = Column(Boolean, default=False)
    modify_customer_order = Column(Boolean, default=False)
    view_purchasing = Column(Boolean, default=False)
    edit_purchasing = Column(Boolean, default=False)
    cms = Column(Boolean, default=False)    
    edit_category = Column(Boolean, default=False)
    barcode_order = Column(Boolean, default=False)
    edit_discount = Column(Boolean, default=False)

