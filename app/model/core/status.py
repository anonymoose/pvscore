from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Text, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.core.statusevent import StatusEvent


class Status(ORMBase, BaseModel):
    __tablename__ = 'core_status'
    __pk__ = 'status_id'

    status_id = Column(Integer, primary_key = True)
    event_id = Column(Integer, ForeignKey('core_status_event.event_id'))
    customer_id = Column(Integer)
    fk_type = Column(String(50))
    fk_id = Column(Integer)
    username = Column(String(75), ForeignKey('core_user.username'))
    note = Column(Text)
    create_dt = Column(DateTime, server_default=text('now()'))

    user = relation('Users')
    event = relation('StatusEvent', lazy="joined")


    @staticmethod
    def add(customer, obj, event, note=None, user=None):
        stat = Status()
        stat.event = event
        if customer:
            stat.customer_id = customer.customer_id
        stat.fk_type = type(obj).__name__
        stat.fk_id = getattr(obj, obj.__pk__)
        stat.note = note
        stat.user = Session.merge(user) if user else None #pylint: disable-msg=E1101
        stat.save()
        if event.change_status:
            obj.status = stat
        obj.save()
        stat.flush()
        return stat


    @staticmethod
    def find_event(enterprise_id, obj, short_name):
        return StatusEvent.find(enterprise_id, type(obj).__name__, short_name)


    @staticmethod
    def find_by_event(customer, obj, event):
        #pylint: disable-msg=E1101
        return Session.query(Status).filter(and_(Status.customer_id==customer.customer_id,
                                                 Status.fk_id == getattr(obj, obj.__pk__),
                                                 Status.fk_type == type(obj).__name__,
                                                 Status.event == event)).order_by(Status.status_id.desc()).all()


    @staticmethod
    def find(obj):
        #pylint: disable-msg=E1101
        return Session.query(Status)\
            .filter(and_(Status.fk_id==getattr(obj, obj.__pk__),
                         Status.fk_type==type(obj).__name__))\
            .order_by(Status.status_id.desc()).all()


    @staticmethod
    def find_by_customer(customer):
        #pylint: disable-msg=E1101
        return Session.query(Status)\
            .filter(Status.customer_id==customer.customer_id)\
            .order_by(Status.status_id.desc()).all()


