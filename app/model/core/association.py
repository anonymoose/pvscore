from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Numeric, Text
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel

class Association(ORMBase, BaseModel):
    __tablename__ = "core_association"
    __pk__ = 'id'

    id = Column(Integer, primary_key=True)
    one_id = Column(Integer)
    one_type = Column(String(50))
    many_id = Column(Integer)
    many_type = Column(String(50))
    create_dt = Column(Date, server_default = text('now()'))

    
