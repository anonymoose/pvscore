from pvscore.tests import TestController, secure
from pvscore.lib.plugin import init_controllers, plugin_registry
from pyramid.config import Configurator
from pvscore import init_pvscore
import paste.deploy   #pylint: disable-msg=F0401

class TestPlugin(TestController):

    @secure
    def test_configuration(self):
        settings = paste.deploy.appconfig('config:unittest.ini', relative_to='.')
        cfg = Configurator(settings=settings)
        init_pvscore(cfg, settings)
        init_controllers(cfg, 'pvscore.controllers._test')
        self.assertEqual(plugin_registry.category('administration_link')[0], 'admin test 1')
        self.assertEqual(plugin_registry.getattr('administration_link', 'admin test 1', 'href'), '/tsst/test_admin_link')
        self.assertEqual(plugin_registry.category('customer_sidebar_link')[0], 'customer sidebar test 1')
        self.assertEqual(plugin_registry.getattr('customer_sidebar_link', 'customer sidebar test 1', 'href'), '/tsst/test_customer_sidebar_link')




