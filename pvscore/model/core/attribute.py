from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, joinedload
from pvscore.model.meta import ORMBase, BaseModel, Session
#from pvscore.thirdparty.dbcache import FromCache, invalidate
import uuid
from pvscore.lib.sqla import GUID

class Attribute(ORMBase, BaseModel):
    """
    Attributes are vertically oriented data for a given FK
    customer (Ken Bedwell) -->      attribute_value ("Wayne") --> attribute ("Middle Name")
                                    attribute_value ("Amy")   --> attribute ("Wife's Name")
                                    attribute_value ("35")    --> attribute ("Age")
    """

    __tablename__ = 'core_attribute'
    __pk__ = 'attr_id'

    attr_id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    fk_type = Column(String(50))
    attr_name = Column(String(100))
    attr_type = Column(String(32))

    @staticmethod
    def find(fk_type, attr_name):
        #pylint: disable-msg=E1101
        # TODO: Fix Attribute caching:  .options(FromCache('Attribute.find.%s.%s' % (fk_type, attr_name)))\
        return Session.query(Attribute)\
            .filter(and_(Attribute.fk_type == fk_type,
                         Attribute.attr_name == attr_name)).first()


    @staticmethod
    def find_values(obj):
        avs = AttributeValue.find_all(obj)
        retval = {}
        for avl in avs:
            retval[avl.attribute.attr_name] = avl.attr_value
        return retval


    @staticmethod
    def create_new(fk_type, attr_name, attr_type='str'):
        att = Attribute()
        att.fk_type = fk_type
        att.attr_name = attr_name
        att.attr_type = attr_type
        att.save()
        return att


    def set(self, obj, value):
        avl = AttributeValue()
        avl.attribute = self
        avl.fk_type = self.fk_type
        avl.fk_id = getattr(obj, obj.__pk__)
        avl.attr_value = value
        avl.save()
        return avl


    def get(self, obj):
        avl = AttributeValue.find(self, getattr(obj, obj.__pk__))
        return avl.attr_value if avl else None


    @staticmethod
    def clear_all(fk_type, fk_id):
        AttributeValue.clear_all(fk_type, fk_id)


class AttributeValue(ORMBase, BaseModel):
    __tablename__ = 'core_attribute_value'
    __pk__ = 'attr_value_id'

    attr_value_id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    attr_id = Column(GUID, ForeignKey('core_attribute.attr_id'))
    attr_value = Column(String(2000))
    fk_type = Column(String(50))
    fk_id = Column(Integer)

    attribute = relation('Attribute')


    @staticmethod
    def clear_all(fk_type, fk_id):
        #pylint: disable-msg=E1101
        Session.execute("delete from core_attribute_value where fk_type = '%s' and fk_id = '%s'" % (fk_type, fk_id))


    @staticmethod
    def find(attr, fk_id):
        #pylint: disable-msg=E1101
        #TODO: Fix attribute value caching:  .options(FromCache('AttributeValue.find.%s.%s' % (attr.attr_id, fk_id)))\
        return Session.query(AttributeValue)\
            .filter(and_(AttributeValue.fk_type == attr.fk_type,
                         AttributeValue.fk_id == fk_id,
                         AttributeValue.attr_id == attr.attr_id)).first()


    @staticmethod
    def find_all(obj):
        #pylint: disable-msg=E1101
        fk_type = type(obj).__name__ 
        fk_id = getattr(obj, obj.__pk__)

        # TODO: Fix attribute value caching:    .options(FromCache('AttributeValue.%s.%s' % (fk_type, fk_id))) \
        return Session.query(AttributeValue).join((Attribute, AttributeValue.attr_id == Attribute.attr_id)) \
            .options(joinedload('attribute')) \
            .filter(and_(AttributeValue.fk_type == fk_type,
                         AttributeValue.fk_id == fk_id)) \
                         .order_by(AttributeValue.attr_value_id).all()


    @staticmethod
    def invalidate_attributes(obj):
        fk_type = type(obj).__name__ 
        fk_id = getattr(obj, obj.__pk__)
        #invalidate(obj, 'AttributeValue.%s.%s' % (fk_type, fk_id))
        
    # @staticmethod
    # def find_fk_id_by_value(fk_type, attr_name, attr_value):
    #     #pylint: disable-msg=E1101
    #     ret = Session.query("fk_id").from_statement("""SELECT cav.fk_id FROM core_attribute_value cav, core_attribute ca
    #                                              where
    #                                              cav.attr_id = ca.attr_id and
    #                                              ca.fk_type = '{fk_type}' and
    #                                              ca.attr_name = '{attr_name}' and
    #                                              cav.fk_type = '{fk_type}' and
    #                                              cav.attr_value = '{attr_value}'""".format(fk_type=fk_type, 
    #                                                                                        attr_name=attr_name,
    #                                                                                        attr_value=attr_value)).one()
    #     return ret[0]

                       
