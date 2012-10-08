import logging
from pvscore.model.meta import Session
import pvscore.lib.util as util

log = logging.getLogger(__name__)

def init_model(engine, settings):
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

    
            


