#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session


class StatusEvent(ORMBase, BaseModel):
    __tablename__ = 'core_status_event'
    __pk__ = 'event_id'

    event_id = Column(Integer, primary_key = True)
    event_type = Column(String(50))
    short_name = Column(String(50))
    display_name = Column(String(50))
    phase = Column(String(50))
    create_dt = Column(Date, server_default = text('now()'))
    end_dt = Column(Date)
    claim = Column(Boolean, default = False)
    finalize = Column(Boolean, default = False)
    is_system = Column(Boolean, default = False)
    milestone_complete = Column(Boolean, default = False)
    note_req = Column(Boolean, default = False)
    dashboard = Column(Boolean, default = False)
    reason_req = Column(Boolean, default = False)
    change_status = Column(Boolean, default = False)
    touch = Column(Boolean, default = False)
    position = Column(Integer, default = 1)
    enterprise_id = Column(Integer, ForeignKey('crm_enterprise.enterprise_id'))
    color = Column(String(15))

    enterprise = relation('Enterprise')


    @staticmethod
    def get_status_types():
        return ['Customer', 
                'CustomerOrder', 
                'OrderItem', 
                'Calendar', 
                'Communication', 
                'Company', 
                'Product',
                'PurchaseOrder']

    
    @staticmethod
    def search(enterprise_id, display_name, short_name):
        dn_clause = sn_clause = ''
        if display_name:
            dn_clause = "and se.display_name like '%%%s%%'" % display_name
        if short_name:
            sn_clause = "and se.short_name like '%%%s%%'" % short_name
        sql = """SELECT * FROM core_status_event se
                 where se.enterprise_id = {ent_id}
                 {dn} {sn}""".format(dn=dn_clause, sn=sn_clause, ent_id=enterprise_id)
        return Session.query(StatusEvent).from_statement(sql).all()


    @staticmethod
    def find(enterprise_id, event_type, short_name):
        return Session.query(StatusEvent).filter(and_(StatusEvent.event_type == event_type, 
                                                      StatusEvent.short_name == short_name,
                                                      or_(StatusEvent.enterprise_id == enterprise_id,
                                                          and_(StatusEvent.enterprise_id == None,
                                                               StatusEvent.is_system == True)))).first()

    @staticmethod
    def find_all(enterprise_id):
        return Session.query(StatusEvent)\
            .filter(StatusEvent.enterprise_id == enterprise_id)\
            .order_by(StatusEvent.short_name, StatusEvent.event_type).all()

    @staticmethod
    def find_all_applicable(enterprise_id, obj):
        # KB: [2010-11-29]: Eventually this will get more complex and base its
        # behavior off the current state of the customer.
        return Session.query(StatusEvent)\
            .filter(and_(StatusEvent.enterprise_id == enterprise_id,
                         StatusEvent.is_system == False,
                         StatusEvent.event_type == type(obj).__name__))\
                         .order_by(StatusEvent.short_name, StatusEvent.event_type).all()


    @staticmethod
    def full_delete(event_id):
        Session.execute("delete from core_status_event where event_id = %s" % event_id)
