#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.crm.company import Company
from app.model.crm.campaign import Campaign
import logging

log = logging.getLogger(__name__)

class Report(ORMBase, BaseModel):
    __tablename__ = 'crm_report'
    __pk__ = 'report_id'

    report_id = Column(Integer, primary_key = True)
    name = Column(String(100))
    description = Column(String(200))
    type = Column(String(50))
    sql = Column(Text)
    initial_sort_col = Column(String(50))
    id_col = Column(String(50))
    column_names = Column(String(1000))
    column_model = Column(String(3000))
    on_dbl_click = Column(Text)
    override = Column(String(200))
    is_vendor = Column(Boolean, default=False)

    show_start_dt = Column(Boolean, default=False)
    show_end_dt = Column(Boolean, default=False)
    show_campaign_id = Column(Boolean, default=False)
    show_company_id = Column(Boolean, default=False)
    show_user_id = Column(Boolean, default=False)
    show_product_id = Column(Boolean, default=False)
    show_vendor_id = Column(Boolean, default=False)

    p0_name = Column(String(50))
    p1_name = Column(String(50))
    p2_name = Column(String(50))

    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)

    @staticmethod
    def find_all(only_show_vendor_reports=False):
        if not only_show_vendor_reports:
            return Session.query(Report).filter(Report.delete_dt == None).order_by(Report.name).all()
        else:
            return Session.query(Report).filter(and_(Report.delete_dt == None,
                                                     Report.is_vendor == True)).order_by(Report.name).all()

    @staticmethod
    def find_default_by_company(company):
        return Session.query(Campaign).filter(and_(Campaign.delete_dt == None,
                                                   Campaign.company == company)).order_by(Campaign.create_dt.asc()).first()

    @staticmethod
    def search(name, company_id, only_show_vendor_reports=False):
        n_clause = cid_clause = v_clause = ''
        if name:
            n_clause = "and rep.name like '%s%%'" % name
        if company_id:
            cid_clause = "and rep.company_id = %d" % int(company_id)
        if only_show_vendor_reports:
            v_clause = "and rep.is_vendor = true"

        sql = """SELECT rep.* FROM crm_report rep
                 where 1=1
                 {n} {cid} {v}
              """.format(n=n_clause, cid=cid_clause, v=v_clause)
        return Session.query(Report).from_statement(sql).all()


    def clear_companies(self):
        if self.report_id:
            ReportCompanyJoin.clear_by_report(self)


    def add_company(self, company_id):
        return ReportCompanyJoin.create_new(self.report_id, company_id)

    @staticmethod
    def full_delete(report_id):
        Session.execute('delete from crm_report_company_join where report_id = %s' % report_id) 
        Session.execute('delete from crm_report where report_id = %s' % report_id)

class ReportCompanyJoin(ORMBase, BaseModel):
    __tablename__ = 'crm_report_company_join'
    __pk__ = 'rcj_id'

    rcj_id = Column(Integer, primary_key = True)
    report_id = Column(Integer, ForeignKey('crm_report.report_id'))
    company_id = Column(Integer, ForeignKey('crm_company.company_id'))

    report = relation('Report')
    company = relation('Company', lazy='joined', primaryjoin=Company.company_id == company_id)

    @staticmethod
    def clear_by_company(company):
        Session.execute("delete from crm_report_company_join where company_id = %d" % int(company.company_id))

    @staticmethod
    def clear_by_report(report):
        Session.execute("delete from crm_report_company_join where report_id = %d" % int(report.report_id))


