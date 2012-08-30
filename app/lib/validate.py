import pdb, logging
from decorator import decorator
import app.lib.util as util
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

log = logging.getLogger(__name__)

def _die(request, msg, redir_to): 
    log.debug("*** VALIDATION ERROR: " + msg)
    #util.test_set_var(msg)

    if redir_to:
        msgkey = '?msg=' if -1 == redir_to.find('?') else 'msg='
        raise HTTPFound(redir_to + msgkey + msg)
    else:
        raise HTTPForbidden()


""" KB: [2011-08-19]: 
    @validate((('fname', 'required'), 
               ('fname', 'string'),
               ('lname', 'required'), 
               ('lname', 'string'),
               ('password', 'required'), 
               ('confirm', 'required'),
               ('password', 'equals', 'confirm')))
    def save(self):
        ...
"""
def validate(rules=(), redir_to=None):
    def wrap(func, self, *args, **kwargs):
        for a in rules:
            ok = True
            key = a[0]
            rule = a[1]
            oval = self.request.GET.get(key)
            if not oval:
                oval = self.request.POST.get(key)
            if not oval:
                oval = self.request.matchdict.get(key)
            val = str(oval)

            if 'required' == rule and util.is_empty(val):
                _die(self.request, '%s is required' % key, redir_to)

            if 'string' == rule and oval and not util.is_string(val):
                _die(self.request, '%s must not be a number' % key, redir_to)
            
            if 'number' == rule and oval and not util.is_number(val):
                _die(self.request, '%s must be a number' % key, redir_to)

            if 'float' == rule and oval and not util.is_float(val):
                _die(self.request, '%s must be a float' % key, redir_to)

            if 'int' == rule and oval and not util.is_int(val):
                _die(self.request, '%s must be a integer' % key, redir_to)

            if 'equals' == rule and oval and len(a) == 3:
                val2 = self.request.GET.get(a[2], self.request.POST.get(a[2], None))
                if util.is_empty(val) != util.is_empty(val2) or str(val) != str(val2):
                    _die(self.request, '%s must equal %s' % (val2, val), redir_to)

        return func(self, *args, **kwargs)
    return decorator(wrap)


def validate_session(rules=(), redir_to=None):
    def wrap(func, self, *args, **kwargs):
        for a in rules:
            ok = True
            key = a[0]
            rule = a[1]
            val = self.request.session[key] if key in self.request.session else None

            if 'required' == rule and val and util.is_empty(val):
                _die(self.request, '%s is required' % key, redir_to)

            if 'string' == rule and val and not util.is_string(val):
                _die(self.request, '%s must not be a number' % key, redir_to)
            
            if 'number' == rule and val and not util.is_number(val):
                _die(self.request, '%s must be a number %s %s' % (key, val, _is_number(val)), redir_to)

            if 'float' == rule and val and not util.is_float(val):
                _die(self.request, '%s must be a float' % key, redir_to)

            if 'int' == rule and val and not util.is_int(val):
                _die(self.request, '%s must be a integer' % key, redir_to)

        return func(self, *args, **kwargs)
    return decorator(wrap)
