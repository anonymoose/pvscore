import os, shutil
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.lib.dbcache import invalidate , FromCache
import uuid
from pvscore.lib.sqla import GUID
import pvscore.lib.util as util

class Asset(ORMBase, BaseModel):
    __tablename__ = "core_asset"
    __pk__ = 'id'

    id = Column(GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    status_id = Column(GUID, ForeignKey('core_status.status_id'))
    enterprise_id = Column(GUID, ForeignKey('crm_enterprise.enterprise_id'))
    extension = Column(String(10))
    name = Column(String(100))
    description = Column(String(1000))
    fk_type = Column(String(50))
    fk_id = Column(Integer)
    create_dt = Column(DateTime, server_default = text('now()'))
    mimetype = Column(String(30)) #
    fs_path = Column(String(512)) #
    web_path = Column(String(512)) #


    status = relation('Status')

    @property
    def exists(self):
        return os.path.exists(self.filesystem_path)


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

    @property
    def path(self):
        return "{reldir}/{assid}{ext}".format(reldir=self.relative_dir,
                                              assid=self.id,
                                              ext=self.extension)

    
    @property
    def absolute_path(self):
        return "/%s" % self.path

    
    @property
    def relative_dir(self):
        this_id = str(self.id)
        return "enterprises/{enterprise_id}/assets/{_0}/{_1}/{_2}".format(enterprise_id=self.enterprise_id,
                                                                          _0=this_id[0],
                                                                          _1=this_id[1],
                                                                          _2=this_id[2])

    @staticmethod
    def create_new(obj, enterprise_id, request):
        asset_data = request.POST['Filedata']
        ass = Asset()
        ass.fk_type = type(obj).__name__
        ass.fk_id = getattr(obj, obj.__pk__)
        ass.enterprise_id = enterprise_id
        ass.name = asset_data.filename
        ass.extension = os.path.splitext(asset_data.filename)[1]
        ass.save()
        ass.flush()        
        storage_root = Asset.get_storage_root()
        fs_real_dir = "{root}/enterprises/{reldir}".format(root=storage_root, reldir=ass.relative_dir)
        util.mkdir_p(fs_real_dir)
        fs_real_path = "{fs_real_dir}/{assid}{ext}".format(fs_real_dir=fs_real_dir,
                                                           assid=ass.id,
                                                           ext=ass.extension)
        with open(fs_real_path, 'wb') as permanent_file: 
            shutil.copyfileobj(asset_data.file, permanent_file)
            asset_data.file.close()
        return ass

    @staticmethod
    def get_storage_root():
        return util.cache_get('pvs.enterprise.root.dir')


    @property
    def filesystem_path(self):
        return '%s/%s' % (Asset.get_storage_root(), self.path)

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
