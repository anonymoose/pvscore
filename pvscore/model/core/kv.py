from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime, Text
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel
import uuid
from pvscore.lib.sqla import GUID


class KeyValue(ORMBase, BaseModel):
    __tablename__ = "core_key_value"
    __pk__ = 'id'

    id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    key = Column(String(256))
    value = Column(Text)
    fk_type = Column(String(50))
    fk_id = Column(Integer)
    create_dt = Column(DateTime, server_default = text('now()'))

    # def __repr__(self):
    #     return '%s : %s %s %s' % (self.id, self.key, self.fk_type, self.fk_id)

    # @staticmethod
    # def find(key, obj):

    #     # KB: [2011-02-10]: Find the most recently added item.
    #     #pylint: disable-msg=E1101
    #     return Session.query(KeyValue).filter(and_(KeyValue.key == key,
    #                                                KeyValue.fk_type == type(obj).__name__,
    #                                                KeyValue.fk_id == getattr(obj, obj.__pk__))) \
    #                                                .order_by(KeyValue.create_dt.desc())\
    #                                                .first()

    # @staticmethod
    # def create_new(key, value, obj):
    #     kvl = KeyValue()
    #     kvl.key = key
    #     kvl.value = value
    #     kvl.fk_type = type(obj).__name__
    #     kvl.fk_id = getattr(obj, obj.__pk__)
    #     kvl.save()
    #     return kvl
    

    
