import logging
import pdb
import app.lib.db as db
from app.model.meta import Session
import app.lib.util as util
from app.model.core.status import Status
from app.model.core.association import Association
from app.model.core.attribute import Attribute, AttributeValue
from app.model.crm.company import Company, Enterprise
from app.model.crm.campaign import Campaign
from app.model.crm.product import Product, ProductChild, ProductCategory, ProductCategoryJoin, ProductReturn, InventoryJournal
from app.model.crm.pricing import ProductPricing
from app.model.crm.customer import Customer
from app.model.crm.billing import Billing, BillingHistory
from app.model.crm.orderitem import OrderItem, OrderItemTermsAcceptance
from app.model.crm.customerorder import CustomerOrder
from app.model.crm.journal import Journal
from app.model.core.users import Users, UserPriv
from app.model.core.statusevent import StatusEvent
from app.model.core.statuseventreason import StatusEventReason
from app.model.crm.comm import Communication
from app.model.cms.site import Site
from app.model.core.kv import KeyValue
from app.model.core.asset import Asset
from app.model.crm.report import Report, ReportCompanyJoin
from app.model.crm.purchase import PurchaseOrder, PurchaseOrderItem, Vendor
from app.model.crm.discount import Discount
from app.model.crm.appointment import Appointment

log = logging.getLogger(__name__)

def init_model(engine, **settings):
    """
    import os
    app_extension = config['app_conf']['pvs.app.extension']
    extension_root = config['app_conf']['pvs.extension.root.dir']
    if os.path.exists('%s/%s/model' % (extension_root, app_extension)):
        m = '%s.model' % config['app_conf']['pvs.app.extension']
        #print 'load_model(%s)' % m
        exec 'import %s' % m


    from app.lib.plugin import plugin_registry
    for plugin_name in plugin_registry:
        plugin = plugin_registry[plugin_name]
        if os.path.exists(plugin.model_path):
            #print 'load_model(%s)' % plugin.model_package_name
            exec 'import %s' % plugin.model_package_name
    """

    # KB: [2011-09-05]: We make this check because when running under Nose,
    # It nags us that this has already been done.  This just eliminates the nag message.
    if Session.registry and not Session.registry.has():
        Session.configure(bind=engine)

    #load everything from the pvs.* keys in the config file into redis
    for setting in settings:
        log.debug('%s = %s' % (setting, settings[setting]))
        if setting.startswith('pvs.'):
            util.cache_set(setting, settings[setting])
            
            


