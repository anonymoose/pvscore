from sqlalchemy import Column, ForeignKey, and_, or_
from sqlalchemy.types import Integer, String, Date, Numeric, Text, DateTime
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.model.core.statusevent import StatusEvent
from app.model.core.users import Users

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
    event = relation('StatusEvent')

    @staticmethod
    def add(customer, obj, event, note=None, user=None):
        """
        if user == None:
            try:
                if 'user_id' in session:
                    user = Users.load(session['user_id'] )
            except: pass
        """
        s = Status()
        s.event = event
        if customer: s.customer = customer
        s.fk_type = type(obj).__name__
        s.fk_id = getattr(obj, obj.__pk__)
        s.note = note
        s.user = Session.merge(user) if user else None
        s.save()
        if event.change_status:
            obj.status = s
            obj.save()
        return s


    @staticmethod
    def find_event(enterprise_id, obj, short_name):
        return StatusEvent.find(enterprise_id, type(obj).__name__, short_name)


    @staticmethod
    def find_by_event(customer, obj, event):
        return Session.query(Status).filter(and_(Status.customer_id==customer.customer_id,
                                                 Status.fk_id == getattr(obj, obj.__pk__),
                                                 Status.fk_type == type(obj).__name__,
                                                 Status.event == event)).order_by(Status.status_id.desc()).all()


    @staticmethod
    def find(obj):
        return Session.query(Status)\
            .filter(and_(Status.fk_id==getattr(obj, obj.__pk__),
                         Status.fk_type==type(obj).__name__))\
            .order_by(Status.status_id.desc()).all()


    @staticmethod
    def find_by_customer(customer):
        return Session.query(Status)\
            .filter(Status.customer_id==customer.customer_id)\
            .order_by(Status.status_id.desc()).all()


    """ KB: [2010-09-16]: Customer is a stanard python-ish property because of circular foreign key issues between status and customer """
    def _get_customer(self):
        return Customer.load(self.customer_id)
    def _set_customer(self, customer):
        self.customer_id = customer.customer_id
    customer = property(_get_customer, _set_customer)
