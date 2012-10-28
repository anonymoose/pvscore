from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel
import uuid
from pvscore.lib.sqla import GUID

class Association(ORMBase, BaseModel):
    __tablename__ = "core_association"
    __pk__ = 'id'

    id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    one_id = Column(Integer)
    one_type = Column(String(50))
    many_id = Column(Integer)
    many_type = Column(String(50))
    create_dt = Column(DateTime, server_default = text('now()'))

    
