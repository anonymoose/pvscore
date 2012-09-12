from pvscore.tests import TestController, secure
from pvscore.model.cms.site import Site

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
        return site_id


    def _delete_new(self, site_id):
        camp = Site.load(site_id)
        self.assertNotEqual(camp, None)
        camp.delete()
        self.commit()

        
