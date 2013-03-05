#pylint: disable-msg=E1101
import logging, uuid
from pvscore.lib.sqla import GUID
from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import String, DateTime, Text
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from mako.template import Template
from pvscore.thirdparty.dbcache import FromCache, invalidate
import pvscore.lib.util as util
from pvscore.model.core.users import Users
from pvscore.model.cms.site import Site
import unicodedata

log = logging.getLogger(__name__)


class Content(ORMBase, BaseModel):
    """
    alter table cms_content add column seo_title varchar(500);
    alter table cms_content add column seo_keywords varchar(1000);
    alter table cms_content add column seo_description varchar(1000);
    """

    __tablename__ = 'cms_content'
    __pk__ = 'content_id'

    content_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    site_id = Column(GUID, ForeignKey('cms_site.site_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    type = Column(String(50))
    name = Column(String(50))
    data = Column(Text)
    seo_title = Column(String(512))
    seo_keywords = Column(String(1000))
    seo_description = Column(String(1000))
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)

    creator = relation('Users', primaryjoin=Users.user_id == user_created)
    site = relation('Site', primaryjoin=Site.site_id == site_id)

    @staticmethod
    def find_by_site(site):
        return Session.query(Content)\
            .options(FromCache('Content.find_by_site', site.site_id))\
            .filter(and_(Content.site == site,
                         Content.delete_dt == None)).order_by(Content.name).all()


    @staticmethod
    def find_by_name(site, name, cached=True):
        if cached:
            return Session.query(Content)\
                .options(FromCache('Content.find_by_name', "%s/%s" % (site.site_id, name)))\
                .filter(and_(Content.site == site,
                             Content.name == name,
                             Content.delete_dt == None)).first()
        else:
            return Session.query(Content)\
                .filter(and_(Content.site == site,
                             Content.name == name,
                             Content.delete_dt == None)).first()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Content.find_by_name', '%s/%s' % (self.site_id, self.name))
        invalidate(self, 'Content.find_by_site', self.site_id)


    def render(self, **kwargs):
        ret = ''
        if self.data:
            globs = kwargs or {}
            data = str(self.data) #unicodedata.normalize('NFKD', self.data).encode('ascii','ignore')
            ret = util.literal(Template(data).render(**globs))   #pylint: disable-msg=W0142
        return ret


def make_content_function(site, request):
    def content(name, cached=True):
        content = Content.find_by_name(site, name, cached)
        return content.render(request=request) if content else ''
    return content
