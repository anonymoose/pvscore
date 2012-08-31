#pylint: disable-msg=E1101
import transaction
from app.model.meta import Session
from app.lib.geoip.geo import Geo
from pyramid.httpexceptions import HTTPForbidden

class BaseUI(object):

    def __init__(self):
        pass

    def db_flush(self):
        Session.flush()


    def db_doom(self):
        transaction.doom()
        

    def db_delete(self, obj):
        Session.delete(obj)


class BaseController(BaseUI):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.enterprise_id = self.request.ctx.enterprise.enterprise_id
        super(BaseController, self).__init__()


    def get_geoip(self):
        geo = Geo()
        return geo.by_ip(self.request.headers['X-Real-Ip'])


    def flash(self, msg):
        self.session.flash(msg)


    def forbid_if(self, result):
        if result:
            raise HTTPForbidden()


    def cancel_session(self):
        self.session.invalidate()


    @property
    def offset(self):
        return int(self.request.GET.get('offset')) if 'offset' in self.request.GET else 0
