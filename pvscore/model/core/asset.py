import os
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, Date
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.lib.dbcache import invalidate , FromCache


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


    @staticmethod
    def find_for_object(obj):
        fk_type = type(obj).__name__
        fk_id = getattr(obj, obj.__pk__)
        #pylint: disable-msg=E1101
        return Session.query(Asset) \
            .options(FromCache('Asset.find_for_object', '%s/%s' % (fk_type, fk_id))) \
            .filter(and_(Asset.fk_type == fk_type,
                         Asset.fk_id == fk_id)).all()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Asset.find_for_object', '%s/%s' % (self.fk_type, self.fk_id))


    def get_listing(self):
        # KB: [2012-09-27]: if this is applicable you'll know it.
        # otherwise it will barf.
        from pvscore.model.crm.listing import Listing
        return Listing.load(self.fk_id)


    # def delete(self):
    #     if os.path.exists(self.fs_path):
    #         os.remove(self.fs_path)
    #     self.invalidate_caches()
    #     Session.delete(self)   #pylint: disable-msg=E1101


    # @staticmethod
    # def create_new(name, fs_path, web_path, fk_type, fk_id):
    #     if os.path.exists(fs_path):
    #         ast = Asset()
    #         ast.fs_path = fs_path
    #         ast.web_path = web_path
    #         ast.name = name
    #         ast.fk_type = fk_type
    #         ast.fk_id = fk_id
    #         ast.save()
    #         return ast
