from pvscore.tests import TestController, secure
from pvscore.model.cms.site import Site
from pyramid.httpexceptions import HTTPForbidden
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.company import Enterprise
import logging
import uuid

log = logging.getLogger(__name__)

# T pvscore.tests.controllers.test_cms_site

class TestCmsSite(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/cms/site/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Site')
        f = R.forms['frm_site']
        self.assertEqual(f['domain'].value, '')


    @secure
    def test_create_new(self):
        site_id = self._create_new()
        self._delete_new(site_id)


    @secure
    def test_list_with_new(self):
        site_id = self._create_new()
        R = self.get('/cms/site/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('testsite.com')
        self._delete_new(site_id)


    @secure
    def test_save_existing(self):
        site_id = self._create_new()
        R = self.get('/cms/site/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('testsite.com')

        R = self.get('/cms/site/edit/%s' % site_id)
        R.mustcontain('Edit Site')
        f = R.forms['frm_site']
        self.assertEqual(f['site_id'].value, site_id)
        self.assertEqual(f['seo_title'].value, 'Test Site')

        f.set('seo_title', 'Test Site New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_site']
        R.mustcontain('Edit Site')

        self.assertEqual(f['seo_title'].value, 'Test Site New')
        self._delete_new(site_id)


    def _create_new(self):
        R = self.get('/cms/site/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Site')
        f = R.forms['frm_site']
        self.assertEqual(f['site_id'].value, '')
        f.set('domain', 'testsite.com')
        f.set('domain_alias0', 'testsite0.com')
        f.set('seo_title', 'Test Site')
        f.set('robots_txt', """User-agent: *
Disallow: /cms/cart/add/*""")

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_site']
        R.mustcontain('Edit Site')
        site_id = f['site_id'].value
        self.assertNotEqual(f['site_id'].value, '')
        site = Site.load(site_id)
        log.debug(site)
        return site_id


    def _delete_new(self, site_id):
        site = Site.load(site_id)
        self.assertNotEqual(site, None)
        site.delete()
        self.commit()


    def test_site_alternate_campaign(self):
        ent = Enterprise.find_all()[0]
        cmpns = Campaign.find_all(ent.enterprise_id)
        other_campaign = cmpns[1]
        R = self.get('/?__cid=%s' % other_campaign.campaign_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain("campaign_id = %s" % other_campaign.campaign_id)

    def test_site_not_hosted(self):
        headers = {'Host': 'www.bogus.com'}
        R = self.app.get('/', params=None, headers=self._get_headers(headers))
        self.assertEqual(R.headers['Location'], 'http://www.google.com')


    def test_dynamic_root(self):
        R = self.get('/')
        R.mustcontain('this is the index')


    def test_dynamic_file(self):
        R = self.get('/dynamic1')
        R.mustcontain('this is dynamic1.mako domain = %s' % self.site.domain)


    def test_dynamic_1deep(self):
        R = self.get('/subdir1-in_subdir_1/220/123')
        R.mustcontain('this is in subdir1 param0 = 220 param1 = 123 param2 = None')
        

    def test_dynamic_2deep(self):
        R = self.get('/subdir1-subdir2-in_subdir_2/220/123')
        R.mustcontain('this is in subdir2 param0 = 220 param1 = 123 param2 = None')
        

    def test_dynamic_not_found(self):
        excepted = False
        try:
            self.get('/subdir1-notthere-in_subdir_2/220/123')
        except Exception as notfound:
            log.info(notfound)
            excepted = True
        self.assertEqual(excepted, True)
        

    def test_customer_found(self):
        cust = self.get_customer()
        R = self.get('/customer?customer_id=%s' % cust.customer_id )
        R.mustcontain('fname = %s lname = %s id = %s' % (cust.fname, cust.lname, cust.customer_id))


    def test_customer_found_post(self):
        cust = self.get_customer()
        R = self.post('/customer',
                      {'customer_id' : cust.customer_id})
        R.mustcontain('fname = %s lname = %s id = %s' % (cust.fname, cust.lname, cust.customer_id))


    def test_customer_not_found(self):
        try:
            self.get('/customer?customer_id=%s' % uuid.uuid4())
        except HTTPForbidden as forbid:
            log.debug(forbid)
            return
        # should never get here.
        self.assertEqual(True, False)



        
