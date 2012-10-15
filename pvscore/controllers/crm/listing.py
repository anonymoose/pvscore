import logging
import os, shutil
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsCustomerLoggedIn
from pvscore.model.crm.listing import Listing
from pvscore.model.core.status import Status
from pvscore.model.core.asset import Asset
from hashlib import md5

import pvscore.lib.util as util

log = logging.getLogger(__name__)

# This status has to be there before anything gets can work.
# insert into core_status_event
# (event_type, short_name, display_name, claim, finalize, is_system,
# milestone_complete, note_req, dashboard, reason_req, change_status, touch)
# values
# ('Listing', 'ASSET_UPLOAD', 'ASSET_UPLOAD', false, false, true,
# true, false, false, false, true, false);
# insert into core_status_event
# (event_type, short_name, display_name, claim, finalize, is_system,
# milestone_complete, note_req, dashboard, reason_req, change_status, touch)
# values
# ('Listing', 'OPEN', 'OPEN', false, false, true,
# true, false, false, false, true, false);
# insert into core_status_event
# (event_type, short_name, display_name, claim, finalize, is_system,
# milestone_complete, note_req, dashboard, reason_req, change_status, touch)
# values
# ('Listing', 'CLOSED', 'CLOSED', false, false, true,
# true, false, false, false, true, false);
# insert into core_status_event
# (event_type, short_name, display_name, claim, finalize, is_system,
# milestone_complete, note_req, dashboard, reason_req, change_status, touch)
# values
# ('ListingMessage', 'SEND_OK', 'SEND_OK', false, false, true,
# false, false, false, false, false, false);
# insert into core_status_event
# (event_type, short_name, display_name, claim, finalize, is_system,
# milestone_complete, note_req, dashboard, reason_req, change_status, touch)
# values
# ('ListingMessage', 'SEND_FAIL', 'SEND_FAIL', false, false, true,
# false, false, false, false, false, false);

