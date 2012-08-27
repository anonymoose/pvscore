import pdb
import logging
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.validate import validate, validate_session
from app.controllers.base import BaseController
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn
from app.model.core.users import Users, UserPriv
from app.model.crm.purchase import Vendor
import app.lib.util as util

log = logging.getLogger(__name__)

class UsersController(BaseController):
    @view_config(route_name='crm.users.edit', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl(self.request.matchdict.get('username'))

        
    @view_config(route_name='crm.users.new', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    @view_config(route_name='crm.users.edit_current', renderer='/crm/users.edit.mako')
    @authorize(IsLoggedIn())
    def edit_current(self):
        return self._edit_impl(self.request.ctx.user.username)


    def _edit_impl(self, username=None):
        user = priv = None
        if username:
            user = self.request.ctx.user if self.request.ctx.user.username == username else Users.load(username)
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


    @view_config(route_name='crm.users.search', renderer='/crm/users.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        username = request.POST.get('username') 
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        return {
            'username' : username,
            'fname' : fname,
            'lname' : lname,
            'email' : email,
            'users' : Users.search(username, fname, lname, email)
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
        u = Users.load(self.request.POST.get('username'))
        if not u:
            u = Users()
            u.enterprise_id = self.enterprise_id

        if not u.priv:
            u.priv = UserPriv()
        u.priv.bind(self.request.POST, True, 'pv')
        u.priv.save()
        u.priv.flush()
        
        orig_pass = u.password
        bogus_pass = ''.join(['-' for i in range(u.password_len)]) if u.password_len else '-'
        u.bind(self.request.POST)
        if u.password != bogus_pass:
            u.password_len = len(u.password)
            u.password = Users.encode_password(u.password)
        else:
            u.password = orig_pass
        u.save()

        self.request.session.flash('Saved user %s' % u.username)
        return HTTPFound('/crm/users/edit/%s' % u.username)


    @view_config(route_name='crm.users.save_password', renderer='string')
    @authorize(IsLoggedIn())
    @validate((('username', 'required'),
               ('password', 'required')))
    def save_password(self):
        username = self.request.POST.get('username')
        u = Users.load(username)
        self.forbid_if(not u or u.enterprise_id != self.enterprise_id)
        u.bind(self.request.POST, False, self.request.GET.get('pfx'))
        u.password = Users.encode_password(u.password)
        u.save()
        return 'True'


        
