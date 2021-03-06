#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, or_, and_
from sqlalchemy.types import String, DateTime, Text, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.core.users import Users
import pvscore.lib.util as util
import logging
import uuid
from pvscore.lib.sqla import GUID

log = logging.getLogger(__name__)

class Appointment(ORMBase, BaseModel):

    __tablename__ = 'crm_appointment'
    __pk__ = 'appointment_id'

    appointment_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    customer_id = Column(GUID, ForeignKey('crm_customer.customer_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    user_assigned = Column(GUID, ForeignKey('core_user.user_id'))
    user_completed = Column(GUID, ForeignKey('core_user.user_id'))
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    title = Column(String(255))
    description = Column(Text)
    calendar_type = Column(String(50))
    remind = Column(Boolean)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    completed_dt = Column(DateTime)
    start_dt = Column(DateTime)
    start_time = Column(String(20))
    end_time = Column(String(20))
    end_dt = Column(DateTime)
    timezone = Column(String(100))
    private = Column(Boolean)
    phone = Column(String(20))
    data_1 = Column(String(250))
    data_2 = Column(String(250))
    public = Column(Boolean)

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
    def find_public(enterprise_id):
        return Session.query(Appointment)\
            .join((Users, Appointment.user_created == Users.user_id))\
            .filter(and_(Appointment.public == True,
                         Appointment.delete_dt == None,
                         Users.enterprise_id == enterprise_id,
                         Appointment.start_dt >= util.now()))\
            .order_by(Appointment.start_dt.desc(), Appointment.start_time.asc()).all()


    @staticmethod
    def find_by_user(user):
        return Session.query(Appointment)\
            .filter(or_(Appointment.creator == user,
                        Appointment.assigned == user))\
                        .order_by(Appointment.start_dt.asc(),
                                  Appointment.start_time.asc()).all()


    @staticmethod
    def find_future_by_user(user):
        return Session.query(Appointment).filter(and_(Appointment.start_dt > util.yesterday(),
                                                      or_(Appointment.creator == user,
                                                          Appointment.assigned == user))).order_by(Appointment.start_dt.asc(),
                                                                                                  Appointment.start_time.asc()).all()

    @staticmethod
    def find_by_month(year, month, user):
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

