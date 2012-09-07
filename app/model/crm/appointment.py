from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Numeric, Text, Boolean
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.core.users import Users
from app.model.crm.customer import Customer

class Appointment(ORMBase, BaseModel):
    __tablename__ = 'crm_appointment'
    __pk__ = 'appointment_id'

    appointment_id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey('crm_customer.customer_id'))
    title = Column(String(255))
    description = Column(Text)
    calendar_type = Column(String(50))
    remind = Column(Boolean)
    user_created = Column(String(50), ForeignKey('core_user.username'))
    user_assigned = Column(String(50), ForeignKey('core_user.username'))
    user_completed = Column(String(50), ForeignKey('core_user.username'))
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
    status_id = Column(Integer, ForeignKey('core_status.status_id'))

    creator = relation('Users', primaryjoin=Users.username == user_created)
    completor = relation('Users', primaryjoin=Users.username == user_completed)
    assigned = relation('Users', primaryjoin=Users.username == user_assigned)
    customer = relation('Customer', backref=backref('appointments'))
    status = relation('Status')


    @staticmethod
    def search(title, description):
        t_clause = d_clause = ''
        if title:
            t_clause = "and appt.title like '%%%s%%'" % title
        if description:
            d_clause = "and appt.description like '%%%s%%'" % description
        sql = """SELECT appt.* FROM crm_appointment appt, core_user u where
                 u.username = appt.user_created and u.enterprise_id = {entid}
                {title} {descr}""".format(entid=BaseModel.get_enterprise_id(), 
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
                                                            order by start_time asc""" ).params(creator=user.username, year=year, month=month).all()


    @staticmethod
    def find_by_day(year, month, day, user):
        return Session.query(Appointment).from_statement("""select * from crm_appointment where 
                                                            (user_created = :creator or user_assigned = :creator)
                                                            and date_part('month', start_dt) = :month
                                                            and date_part('year', start_dt) = :year 
                                                            and date_part('day', start_dt) = :day
                                                            order by start_time asc""").params(creator=user.username, year=year, month=month, day=day).all()
