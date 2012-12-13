#pylint: disable-msg=E1101
from sqlalchemy import Column, ForeignKey, or_
from sqlalchemy.types import Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import text
from pvscore.model.meta import ORMBase, BaseModel, Session
from pvscore.model.core.users import Users
from pvscore.model.crm.company import Company
from pvscore.thirdparty.dbcache import FromCache, invalidate
import logging
import uuid
from pvscore.lib.sqla import GUID

log = logging.getLogger(__name__)


class Site(ORMBase, BaseModel):
    __tablename__ = 'cms_site'
    __pk__ = 'site_id'

    site_id = Column(GUID, default=uuid.uuid4, nullable=False, unique=True, primary_key=True)
    company_id = Column(GUID, ForeignKey('crm_company.company_id'))
    default_campaign_id = Column(GUID, ForeignKey('crm_campaign.campaign_id'))
    user_created = Column(GUID, ForeignKey('core_user.user_id'))
    domain = Column(String(50))
    domain_alias0 = Column(String(50))
    domain_alias1 = Column(String(50))
    domain_alias2 = Column(String(50))
    description = Column(String(100))
    root_page_id = Column(Integer)
    create_dt = Column(DateTime, server_default = text('now()'))
    delete_dt = Column(DateTime)
    header_code = Column(String(1000))
    footer_code = Column(String(1000))
    config_json = Column(Text)
    seo_title = Column(String(512))
    seo_keywords = Column(String(1000))
    seo_description = Column(String(1000))
    google_analytics_id = Column(String(20))
    eyefoundit_analytics_id = Column(String(20))
    shipping_method = Column(String(50))
    tax_method = Column(String(50))
    robots_txt = Column(Text)
    maintenance_mode = Column(Boolean, default=False)
    namespace = Column(String(30))

    company = relation('Company', lazy='joined')
    default_campaign = relation('Campaign', lazy='joined')
    creator = relation('Users', primaryjoin=Users.user_id == user_created)

    def __repr__(self):  #pragma: no cover
        return '%s : %s' % (self.domain, self.company.name)


    @staticmethod
    def get_shipping_methods():
        return ['Flat', 'Per', 'Tiered', 'UPS', 'FedEx']


    @staticmethod
    def get_tax_methods():
        return ['Flat', 'No', 'Area']


    @staticmethod
    def find_all(enterprise_id):
        return Session.query(Site) \
            .options(FromCache('Site.find_all', enterprise_id)) \
            .join((Company, Company.company_id == Site.company_id))\
            .filter(Company.enterprise_id == enterprise_id)\
            .order_by(Site.domain).all()


    @staticmethod
    def find_by_host(host):
        www_host = (host if host.startswith('www.') else 'www.%s' % host).replace(':80', '')
        short_host = host.replace('www.', '').replace(':80', '')
        return Session.query(Site) \
            .options(FromCache('Site.find_by_host', host)) \
            .filter(or_(
                Site.domain==host,
                Site.domain==www_host,
                Site.domain==short_host,
                Site.domain_alias0==host,
                Site.domain_alias0==www_host,
                Site.domain_alias0==short_host,
                Site.domain_alias1==host,
                Site.domain_alias1==www_host,
                Site.domain_alias1==short_host,
                Site.domain_alias2==host,
                Site.domain_alias2==www_host,
                Site.domain_alias2==short_host)).first()


    def invalidate_caches(self, **kwargs):
        invalidate(self, 'Site.find_by_host', self.domain)
        invalidate(self, 'Site.find_by_host', 'www.'+self.domain)
        invalidate(self, 'Site.find_all', self.company.enterprise_id)


    # def store_asset(self, asset_data, folder):
    #     """ KB: [2010-11-18]:
    #     called from pvscore.controllers.cms.asset::upload()
    #     http://pylonsbook.com/en/1.1/working-with-forms-and-validators.html
    #     """
    #     fs_path = os.path.join(
    #         '%s%s' % (self.site_full_directory, folder),
    #         asset_data.filename.replace(os.sep, '_')
    #         )
    #     permanent_file = open(fs_path, 'wb')
    #     shutil.copyfileobj(asset_data.file, permanent_file)
    #     asset_data.file.close()
    #     permanent_file.close()
    #     # at this point everything is saved to disk. Create an asset object in
    #     # the DB to remember it.
    #     return Asset.create_new(asset_data.filename,
    #                          fs_path,
    #                          '{base}/{f}'.format(base=self.site_web_directory('images'),
    #                                              f=asset_data.filename),
    #                          self).flush()

    # def get_config(self):
    #     #dir = '/Users/kbedwell/dev/pydev/wm/app/sites/' + self.site_directory
    #     #cache_key = 'site.config.%s' % self.site_id
    #     #if not util.cache_has_key(cache_key):
    #     directory = self.site_full_directory
    #     cfgfile = directory + '/site.config'
    #     if os.path.exists(cfgfile):
    #         config = ConfigParser.ConfigParser()
    #         config.read(cfgfile)
    #         return config


    # def get_shipping(self):
    #     from pvscore.lib.plugin import plugin_registry
    #     cfg = self.get_config()
    #     shipping_type = cfg.get('SHIPPING', 'type')
    #     pe = plugin_registry[shipping_type]
    #     return pe.obj

    # @property
    # def site_full_directory(self):
    #     return "{root_dir}/{dirname}".format(root_dir=util.nvl(util.cache_get('pvs.site.root.dir'), 'sites'),
    #                                          dirname=self.site_directory)


    # @property
    # def site_directory(self):
    #     return str(self.site_id)


    # def create_dir_structure(self):
    #     dirname = self.site_full_directory
    #     util.mkdir_p(dirname)
    #     util.mkdir_p("%s/images" % dirname)
    #     util.mkdir_p("%s/script" % dirname)
    #     util.mkdir_p("%s/cache" % dirname)


    # def site_web_directory(self, subdir=''):
    #     """ KB: [2011-02-02]: The "companies" below corresponds to the /companies location in the nginx conf file """
    #     return "/sites/{dirname}/{subdir}".format(dirname=self.site_directory, subdir=subdir)

