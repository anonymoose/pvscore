import logging
import os, shutil
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.controllers.base import BaseController
from pvscore.model.crm.customer import Customer
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsCustomerLoggedIn
from pvscore.model.crm.listing import Listing, ListingMessage, ListingFavorite
from pvscore.model.core.status import Status
from pvscore.controllers.cms.site import SiteController
from pvscore.model.core.asset import Asset
from pvscore.model.cms.site import Site
from hashlib import md5
import pvscore.lib.util as util
from pvscore.lib.geoip.geo import Geo

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

class ListingPlugin(BaseController):

    def remove_listing(self, listing_id):
        cust = Customer.load(session['customer_id'])
        l = Listing.load(self.request.matchdict('listing_id'))
        self.forbid_if(not l or not cust or l.customer != cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())
        l.soft_delete()
        Status.add(cust, l, Status.find_event(l, 'CLOSED'), 'Listing Deleted: %s' % self.request.POST.get('title'))
        l.commit()
        return 'True'

    def toggle_favorite(self, listing_id):
        self.forbid_if(not 'customer_id' in session)
        cust = Customer.load(session['customer_id'])
        l = Listing.load(listing_id)
        self.forbid_if(not l or not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())
        lf = ListingFavorite.find_favorite(cust, l)
        if lf:
            lf.track_delete()
            lf.delete()
        else:
            lf.track_add()
            lf = ListingFavorite.create_new(cust, l)
        lf.commit()
        return 'True'

    def favorites(self):
        self.forbid_if(not 'customer_id' in session)
        cust = Customer.load(session['customer_id'])
        self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

        c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
        c.geo_ip = self._get_geoip()
        c.lat = c.geo_ip['latitude']
        c.lng = c.geo_ip['longitude']
        if 'HOME' == c.bullseye:
            c.lat = cust.default_latitude
            c.lng = cust.default_longitude

        c.listings = ListingFavorite.find_favorites_by_customer(cust)
        c.search = cust.get_attr('keywords')
        c.category = None
        c.is_favorites = True
        sc = SiteController()
        if self.request.GET.get('results_page'):
            return sc.show_page(self.request.POST.get('results_page'))
        else:
            return sc.show_page('results.html')

    def json(self, listing_id):
        cust = Customer.load(session['customer_id'])
        c.listing = Listing.load(listing_id)
        self.forbid_if(not c.listing or not cust or c.listing.customer != cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())
        return self.render('listing.json.mako')

    def _get_geoip(self):
        g = Geo()
        """ KB: [2011-03-28]: This works when proxied by nginx. """
        return g.by_ip(self.request.headers['X-Real-Ip'])

    def category_search(self, category_id, category=None):
        c.search = category.replace('-', ' ').capitalize()
        c.category = category
        cust = None
        if 'customer_id' in session:
            cust = Customer.load(session['customer_id'])
            self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

        c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
        c.geo_ip = self._get_geoip()
        c.lat = c.geo_ip['latitude']
        c.lng = c.geo_ip['longitude']
        if 'HOME' == c.bullseye and cust:
            c.lat = cust.default_latitude
            c.lng = cust.default_longitude

        c.listings = Listing.search('', category_id, c.lat, c.lng, int(self.request.GET.get('radius', '10')))

        sc = SiteController()
        if self.request.GET.get('results_page'):
            return sc.show_page(self.request.POST.get('results_page'))
        else:
            return sc.show_page('results.html')

    def search(self):
        c.search = self.request.GET.get('search')
        if not c.search or c.search == 'Keyword': redirect(self.request.referrer)
        c.category = self.request.GET.get('category')
        cust = None
        if 'customer_id' in session:
            cust = Customer.load(session['customer_id'])
            self.forbid_if(not cust or cust.campaign.company.enterprise_id != BasePlugin.get_enterprise_id())

        c.bullseye = self.request.cookies.get('bullseye', 'CURRENT')
        c.geo_ip = self._get_geoip()
        c.lat = c.geo_ip['latitude']
        c.lng = c.geo_ip['longitude']
        if 'HOME' == c.bullseye and cust:
            c.lat = cust.default_latitude
            c.lng = cust.default_longitude

        c.listings = Listing.search(c.search, c.category, c.lat, c.lng, int(self.request.GET.get('radius', '10')))

        sc = SiteController()
        if self.request.GET.get('results_page'):
            return sc.show_page(self.request.POST.get('results_page'))
        else:
            return sc.show_page('results.html')

    def add_picture(self):
        return self.render('listing.add_picture.mako')

    @authorize(IsCustomerLoggedIn())
    def save(self):
        return self._save()

    def _save(self, do_redir=True):
        self.forbid_if('redir' not in self.request.POST)
        redir = self.request.POST.get('redir')
        cust = Customer.load(session['customer_id'])
        self.forbid_if(not cust)

        l = Listing.load(self.request.POST.get('listing_id'))
        if not l:
            site = self._get_site()
            l = Listing()
            l.customer = cust
            l.company = site.company
            l.ip = util.self.request_ip()
            g = Geo()
            gip = g.by_ip(l.ip)
            if gip and gip['latitude'] and gip['longitude']:
                l.latitude = gip['latitude'] if 'latitude' in gip else None
                l.longitude = gip['longitude'] if 'longitude' in gip else None
                l.city = gip['city'] if 'city' in gip else None
                l.state = gip['region_name'] if 'region_name' in gip else None
                l.zip = gip['postal_code'] if 'postal_code' in gip else None
                l.country = gip['country_code'] if 'country_code' in gip else None
                l.dma = gip['dma_code'] if 'dma_code' in gip else None

        # this overrides the original lat/lng settings if they are coming from
        # the POST instead of the geo ip.
        l.bind(self.request.POST, True)
        l.save()
        Status.add(cust, l, Status.find_event(l, 'OPEN'), 'Listing Created: %s' % self.request.POST.get('title'))
        self.db_commit()

        for k in self.request.POST.keys():
            if k.startswith('asset_'):
                a = Asset.load(k[6:])
                a.fk_type = 'Listing'
                a.fk_id = l.listing_id
                a.save()
        self.db_commit()

        if do_redir:
            flash('Listing: "%s" saved' % l.title)
            redirect('%s?listing_id=%s&post=1' % (redir, l.listing_id))
        else:
            return l

    """ KB: [2011-06-24]: Called when user (or not) replies to a listing.
    Queue into pvs_listing_message so we can send it out in batches.
    """
    def initial_reply(self):
        self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
                       'email' not in self.request.POST or not self.request.POST.get('email') or
                       'subject' not in self.request.POST or not self.request.POST.get('subject') or
                       'redir' not in self.request.POST or not self.request.POST.get('redir'))
        listing_id = self.request.POST.get('listing_id')
        l = Listing.load(listing_id)
        self.forbid_if(not l)

        email = self.request.POST.get('email')
        redir = self.request.POST.get('redir')
        msg_count = ListingMessage.find_count_by_email_and_listing(email, l)
        if msg_count > 0:
            flash('You have already replied to this listing.')
            redirect('%s?listing_id=%s' % (redir, listing_id))

        geo_ip = self._get_geoip()
        lat = lng = None
        if geo_ip:
            lat = geo_ip['latitude']
            lng = geo_ip['longitude']

        msg = ListingMessage()
        msg.listing_id = listing_id
        msg.customer_id = l.customer_id
        msg.company_id = l.company_id
        msg.subject = util.nvl(self.request.POST.get('subject'))
        msg.message = util.nvl(self.request.POST.get('message'))
        msg.responder_email = email.lower()
        msg.to_email = l.customer.email.lower()
        msg.from_email = email.lower()
        msg.from_latitude = lat
        msg.from_longitude = lng
        msg.from_ip = util.self.request_ip()
        msg.save()
        msg.commit()
        flash('Message sent.')
        redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

    """ KB: [2011-06-28]: We don't need a subject or "email" because the customer is sending this out.
    Queue into pvs_listing_message so we can send it out in batches.
    """
    @authorize(IsCustomerLoggedIn())
    def customer_reply(self):
        self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
                       'reply_to_id' not in self.request.POST or not self.request.POST.get('reply_to_id') or
                       'ckey' not in self.request.POST or not self.request.POST.get('ckey') or
                       'redir' not in self.request.POST or not self.request.POST.get('redir'))
        listing_id = self.request.POST.get('listing_id')
        l = Listing.load(listing_id)
        self.forbid_if(not l)

        listing_message_reply_to = ListingMessage.load(self.request.POST.get('reply_to_id'))
        self.forbid_if(not listing_message_reply_to
                       or not ListingMessage.validate_customer(l,
                                                               listing_message_reply_to,
                                                               self.request.POST.get('ckey')))
        cust = Customer.load(session['customer_id'])
        redir = self.request.POST.get('redir')
        geo_ip = self._get_geoip()
        lat = lng = None
        if geo_ip:
            lat = geo_ip['latitude']
            lng = geo_ip['longitude']

        msg = ListingMessage()
        msg.listing_id = listing_id
        msg.customer_id = l.customer_id
        msg.company_id = l.company_id
        msg.subject = 'RE: %s' % util.nvl(self.request.POST.get('subject'))
        msg.message = util.nvl(self.request.POST.get('message'))
        msg.responder_email = listing_message_reply_to.responder_email.lower()
        msg.to_email = listing_message_reply_to.responder_email.lower()
        msg.from_email = cust.email.lower()
        msg.from_latitude = lat
        msg.from_longitude = lng
        msg.from_ip = util.self.request_ip()
        msg.save()
        msg.commit()
        flash('Message sent.')
        redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

    def responder_reply(self):
        self.forbid_if('listing_id' not in self.request.POST or not self.request.POST.get('listing_id') or
                       'reply_to_id' not in self.request.POST or not self.request.POST.get('reply_to_id') or
                       'rkey' not in self.request.POST or not self.request.POST.get('rkey') or
                       'redir' not in self.request.POST or not self.request.POST.get('redir'))
        listing_id = self.request.POST.get('listing_id')
        l = Listing.load(listing_id)
        self.forbid_if(not l)

        listing_message_reply_to = ListingMessage.load(self.request.POST.get('reply_to_id'))
        self.forbid_if(not listing_message_reply_to
                       or not ListingMessage.validate_responder(l,
                                                                listing_message_reply_to,
                                                                self.request.POST.get('rkey')))
        email = self.request.POST.get('email')
        redir = self.request.POST.get('redir')

        geo_ip = self._get_geoip()
        lat = lng = None
        if geo_ip:
            lat = geo_ip['latitude']
            lng = geo_ip['longitude']

        msg = ListingMessage()
        msg.listing_id = listing_id
        msg.customer_id = l.customer_id
        msg.company_id = l.company_id
        msg.subject = util.nvl(self.request.POST.get('subject'))
        msg.message = util.nvl(self.request.POST.get('message'))
        msg.responder_email = listing_message_reply_to.responder_email.lower()
        msg.to_email = l.customer.email.lower()
        msg.from_email = msg.responder_email
        msg.from_latitude = lat
        msg.from_longitude = lng
        msg.from_ip = util.self.request_ip()
        msg.save()
        msg.commit()
        flash('Message sent.')
        redirect('%s?listing_id=%s&listing_message_id=%s' % (self.request.POST.get('redir'), listing_id, msg.listing_message_id))

    #@authorize(IsCustomerLoggedIn())
    def upload_asset(self, listing_id):
        """ KB: [2011-03-23]: Take this file and hash its name up to put it in a sensible directory. """
        l = Listing.load(listing_id)
        self.forbid_if(not l)
        site = self._get_site()
        asset_data = self.request.POST['Filedata']
        filename = md5('%s%s' % (asset_data.filename, listing_id)).hexdigest()
        extension = os.path.splitext(asset_data.filename)[1]
        folder = '/images/%s/%s/%s' % (filename[0], filename[1], filename[2])
        util.mkdir_p('%s%s' % (site.site_full_directory, folder))
        fs_path = os.path.join('%s%s' % (site.site_full_directory, folder), filename+extension)
        permanent_file = open(fs_path, 'wb')
        shutil.copyfileobj(asset_data.file, permanent_file)
        asset_data.file.close()
        permanent_file.close()

        # at this point everything is saved to disk. Create an asset object in
        # the DB to remember it.
        if os.path.exists(fs_path):
            a = Asset()
            a.fs_path = fs_path
            a.web_path = '%s/%s/%s/%s/%s' % (site.site_web_directory('images'),
                                             filename[0], filename[1], filename[2], filename+extension)
            a.fk_type = 'Listing'
            a.fk_id = listing_id
            a.name = filename+extension
            a.save()
            Status.add(l.customer, l, Status.find_event(l, 'ASSET_UPLOAD'),
                       '%s = %s' % (asset_data.filename, filename))

            a.commit()
            return str(a.id)

class ListingUtil:
    @staticmethod
    def _get_site():
        site = None
        if not 'site_id' in session:
            site = Site.find_by_host(self.request.host)
            session['site_id'] = site.site_id
        else:
            site = Site.load(session['site_id'])
        if not site:
            abort(500)
        return site

    @staticmethod
    def get_categories():
        """ KB: [2011-03-28]: The categories have to be defined in the site.config file.  They are stored in the DB
        as strings for now.
        """
        site = ListingUtil._get_site()
        cfg = site.get_config()
        categories = cfg.get('CATEGORIES', 'categories')
        return [cs.split('|') for cs in categories.split(',')]

