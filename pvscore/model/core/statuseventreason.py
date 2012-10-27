from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Date
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel
import uuid
from pvscore.lib.sqla import GUID


class StatusEventReason(ORMBase, BaseModel):
    __tablename__ = 'core_status_event_reason'
    __pk__ = 'reason_id'

    reason_id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    event_id = Column(GUID, ForeignKey('core_status_event.event_id'))
    name = Column(String(50))
    create_dt = Column(Date, server_default = text('now()'))
    delete_dt = Column(Date)

    event = relation('StatusEvent', backref=backref('reasons', order_by='StatusEventReason.name'))
    
    

        
