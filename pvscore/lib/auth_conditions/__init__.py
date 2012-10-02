#pylint: disable-msg=W0613,R0903,W0511
import urllib
from pvscore.lib.helpers import is_api
from pyramid.httpexceptions import HTTPFound

class NotValidAuth(Exception):
    pass

# class AllMet(object):

#     message = u'All of these conditions have to be met: %s.'

#     def __init__(self, *args):
#         self.conditions = args


#     def check(self, controller):
#         condition_messages = []
#         valid = True
#         for condition in self.conditions:
#             try:
#                 condition.check(controller)
#             except NotValidAuth as exc:
#                 valid = False
#                 condition_messages.append(unicode(exc))
#         if valid:
#             return True
#         raise NotValidAuth(self.message % ', '.join(condition_messages))

# class OneMet(object):

#     message = u'At least one of these conditions have to be met: %s.'

#     def __init__(self, *args):
#         self.conditions = args


#     def check(self, controller):
#         condition_messages = []
#         for condition in self.conditions:
#             try:
#                 condition.check(controller)
#                 return True
#             except NotValidAuth as exc:
#                 condition_messages.append(unicode(exc))
#         raise NotValidAuth(self.message % ', '.join(condition_messages))


#     def handler(self, exc, controller):        #pylint: disable-msg=W0613
#         """ TODO: KB: [2010-08-12]: Fix this to be dynamic by app """
#         raise HTTPFound('/crm/login?path=%s&vars=%s' % (controller.request.path, urllib.quote(controller.request.query_string)))


# class Not(object):

#     message = u'All of these conditions have to be not met: %s.'

#     def __init__(self, *args):
#         self.conditions = args


#     def check(self, controller):
#         condition_messages = []
#         valid = True
#         for condition in self.conditions:
#             try:
#                 condition.check(controller)
#                 valid = False
#             except NotValidAuth as exc:
#                 condition_messages.append(unicode(exc))
#         if valid:
#             return True
#         raise NotValidAuth(self.message % ', '.join(condition_messages))


class IsLoggedIn(object):

    message = u'User must be logged'


    def check(self, controller):
        """ KB: [2010-09-23]: If it's an API call, then @api_method() (core.lib.decorators.api) will handle security. """
        if 'crm_logged_in' in controller.session and controller.session['crm_logged_in'] == True and ('user_id' in controller.session or is_api(controller.request)):
            return True
        raise NotValidAuth(self.message)


    def handler(self, exc, controller):        #pylint: disable-msg=W0613
        """ TODO: KB: [2010-08-12]: Fix this to be dynamic by app """
        raise HTTPFound('/crm/login?path=%s&vars=%s' % (controller.request.path, urllib.quote(controller.request.query_string)))


class IsCustomerLoggedIn(object):
    message = u'Customer must be logged'

    def check(self, controller):
        if 'customer_id' in controller.session and controller.session['customer_id'] is not None and controller.request.ctx.customer is not None:
            return True
        raise NotValidAuth(self.message)

    def handler(self, exc, controller):        #pylint: disable-msg=W0613
        """ TODO: KB: [2010-08-12]: Fix this to be dynamic by app """
        raise HTTPFound('/?path=%s&vars=%s' % (controller.request.path, urllib.quote(controller.request.query_string)))


# class IsInternalReferrer(object):
#     message = u'Referrer must be from internal source: %s invalid'

#     def check(self, controller):
#         if controller.request.host is not None and controller.request.referrer is not None and '//'+controller.request.host in controller.request.referrer:
#             return True
#         raise NotValidAuth(self.message % controller.request.referrer)


#     def handler(self, exc, controller):        #pylint: disable-msg=W0613
#         raise HTTPFound('/')

