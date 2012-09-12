#pylint: disable-msg=W0613
import time
import logging
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.company import Enterprise
from pvscore.model.cms.site import Site
from pvscore.model.core.users import Users
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
import pvscore.lib.util as util

log = logging.getLogger(__name__)

def timing_tween_factory(handler, registry):
    # if timing support is enabled, return a wrapper
    def timing_tween(request):
        start = time.time()
        try:
            response = handler(request)
        finally:
            end = time.time()
            log.debug('TIMING: %s %s' % (request.path, round(end - start, 6)))
        return response
    return timing_tween
    # if timing support is not enabled, return the original
    # handler
    #return handler


def request_context_tween_factory(handler, registry):
    """ KB: [2012-08-10]: Figure out what site we are on. Make sure that the
    enterprise we are on matches the site we are on.
    End result is that there is a site, campaign, and enterprise in
    request.ctx, and site_id, campaign_id, and enterprise_id in session
    Make sure we are not doing this for static content.
    """

    def request_context_tween(request):
        if request.url.find('/static/') == -1:
            log.debug("URL: %s" % request.url)
            if not hasattr(request, 'ctx'):
                request.ctx = util.DataObj({})
    
            if not request.ctx.site:
                if not _remember_site(request):
                    return HTTPFound("http://www.google.com")
                
            if not request.ctx.campaign:
                _remember_campaign(request)
    
            if not request.ctx.enterprise:
                _remember_enterprise(request)
                
            if not request.ctx.user:
                _remember_user(request)

            request.tmpl_context.site = request.ctx.site
            request.tmpl_context.enterprise = request.ctx.enterprise
            request.tmpl_context.campaign = request.ctx.campaign
            request.tmpl_context.user = request.ctx.user
        return handler(request)
    return request_context_tween


def _remember_site(request):
    if 'site_id' in request.session:
        request.ctx.site = Site.load(request.session['site_id'])
    else:
        if '__sid' in request.params:
            request.ctx.site = Site.find_by_host(request.params['__sid'])
        else:
            request.ctx.site = Site.find_by_host(request.host)
        if not request.ctx.site:
            return False
        request.session['site_id'] = request.ctx.site.site_id
    return True


def _remember_campaign(request):
    if 'campaign_id' in request.session:
        request.ctx.campaign = Campaign.load(request.session['campaign_id'])
    else:
        if '__cid' in request.params:
            request.ctx.campaign = Campaign.load(request.params['campaign_id'])
        else:
            request.ctx.campaign = Campaign.load(request.ctx.site.company.default_campaign_id)
        request.session['campaign_id'] = request.ctx.campaign.campaign_id


def _remember_enterprise(request):
    if 'enterprise_id' in request.session:
        request.ctx.enterprise = Enterprise.load(request.session['enterprise_id'])
    else:
        request.ctx.enterprise = request.ctx.site.company.enterprise
        request.session['enterprise_id'] = request.ctx.enterprise.enterprise_id


def _remember_user(request):
    if 'user_id' in request.session:
        request.ctx.user = Users.load(request.session['user_id'])


        
