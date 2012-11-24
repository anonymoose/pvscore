from pvscore.tests import TestController, secure
from pvscore.model.cms.content import Content
import logging, transaction


log = logging.getLogger(__name__)

# T pvscore.tests.controllers.test_cms_content

class TestCmsContent(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/cms/content/new/%s' % self.site.site_id)
        assert R.status_int == 200
        R.mustcontain('New Content Block')
        f = R.forms['frm_content']
        self.assertEqual(f['content_id'].value, '')
        self.assertEqual(f['site_id'].value, str(self.site.site_id))


    @secure
    def test_create_new(self):
        content_id = content_create_new(self)
        content_delete_new(content_id)


    @secure
    def test_list_with_new(self):
        content_id = content_create_new(self)
        R = self.get('/cms/content/list/%s' % self.site.site_id)
        assert R.status_int == 200
        R.mustcontain('nosetest.content.0')
        content_delete_new(content_id)


    @secure
    def test_save_existing(self):
        content_id = content_create_new(self)
        R = self.get('/cms/content/list/%s' % self.site.site_id)
        assert R.status_int == 200
        R.mustcontain('nosetest.content.0')

        R = self.get('/cms/content/edit/%s/%s' % (self.site.site_id, content_id))
        R.mustcontain('Edit Content Block')
        f = R.forms['frm_content']
        self.assertEqual(str(f['content_id'].value), str(content_id))
        self.assertEqual(f['name'].value, 'nosetest.content.0')

        f.set('name', 'nosetest.content.1')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_content']
        R.mustcontain('Edit Content Block')

        self.assertEqual(f['name'].value, 'nosetest.content.1')
        content_delete_new(content_id)


    @secure
    def test_content(self):
        content_id = content_create_new(self)
        R = self.get('/content?content_name=nosetest.content.0')
        assert R.status_int == 200
        R.mustcontain('nosetest.content.0')
        R.mustcontain(str(self.site.site_id))
        content_delete_new(content_id)


    def test_content_non_existant(self):
        R = self.get('/content?content_name=bogus.bogus')
        assert R.status_int == 200
        assert R.body.replace('\n', '') == ''



def content_create_new(self_):
    R = self_.get('/cms/content/new/%s' % self_.site.site_id)
    assert R.status_int == 200
    R.mustcontain('New Content Block')
    f = R.forms['frm_content']
    assert f['content_id'].value == ''
    f.set('name', 'nosetest.content.0')
    f.set('data', "${request.GET['content_name']} ${request.ctx.site.site_id}")
    
    R = f.submit('submit')
    assert R.status_int == 302
    R = R.follow()
    assert R.status_int == 200
    f = R.forms['frm_content']
    R.mustcontain('Edit Content Block')
    content_id = f['content_id'].value
    assert f['content_id'].value != ''
    content = Content.load(content_id)
    return content.content_id


def content_delete_new(content_id):
    content = Content.load(content_id)
    assert content != None
    content.delete()
    transaction.commit()
    
