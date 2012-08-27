import pdb
import re, os, transaction
from app.model.meta import Session
from app.lib.helpers import is_api
import app.lib.util as util
from app.model.core.users import Users
from app.lib.geoip.geo import Geo
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

class BaseUI:

    def get_geoip(self):
        g = Geo()
        """ KB: [2011-03-28]: This works when proxied by nginx. """
        return g.by_ip(request.headers['X-Real-Ip'])


    def set_current_user(self):
        c.current_user = Users.load(session['user_id']) if 'user_id' in session else None


    def db_flush(self):
        Session.flush()


    def db_doom(self):
        transaction.doom()
        

    def db_delete(self, o):
        Session.delete(o)


    def flash(self, msg):
        self.request.session.flash(msg)


    def forbid_if(self, result):
        if result:
            raise HTTPForbidden()

class BaseController(BaseUI):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.enterprise_id = self.request.ctx.enterprise.enterprise_id


    def flash(self, msg):
        self.session.flash(msg)


    def cancel_session(self):
        self.session.invalidate()


    @property
    def offset(self):
        return int(self.request.GET.get('offset')) if 'offset' in self.request.GET else 0
