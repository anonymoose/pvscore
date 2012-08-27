import os
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date, Numeric, Text
from sqlalchemy.orm import relation, backref
from sqlalchemy.sql.expression import text
from app.model.meta import ORMBase, BaseModel, Session
from app.lib.dbcache import FromCache, invalidate

class Asset(ORMBase, BaseModel):
    __tablename__ = "core_asset"
    __pk__ = 'id'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    mimetype = Column(String(30))
    fs_path = Column(String(512))
    web_path = Column(String(512))
    fk_type = Column(String(50))
    fk_id = Column(Integer)
    create_dt = Column(Date, server_default = text('now()'))
    status_id = Column(Integer, ForeignKey('core_status.status_id'))

    status = relation('Status')

    @property
    def exists(self):
        return os.path.exists(self.fs_path)

    def delete(self):
        if os.path.exists(self.fs_path):
            os.remove(self.fs_path)
        self.invalidate_caches()
        Session.delete(self)

    @staticmethod
    def find_for_object(obj):
        fk_type = type(obj).__name__
        fk_id = getattr(obj, obj.__pk__)
        return Session.query(Asset) \
            .options(FromCache('Asset.find_for_object', '%s/%s' % (fk_type, fk_id))) \
            .filter(and_(Asset.fk_type == fk_type,
                         Asset.fk_id == fk_id)).all()

    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Asset.find_for_object', '%s/%s' % (self.fk_type, self.fk_id))

    @staticmethod
    def create_new(name, fs_path, web_path, fk_type, fk_id):
        if os.path.exists(fs_path):
            a = Asset()
            a.fs_path = fs_path
            a.web_path = web_path
            a.name = name
            a.fk_type = fk_type
            a.fk_id = fk_id
            a.save()
            return a


