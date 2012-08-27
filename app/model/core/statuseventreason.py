from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Numeric, Text
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel

class StatusEventReason(ORMBase, BaseModel):
    __tablename__ = 'core_status_event_reason'
    __pk__ = 'reason_id'

    reason_id = Column(Integer, primary_key = True)
    event_id = Column(Integer, ForeignKey('core_status_event.event_id'))
    name = Column(String(50))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)

    event = relation('StatusEvent', backref=backref('reasons', order_by='StatusEventReason.name'))
    
    

        
