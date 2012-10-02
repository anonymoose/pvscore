from pvscore.tests import TestController, secure
from pvscore.model.crm.campaign import Campaign

# T pvscore.tests.controllers.test_crm_campaign

class TestCrmCampaign(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/crm/campaign/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Campaign')
        f = R.forms['frm_campaign']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_list_with_new(self):
        campaign_id = self._create_new()
        R = self.get('/crm/campaign/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Campaign')
        self._delete_new(campaign_id)


    @secure
    def test_single_search(self):
        campaign_id = self._create_new()
        camp = Campaign.load(campaign_id)
        R = self.post('/crm/campaign/search',
                      {'name': 'Test Campaign',
                       'company_id' : camp.company_id})
        R.mustcontain('%s : Test Campaign' % campaign_id)
        self._delete_new(campaign_id)


    @secure
    def test_save_existing(self):
        campaign_id = self._create_new()
        R = self.get('/crm/campaign/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Campaign')

        R = self.get('/crm/campaign/edit/%s' % campaign_id)
        R.mustcontain('Edit Campaign')
        f = R.forms['frm_campaign']
        self.assertEqual(f['campaign_id'].value, campaign_id)
        self.assertEqual(f['name'].value, 'Test Campaign')
        self.assertEqual(f['default_url'].value, 'testxyz.com')
        self.assertEqual(f['email'].value, 'ken@testxyz.com')

        f.set('name', 'Test Campaign New')
        f.set('default_url', 'testxyz.com New')
        f.set('email', 'ken@testxyz.com New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_campaign']
        R.mustcontain('Edit Campaign')

        self.assertEqual(f['campaign_id'].value, campaign_id)
        self.assertEqual(f['name'].value, 'Test Campaign New')
        self.assertEqual(f['default_url'].value, 'testxyz.com New')
        self.assertEqual(f['email'].value, 'ken@testxyz.com New')

        self._delete_new(campaign_id)


    def _create_new(self):
        R = self.get('/crm/campaign/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Campaign')
        f = R.forms['frm_campaign']
        self.assertEqual(f['campaign_id'].value, '')
        f.set('name', 'Test Campaign')
        f.set('default_url', 'testxyz.com')
        f.set('email', 'ken@testxyz.com')
        f.set('smtp_username', 'suser')
        f.set('smtp_password', 'spass')
        f.set('smtp_server', 'sserver')
        f.set('imap_username', 'imapuser')
        f.set('imap_password', 'imappass')
        f.set('imap_server', 'imapserver')
        f.set('attr_name[0]', 'attr0key')
        f.set('attr_value[0]', 'attr0val')
        f.set('attr_name[1]', 'attr1key')
        f.set('attr_value[1]', 'attr1val')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_campaign']
        R.mustcontain('Edit Campaign')
        campaign_id = f['campaign_id'].value
        self.assertNotEqual(f['campaign_id'].value, '')
        return campaign_id


    def _delete_new(self, campaign_id):
        camp = Campaign.load(campaign_id)
        self.assertNotEqual(camp, None)
        camp.delete()
        self.commit()

        
