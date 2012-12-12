from pvscore.controllers.base import BaseController
from pyramid.view import view_config
from pvscore.lib.validate import validate
from pvscore.lib.plugin import plugin_administration_link, plugin_customer_sidebar_link
import os

if 'PVS_TESTING' in os.environ and os.environ['PVS_TESTING'] == 'TRUE':

    class TsstController(BaseController):
        """ KB: [2011-09-02]: This guy is simply here to test out our framework stuff.
        Don't expose the routes to the outside world.
        meaning, hide them via nginx.
        It's named "TsstController" so nose tests doesn't try to run it magically.
        """

        @view_config(route_name='test.1', renderer='string')
        @validate((('fname', 'required'),
                   ('fname', 'string'),
                   ('email', 'required'),
                   ('email', 'string'),
                   ('email', 'email'),
                   ('password', 'required'),
                   ('confirm', 'required'),
                   ('password', 'equals', 'confirm'),
                   ('a', 'float'),
                   ('b', 'int'),
                   ('c', 'number')))
        def tsst_validate(self):
            return 'CALLED:tsst_validate'


        @plugin_administration_link(link_text="admin test 1", href="/tsst/test_admin_link")
        @view_config(route_name='test.2', renderer="string")
        def tsst_admin_link(self):
            return "Admin link landing page"


        @view_config(route_name='test.3', renderer='string')
        @validate([('a', 'float')])
        def tsst_float(self):
            return 'CALLED:tsst_float'


        @view_config(route_name='test.4', renderer='string')
        @validate([('a', 'int')])
        def tsst_int(self):
            return 'CALLED:tsst_int'


        @view_config(route_name='test.5', renderer='string')
        @validate([('a', 'string')])
        def tsst_string(self):
            return 'CALLED:tsst_string'


        @view_config(route_name='test.6', renderer='string')
        @validate([('a', 'number')])
        def tsst_number(self):
            return 'CALLED:tsst_number'


        @view_config(route_name='test.7', renderer='string')
        @validate([('a', 'equals', 'b')])
        def tsst_equals(self):
            return 'CALLED:tsst_equals'


        @view_config(route_name='test.8', renderer='string')
        @validate([('a', 'float')], '/tsst/tsst_redirto_post')
        def tsst_redirto(self):
            return 'CALLED:tsst_redirto'


        @view_config(route_name='test.9', renderer='string')
        def tsst_redirto_post(self):
            return 'REDIRECTED_TO OK'


        @plugin_customer_sidebar_link(link_text="customer sidebar test 1", href="/tsst/test_customer_sidebar_link")
        @view_config(route_name='test.10', renderer="string")
        def tsst_customer_sidebar_link(self):
            return "Customer sidebar landing page"





