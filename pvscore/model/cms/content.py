#pylint: disable-msg=E1101
import logging
from pvscore.lib.sqla import GUID
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import String, DateTime, Text
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from mako.template import Template
from pvscore.lib.dbcache import FromCache, invalidate
import pvscore.lib.util as util
import simplejson as json

log = logging.getLogger(__name__)


class Content(ORMBase, BaseModel):
    __tablename__ = 'cms_content'
    __pk__ = 'content_id'

    content_id = Column(GUID, primary_key=True)
    site_id = Column(GUID, ForeignKey('core_user.user_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    type = Column(String(50))
    name = Column(String(50))
    data = Column(Text)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    creator = relation('Users')
    site = relation('Site')

    @staticmethod
    def find_by_site(site):
        return Session.query(Content)\
            .options(FromCache('Content.find_by_site', site.site_id))\
            .filter(and_(Content.site == site,
                         Content.delete_dt == None)).order_by(Content.name).all()
    

    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Content.find_by_name_and_type', self.site_id)


    def render(self, **kwargs):
        if self.data:
            globs = kwargs or {}
            #globs['c'].catalog = Catalog(self.content.page.site, self.get_campaign(self.content.page.site))
            return util.literal(Template(self.data).render(globs))
        else:
            return ''


    def data_to_json(self):
        return json.loads(self.data) if self.data else ''


