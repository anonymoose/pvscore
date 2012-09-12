import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.lib.validate import validate
import pvscore.lib.util as util
from pvscore.model.core.users import Users

log = logging.getLogger(__name__)

class LoginController(BaseController):

    @view_config(route_name="crm.login", renderer="/crm/login.mako")
    def index(self):
        return {}

    @view_config(route_name="crm.login.post", renderer="/crm/login.mako")
    @validate((('username', 'string'),
               ('username', 'required'),
               ('password', 'required')))
    def login(self):
        uid = self.request.POST.get('username')
        pwd = self.request.POST.get('password')

        if uid and pwd and Users.authenticate(uid, pwd):
            log.debug("%s logging in to %s" % (uid, self.request.url))
            self.session['user_id'] = uid
            self.session['customer_logged_in'] = False
            self.session['crm_logged_in'] = True
            user = Users.load(uid)
            # this ensures that they are logging in from the web and not crawling
            # to get in brute force.
            self.forbid_if(not user)

            # If they were on a page and got timed out, send them 
            # back where they were as a convenience.
            if util.get(self.request.POST, 'path'):
                if util.get(self.request.POST, 'vars'):
                    return HTTPFound('%s?%s' % (self.request.POST['path'], self.request.POST['vars']))
                else:
                    return HTTPFound(self.request.POST['path'])
            else:
                return HTTPFound('/crm/dashboard')
                # If the user is an external vendor, send them to the reports
                #if user.is_vendor_user():
                #    log.debug("%s redirecting to vendor user" % uid)
                #    return HTTPFound('/crm/report/list')
                #else:
                #    # if the user is required to accept terms, then send
                #    # them to the right place.  Terms handling is up to
                #    # the page.
                #    if user.enterprise and user.enterprise.terms_required and not user.enterprise.terms_accepted:
                #        return HTTPFound(user.enterprise.terms_link)
                #
                #    # If the user has been provisioned with a specific
                #    # place to log in, then send them there.
                #    if user.login_link:
                #        return HTTPFound(user.login_link)
                #    else:
                #        return HTTPFound('/crm/dashboard')
        else:
            log.debug("%s failed login in to %s" % (uid, self.request.url))
            self.flash('Invalid User or Password')
            return {}

    @view_config(route_name="crm.login.logout")
    def logout(self):
        self.cancel_session()
        return HTTPFound(util.get(self.request.GET, 'redir', '/'))

#    def customer_login(self):
#        if 'site_id' in session:
#            site = Site.load(session['site_id'])
#        else:
#            site = Site.find_by_host(request.host)
#            session['site_id'] = site.site_id
#
#        uid = request.POST.get('username')
#        pwd = request.POST.get('password')
#
#        if uid and pwd and Customer.authenticate(uid, pwd, site.company):
#            session['username'] = uid
#            cust = Customer.find_by_company(uid, site.company)
#            """ KB: [2010-10-07]: this is also used to determine on the
#            CRM side if this is from a portal session or if it is from the crm side
#            """
#            session['customer_id'] = cust.customer_id
#            session['customer_logged_in'] = True
#            session['crm_logged_in'] = False
#            session.save()
#            if 'redir' in request.POST:
#                redirect(request.POST.get('redir'))
#            else:
#                redirect(url(config['app_conf']['pvs.portal.initial_route']))
#        else:
#            flash('Invalid User or Password')
#            redirect(request.referrer)
#
#    @validate((('username', 'string'),
#               ('username', 'required')))
#    def customer_forgot_password(self):
#        """ KB: [2011-03-13]: Try to be at least a little sneaky.  Don't give any hints as to valid user accounts, etc.
#        If we don't find that email address then just redir back to /.
#        """
#        uid = request.POST.get('username')
#        if not uid: redirect('/')
#
#        cust = Customer.find_by_company(uid, site.company)
#        if not cust: redirect('/')
#
#        # reset the customer's password to something random.
#        cust.password = '%s%s%s' % (chr(random.randint(65,90)),
#                                    chr(random.randint(97, 122)),
#                                    str(random.randint(100000, 999999)))
#
#        cust.save()
#        cust.commit()
#        cmpn = Campaign.load(session['campaign_id'])
#        cmpn.send_forgot_password_comm(cust)
#        flash('Your password has been sent to the email address you provided.')
#        if request.POST.get('redir'):
#            redirect(request.POST.get('redir'))
#        else:
#            redirect('/')
#
#    """ KB: [2011-06-28]:
#    http://ww.wealthmakers.com/crm/customer_login_to_link/fdf774eb58feefd35fc2abab7db194e8/http%3A%7C%7Cww.wealthmakers.com%7Cireport.html%3Firid%3D13235
#    """
#    def customer_login_to_link(self, key, link):
#        cust = Customer.find_by_key(key)
#        if cust:
#            session['customer_id'] = cust.customer_id
#            session['customer_logged_in'] = True
#            session['crm_logged_in'] = False
#            session.save()
#            redirect(link.replace('|', '/'))
#        else:
#            flash('Invalid User or Password')
#            redirect('/')
