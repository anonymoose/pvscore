import logging
from pvscore.model.meta import Session
import pvscore.lib.util as util
# from pvscore.model.core.status import Status
# from pvscore.model.core.association import Association
# from pvscore.model.core.attribute import Attribute, AttributeValue
# from pvscore.model.crm.company import Company, Enterprise
# from pvscore.model.crm.campaign import Campaign
# from pvscore.model.crm.product import Product, ProductChild, ProductCategory, ProductCategoryJoin, ProductReturn, InventoryJournal
# from pvscore.model.crm.pricing import ProductPricing
# from pvscore.model.crm.customer import Customer
# from pvscore.model.crm.billing import Billing, BillingHistory
# from pvscore.model.crm.orderitem import OrderItem, OrderItemTermsAcceptance
# from pvscore.model.crm.customerorder import CustomerOrder
# from pvscore.model.crm.journal import Journal
# from pvscore.model.core.users import Users, UserPriv
# from pvscore.model.core.statusevent import StatusEvent
# from pvscore.model.core.statuseventreason import StatusEventReason
# from pvscore.model.crm.comm import Communication
# from pvscore.model.cms.site import Site
# from pvscore.model.core.kv import KeyValue
# from pvscore.model.core.asset import Asset
# from pvscore.model.crm.report import Report, ReportCompanyJoin
# from pvscore.model.crm.purchase import PurchaseOrder, PurchaseOrderItem, Vendor
# from pvscore.model.crm.discount import Discount
# from pvscore.model.crm.appointment import Appointment

log = logging.getLogger(__name__)

def init_model(engine, **settings):
    """
    import os
    app_extension = config['app_conf']['pvs.core.extension']
    extension_root = config['app_conf']['pvs.extension.root.dir']
    if os.path.exists('%s/%s/model' % (extension_root, app_extension)):
        m = '%s.model' % config['app_conf']['pvs.core.extension']
        #print 'load_model(%s)' % m
        exec 'import %s' % m


    from pvscore.lib.plugin import plugin_registry
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
            
            


