#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, or_
from sqlalchemy.types import Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.core.users import Users
import logging
import uuid
from pvscore.lib.sqla import GUID

log = logging.getLogger(__name__)

class Appointment(ORMBase, BaseModel):
    __tablename__ = 'crm_appointment'
    __pk__ = 'appointment_id'

    appointment_id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    customer_id = Column(GUID, ForeignKey('crm_customer.customer_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    user_assigned = Column(GUID, ForeignKey('core_user.user_id'))
    user_completed = Column(GUID, ForeignKey('core_user.user_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    title = Column(String(255))
    description = Column(Text)
    calendar_type = Column(String(50))
    remind = Column(Boolean)
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)
    completed_dt = Column(Date)
    start_dt = Column(Date)
    start_time = Column(String(20))
    end_time = Column(String(20))
    end_dt = Column(Date)
    private = Column(Boolean)
    phone = Column(String(20))
    data_1 = Column(String(250))
    data_2 = Column(String(250))

    creator = relation('Users', primaryjoin=Users.user_id == user_created)
    completor = relation('Users', primaryjoin=Users.user_id == user_completed)
    assigned = relation('Users', primaryjoin=Users.user_id == user_assigned)
    customer = relation('Customer', backref=backref('appointments'))
    status = relation('Status')


    @staticmethod
    def search(enterprise_id, title, description):
        t_clause = d_clause = ''
        if title:
            t_clause = "and appt.title like '%%%s%%'" % title
        if description:
            d_clause = "and appt.description like '%%%s%%'" % description
        sql = """SELECT appt.* FROM crm_appointment appt, core_user u where
                 u.user_id = appt.user_created
                 and (u.enterprise_id = '{entid}' or u.enterprise_id is null)
                {title} {descr}""".format(entid=enterprise_id, 
                                          title=t_clause, 
                                          descr=d_clause)
        return Session.query(Appointment).from_statement(sql).all()


    @staticmethod
    def find_by_customer(customer):
        return Session.query(Appointment).filter(Appointment.customer == customer).order_by(Appointment.start_dt.desc(),
                                                                                             Appointment.start_time.asc()).all()

    
    @staticmethod
    def find_by_user(user):
        return Session.query(Appointment).filter(or_(Appointment.creator == user,
                                                     Appointment.assigned == user)).order_by(Appointment.start_dt.desc(),
                                                                                             Appointment.start_time.asc()).all()


    @staticmethod
    def find_by_month(year, month, user):
        #return Session.query(Appointment).from_statement("""select *, ((start_time + 5) - %s) from crm_appointment where % user.tz_offset
        return Session.query(Appointment).from_statement("""select * from crm_appointment where 
                                                            (user_created = :creator or user_assigned = :creator)
                                                            and date_part('month', start_dt) = :month
                                                            and date_part('year', start_dt) = :year 
                                                            order by start_time asc""" ).params(creator=user.user_id, year=year, month=month).all()


    @staticmethod
    def find_by_day(year, month, day, user):
        return Session.query(Appointment).from_statement("""select * from crm_appointment where 
                                                            (user_created = :creator or user_assigned = :creator)
                                                            and date_part('month', start_dt) = :month
                                                            and date_part('year', start_dt) = :year 
                                                            and date_part('day', start_dt) = :day
                                                            order by start_time asc""").params(creator=user.user_id, year=year, month=month, day=day).all()

    @staticmethod
    def full_delete(appointment_id):
        Session.execute("delete from crm_appointment where appointment_id = '%s'" % appointment_id)

        
