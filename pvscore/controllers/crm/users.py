import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.lib.validate import validate
from pvscore.controllers.base import BaseController
from pvscore.lib.decorators.authorize import authorize 
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.core.users import Users, UserPriv
from pvscore.model.crm.purchase import Vendor
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class UsersController(BaseController):
    @view_config(route_name='crm.users.edit', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl(self.request.matchdict.get('user_id'))

        
    @view_config(route_name='crm.users.new', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    @view_config(route_name='crm.users.edit_current', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def edit_current(self):
        return HTTPFound('/crm/users/edit/%s' % self.request.ctx.user.user_id)


    def _edit_impl(self, user_id=None):
        user = priv = None
        if user_id:
            user = self.request.ctx.user if self.request.ctx.user.user_id == user_id else Users.load(user_id)
            priv = user.priv if user.priv else UserPriv()
        else:
            user = Users()
            priv = UserPriv()
        return {
            'user_types':Users.get_user_types(),
            'vendors' :util.select_list(Vendor.find_all(self.enterprise_id), 'vendor_id', 'name', True),
            'user' : user,
            'priv' : priv
            }


    @view_config(route_name='crm.users.list', renderer='/crm/users.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'users' : Users.find_all(self.enterprise_id)}


    @view_config(route_name='crm.users.save')
    @authorize(IsLoggedIn())
    @validate((('fname', 'required'), 
               ('fname', 'string'),
               ('lname', 'required'), 
               ('lname', 'string'),
               ('email', 'required'), 
               ('email', 'string'),
               ('email', 'email'),
               ('password', 'equals', 'confirm')))
    def save(self):
        usr = Users.load(self.request.POST.get('user_id'))
        if not usr:
            usr = Users()
            usr.enterprise_id = self.enterprise_id

        if not usr.priv:
            usr.priv = UserPriv()
        usr.priv.bind(self.request.POST, True, 'pv')
        usr.priv.save()
        usr.priv.flush()
        
        orig_pass = usr.password
        bogus_pass = ''.join(['-' for _ in range(usr.password_len)]) if usr.password_len else '-'
        usr.bind(self.request.POST)
        if usr.password != bogus_pass:
            usr.password_len = len(usr.password)
            usr.password = Users.encode_password(usr.password)
        else:
            usr.password = orig_pass
        usr.save()
        usr.flush()
        usr.invalidate_self()

        self.request.session.flash('Saved user %s' % usr.user_id)
        return HTTPFound('/crm/users/edit/%s' % usr.user_id)


    @view_config(route_name='crm.users.save_password', renderer='string')
    @authorize(IsLoggedIn())
    @validate((('user_id', 'required'),
               ('password', 'required')))
    def save_password(self):
        user_id = self.request.POST.get('user_id')
        usr = Users.load(user_id)
        self.forbid_if(not usr or usr.enterprise_id != self.enterprise_id)
        usr.bind(self.request.POST, False, self.request.GET.get('pfx'))
        usr.password = Users.encode_password(usr.password)
        usr.save()
        return 'True'


    # @view_config(route_name='crm.users.search', renderer='/crm/users.search.mako')
    # @authorize(IsLoggedIn())
    # def search(self):
    #     username = self.request.POST.get('username') 
    #     fname = self.request.POST.get('fname')
    #     lname = self.request.POST.get('lname')
    #     email = self.request.POST.get('email')
    #     return {
    #         'username' : username,
    #         'fname' : fname,
    #         'lname' : lname,
    #         'email' : email,
    #         'users' : Users.search(self.enterprise_id, username, fname, lname, email)
    #         }

