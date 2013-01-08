#pylint: disable-msg=E1101
from pvscore.model.meta import Session
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
import logging
from pvscore.lib.plugin import plugin_registry

log = logging.getLogger(__name__)

class BaseUI(object):

    def __init__(self):
        pass

    def db_flush(self):
        Session.flush()


    # def db_doom(self):
    #     transaction.doom()


    # def db_delete(self, obj):
    #     Session.delete(obj)


class BaseController(BaseUI):
    def __init__(self, request):
        if request:
            self.request = request
            self.session = request.session
            self.user = self.request.ctx.user
            self.plugin_registry = plugin_registry

            self.enterprise_id = self.request.ctx.enterprise.enterprise_id
            # KB: [2013-01-07]: override the enterprise ID if this user has one.
            # Allows us secure multi hosting.
            if self.request.ctx.user and self.request.ctx.user.enterprise_id:
                self.enterprise_id = self.request.ctx.user.enterprise_id
                self.request.session['enterprise_id'] = self.request.ctx.user.enterprise_id

        super(BaseController, self).__init__()


    # def get_geoip(self):
    #     geo = Geo()
    #     return geo.by_ip(self.request.headers['X-Real-Ip'])


    def flash(self, msg):
        self.session.flash(msg)


    def forbid_if(self, result, msg=None):
        if result:
            if msg:
                log.info(msg)
            raise HTTPForbidden()


    def redir_if(self, result, goto='/', msg=None):
        if result: #pragma: no cover
            if msg:
                log.info(msg)
            raise HTTPFound(goto)


    def cancel_session(self):
        self.session.invalidate()


    @property
    def offset(self):
        return int(self.request.GET.get('offset')) if 'offset' in self.request.GET else 0


    def find_redirect(self, params=""):
        if self.request.POST.get('redir'):
            return HTTPFound('%s%s' % (self.request.POST.get('redir'), params))
        return HTTPFound('%s%s' % (self.request.referrer, params)) if self.request.referrer else HTTPFound('/%s' % params)


    def raise_redirect(self, goto=None, params=""):
        if goto:
            raise HTTPFound(goto)  #pragma: no cover
        else:
            if self.request.POST.get('redir'):
                raise HTTPFound('%s%s' % (self.request.POST.get('redir'), params))
            raise HTTPFound('%s%s' % (self.request.referrer, params)) if self.request.referrer else HTTPFound('/%s' % params)