class ListingController(BaseController):

    @view_config(route_name='crm.listing.remove', renderer="string")
    @authorize(IsCustomerLoggedIn())
    def remove(self):
        lis = Listing.load(self.request.matchdict.get('listing_id'))
        cust = self.request.ctx.customer
        self.forbid_if(not lis or not cust or lis.customer.customer_id != cust.customer_id or cust.campaign.company.enterprise_id != self.enterprise_id)
        lis.soft_delete()
        Status.add(cust, lis, Status.find_event(self.enterprise_id, lis, 'CLOSED'),
                   'Listing Deleted: %s' % self.request.POST.get('title'))
        return 'True'


    @view_config(route_name='crm.listing.json.get', renderer="/crm/listing.json.mako")
    @view_config(route_name='crm.listing.json', renderer="/crm/listing.json.mako")
    @authorize(IsCustomerLoggedIn())
    def json(self):
        listing_id = self.request.matchdict.get('listing_id')
        if not listing_id:
            listing_id = self.request.GET.get('listing_id')
        self.forbid_if(not listing_id)
        cust = self.request.ctx.customer
        listing = Listing.load(listing_id)
        self.forbid_if(not listing or not cust or listing.customer.customer_id != cust.customer_id or cust.campaign.company.enterprise_id != self.enterprise_id)
        return {
            'listing' : listing
            }

    
    @view_config(route_name='crm.listing.show_add_picture', renderer="/crm/listing.add_picture.mako")
    @authorize(IsCustomerLoggedIn())
    def add_picture(self):
        return {}


    @view_config(route_name='crm.listing.save')
    @authorize(IsCustomerLoggedIn())
    def save(self):
        self.forbid_if('redir' not in self.request.POST)
        redir = self.request.POST.get('redir')
        cust = self.request.ctx.customer
        lis = Listing.load(self.request.POST.get('listing_id'))
        if not lis:
            lis = Listing()
            lis.customer = cust
            lis.company = self.request.ctx.campaign.company
            lis.site = self.request.ctx.site
            # l.ip = util.self.request_ip()
            # g = Geo()
            # gip = g.by_ip(l.ip)
            # if gip and gip['latitude'] and gip['longitude']:
            #     l.latitude = gip['latitude'] if 'latitude' in gip else None
            #     l.longitude = gip['longitude'] if 'longitude' in gip else None
            #     l.city = gip['city'] if 'city' in gip else None
            #     l.state = gip['region_name'] if 'region_name' in gip else None
            #     l.zip = gip['postal_code'] if 'postal_code' in gip else None
            #     l.country = gip['country_code'] if 'country_code' in gip else None
            #     l.dma = gip['dma_code'] if 'dma_code' in gip else None
        # this overrides the original lat/lng settings if they are coming from
        # the POST instead of the geo ip.
        lis.bind(self.request.POST, True)
        lis.save()
        self.db_flush()

        # for key in self.request.POST.keys():
        #     if key.startswith('asset_'):
        #         ass = Asset.load(key[6:])
        #         ass.fk_type = 'Listing'
        #         ass.fk_id = lis.listing_id
        #         ass.save()

        Status.add(cust, lis, Status.find_event(self.enterprise_id, lis, 'OPEN'),
                   'Listing Created: %s' % self.request.POST.get('title'))
        self.flash('Listing: "%s" saved' % lis.title)
        return HTTPFound('%s?listing_id=%s&post=1' % (redir, lis.listing_id))


    @view_config(route_name='crm.listing.upload', renderer='string')
    # KB: [2012-09-26]: we can't use IsCustomerLoggedIn() here because flash doesn't
    # respect sessions.  the .../{hash} parameter ensures that uploads
    # are secure.
    def upload_asset(self):
        """ KB: [2011-03-23]: Take this file and hash its name up to put it in a sensible directory. """
        listing_id = self.request.matchdict.get('listing_id')
        listing_hash = self.request.matchdict.get('hash')
        lis = Listing.load(listing_id)
        self.forbid_if(not lis or lis.hash != listing_hash)
        site = self.request.ctx.site
        asset_data = self.request.POST['Filedata']
        filename = md5('%s%s' % (asset_data.filename, listing_id)).hexdigest()
        extension = os.path.splitext(asset_data.filename)[1]
        folder = 'images/%s/%s/%s' % (filename[0], filename[1], filename[2])
        util.mkdir_p('%s/%s' % (site.site_full_directory, folder))
        fs_path = os.path.join(folder, filename+extension)
        fs_path_real = os.path.join('%s/%s' % (site.site_full_directory, folder), filename+extension)
        permanent_file = open(fs_path_real, 'wb')
        shutil.copyfileobj(asset_data.file, permanent_file)
        asset_data.file.close()
        permanent_file.close()

        # at this point everything is saved to disk. Create an asset object in
        # the DB to remember it.
        if os.path.exists(fs_path_real):
            ass = Asset()
            ass.fs_path = fs_path
            ass.web_path = '%s/%s/%s/%s/%s' % (site.site_web_directory('images'),
                                             filename[0], filename[1], filename[2], filename+extension)
            ass.fk_type = 'Listing'
            ass.fk_id = listing_id
            ass.name = filename+extension
            ass.save()
            Status.add(lis.customer, lis, Status.find_event(self.enterprise_id, lis, 'ASSET_UPLOAD'),
                       '%s = %s' % (asset_data.filename, filename))
            return str(ass.id)
        


    # def category_search(self, category_id, category=None):
    #     c.search = category.replace('-', ' ').capitalize()
    #     c.category = category
    #     cust = None
    #     if 'customer_id' in session:
    #         cust = Customer.load(session['customer_id'])
    #         self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

    #     c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
    #     c.geo_ip = self._get_geoip()
    #     c.lat = c.geo_ip['latitude']
    #     c.lng = c.geo_ip['longitude']
    #     if 'HOME' == c.bullseye and cust:
    #         c.lat = cust.default_latitude
    #         c.lng = cust.default_longitude

    #     c.listings = Listing.search('', category_id, c.lat, c.lng, int(self.request.GET.get('radius', '10')))

    #     sc = SiteController()
    #     if self.request.GET.get('results_page'):
    #         return sc.show_page(self.request.POST.get('results_page'))
    #     else:
    #         return sc.show_page('results.html')

    # def toggle_favorite(self, listing_id):
    #     self.forbid_if(not 'customer_id' in session)
    #     cust = Customer.load(session['customer_id'])
    #     l = Listing.load(listing_id)
    #     self.forbid_if(not l or not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())
    #     lf = ListingFavorite.find_favorite(cust, l)
    #     if lf:
    #         lf.track_delete()
    #         lf.delete()
    #     else:
    #         lf.track_add()
    #         lf = ListingFavorite.create_new(cust, l)
    #     lf.commit()
    #     return 'True'


    # def favorites(self):
    #     self.forbid_if(not 'customer_id' in session)
    #     cust = Customer.load(session['customer_id'])
    #     self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

    #     c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
    #     c.geo_ip = self._get_geoip()
    #     c.lat = c.geo_ip['latitude']
    #     c.lng = c.geo_ip['longitude']
    #     if 'HOME' == c.bullseye:
    #         c.lat = cust.default_latitude
    #         c.lng = cust.default_longitude

    #     c.listings = ListingFavorite.find_favorites_by_customer(cust)
    #     c.search = cust.get_attr('keywords')
    #     c.category = None
    #     c.is_favorites = True
    #     sc = SiteController()
    #     if self.request.GET.get('results_page'):
    #         return sc.show_page(self.request.POST.get('results_page'))
    #     else:
    #         return sc.show_page('results.html')

    # def search(self):
    #     c.search = self.request.GET.get('search')
    #     if not c.search or c.search == 'Keyword': redirect(self.request.referrer)
    #     c.category = self.request.GET.get('category')
    #     cust = None
    #     if 'customer_id' in session:
    #         cust = Customer.load(session['customer_id'])
    #         self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

    #     c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
    #     c.geo_ip = self._get_geoip()
    #     c.lat = c.geo_ip['latitude']
    #     c.lng = c.geo_ip['longitude']
    #     if 'HOME' == c.bullseye and cust:
    #         c.lat = cust.default_latitude
    #         c.lng = cust.default_longitude

    #     c.listings = Listing.search(c.search, c.category, c.lat, c.lng, int(self.request.GET.get('radius', '10')))

    #     sc = SiteController()
    #     if self.request.GET.get('results_page'):
    #         return sc.show_page(self.request.POST.get('results_page'))
    #     else:
    #         return sc.show_page('results.html')

    # """ KB: [2011-06-24]: Called when user (or not) replies to a listing.
    # Queue into pvs_listing_message so we can send it out in batches.
    # """
    # def initial_reply(self):
    #     self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
    #                    'email' not in self.request.POST or not self.request.POST.get('email') or
    #                    'subject' not in self.request.POST or not self.request.POST.get('subject') or
    #                    'redir' not in self.request.POST or not self.request.POST.get('redir'))
    #     listing_id = self.request.POST.get('listing_id')
    #     l = Listing.load(listing_id)
    #     self.forbid_if(not l)

    #     email = self.request.POST.get('email')
    #     redir = self.request.POST.get('redir')
    #     msg_count = ListingMessage.find_count_by_email_and_listing(email, l)
    #     if msg_count > 0:
    #         flash('You have already replied to this listing.')
    #         redirect('%s?listing_id=%s' % (redir, listing_id))

    #     geo_ip = self._get_geoip()
    #     lat = lng = None
    #     if geo_ip:
    #         lat = geo_ip['latitude']
    #         lng = geo_ip['longitude']

    #     msg = ListingMessage()
    #     msg.listing_id = listing_id
    #     msg.customer_id = l.customer_id
    #     msg.company_id = l.company_id
    #     msg.subject = util.nvl(self.request.POST.get('subject'))
    #     msg.message = util.nvl(self.request.POST.get('message'))
    #     msg.responder_email = email.lower()
    #     msg.to_email = l.customer.email.lower()
    #     msg.from_email = email.lower()
    #     msg.from_latitude = lat
    #     msg.from_longitude = lng
    #     msg.from_ip = util.self.request_ip()
    #     msg.save()
    #     msg.commit()
    #     flash('Message sent.')
    #     redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

    # """ KB: [2011-06-28]: We don't need a subject or "email" because the customer is sending this out.
    # Queue into pvs_listing_message so we can send it out in batches.
    # """
    # @authorize(IsCustomerLoggedIn())
    # def customer_reply(self):
    #     self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
    #                    'reply_to_id' not in self.request.POST or not self.request.POST.get('reply_to_id') or
    #                    'ckey' not in self.request.POST or not self.request.POST.get('ckey') or
    #                    'redir' not in self.request.POST or not self.request.POST.get('redir'))
    #     listing_id = self.request.POST.get('listing_id')
    #     l = Listing.load(listing_id)
    #     self.forbid_if(not l)

    #     listing_message_reply_to = ListingMessage.load(self.request.POST.get('reply_to_id'))
    #     self.forbid_if(not listing_message_reply_to
    #                    or not ListingMessage.validate_customer(l,
    #                                                            listing_message_reply_to,
    #                                                            self.request.POST.get('ckey')))
    #     cust = Customer.load(session['customer_id'])
    #     redir = self.request.POST.get('redir')
    #     geo_ip = self._get_geoip()
    #     lat = lng = None
    #     if geo_ip:
    #         lat = geo_ip['latitude']
    #         lng = geo_ip['longitude']

    #     msg = ListingMessage()
    #     msg.listing_id = listing_id
    #     msg.customer_id = l.customer_id
    #     msg.company_id = l.company_id
    #     msg.subject = 'RE: %s' % util.nvl(self.request.POST.get('subject'))
    #     msg.message = util.nvl(self.request.POST.get('message'))
    #     msg.responder_email = listing_message_reply_to.responder_email.lower()
    #     msg.to_email = listing_message_reply_to.responder_email.lower()
    #     msg.from_email = cust.email.lower()
    #     msg.from_latitude = lat
    #     msg.from_longitude = lng
    #     msg.from_ip = util.self.request_ip()
    #     msg.save()
    #     msg.commit()
    #     flash('Message sent.')
    #     redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

    # def responder_reply(self):
    #     self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
    #                    'reply_to_id' not in self.request.POST or not self.request.POST.get('reply_to_id') or
    #                    'rkey' not in self.request.POST or not self.request.POST.get('rkey') or
    #                    'redir' not in self.request.POST or not self.request.POST.get('redir'))
    #     listing_id = self.request.POST.get('listing_id')
    #     l = Listing.load(listing_id)
    #     self.forbid_if(not l)

    #     listing_message_reply_to = ListingMessage.load(self.request.POST.get('reply_to_id'))
    #     self.forbid_if(not listing_message_reply_to
    #                    or not ListingMessage.validate_responder(l,
    #                                                             listing_message_reply_to,
    #                                                             self.request.POST.get('rkey')))
    #     email = self.request.POST.get('email')
    #     redir = self.request.POST.get('redir')

    #     geo_ip = self._get_geoip()
    #     lat = lng = None
    #     if geo_ip:
    #         lat = geo_ip['latitude']
    #         lng = geo_ip['longitude']

    #     msg = ListingMessage()
    #     msg.listing_id = listing_id
    #     msg.customer_id = l.customer_id
    #     msg.company_id = l.company_id
    #     msg.subject = util.nvl(self.request.POST.get('subject'))
    #     msg.message = util.nvl(self.request.POST.get('message'))
    #     msg.responder_email = listing_message_reply_to.responder_email.lower()
    #     msg.to_email = l.customer.email.lower()
    #     msg.from_email = msg.responder_email
    #     msg.from_latitude = lat
    #     msg.from_longitude = lng
    #     msg.from_ip = util.self.request_ip()
    #     msg.save()
    #     msg.commit()
    #     flash('Message sent.')
    #     redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

