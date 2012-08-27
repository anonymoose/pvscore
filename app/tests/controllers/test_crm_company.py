import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.company import Company, Enterprise
import transaction
from zope.sqlalchemy import mark_changed

# T app.tests.controllers.test_crm_company:TestCrmCompany.test_quickstart

class TestCrmCompany(TestController):

    @secure
    def test_show_new(self):
        R = self.get('/crm/company/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Company')
        f = R.forms['frm_company']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_create_new(self):
        company_id = self._create_new()
        self._delete_new(company_id)


    @secure
    def test_list_with_new(self):
        company_id = self._create_new()
        R = self.get('/crm/company/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Company')
        self._delete_new(company_id)


    @secure
    def test_single_search(self):
        company_id = self._create_new()
        R = self.post('/crm/company/search',
                      {'name': 'Test Company'})
        R.mustcontain('%s : Test Company' % company_id)
        self._delete_new(company_id)


    @secure
    def test_save_existing(self):
        company_id = self._create_new()
        R = self.get('/crm/company/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Company')

        R = self.get('/crm/company/edit/%s' % company_id)
        R.mustcontain('Edit Company')
        f = R.forms['frm_company']
        self.assertEqual(f['company_id'].value, company_id)
        self.assertEqual(f['name'].value, 'Test Company')
        self.assertEqual(f['email'].value, 'ken@testxyz.com')

        f.set('name', 'Test Company New')
        f.set('email', 'ken@testxyz.com New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_company']
        R.mustcontain('Edit Company')

        self.assertEqual(f['company_id'].value, company_id)
        self.assertEqual(f['name'].value, 'Test Company New')
        self.assertEqual(f['email'].value, 'ken@testxyz.com New')

        self._delete_new(company_id)


    def _create_new(self):
        R = self.get('/crm/company/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Company')
        f = R.forms['frm_company']
        self.assertEqual(f['company_id'].value, '')
        f.set('name', 'Test Company')
        f.set('email', 'ken@testxyz.com')
        f.set('addr1', '123 elm')
        f.set('phone', '1234567890')
        f.set('attr_name[0]', 'attr0key')
        f.set('attr_value[0]', 'attr0val')
        f.set('attr_name[1]', 'attr1key')
        f.set('attr_value[1]', 'attr1val')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_company']
        R.mustcontain('Edit Company')
        company_id = f['company_id'].value
        self.assertNotEqual(f['company_id'].value, '')
        return company_id


    def _delete_new(self, company_id):
        c = Company.load(company_id)
        self.assertNotEqual(c, None)
        c.delete()
        self.commit()

        
    @secure
    def test_show_new_enterprise(self):
        R = self.get('/crm/company/enterprise/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Enterprise')
        f = R.forms['frm_enterprise']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_create_new_enterprise(self):
        enterprise_id = self._create_new_enterprise()
        self._delete_new_enterprise(enterprise_id)

    def _create_new_enterprise(self):
        R = self.get('/crm/company/enterprise/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Enterprise')
        f = R.forms['frm_enterprise']
        self.assertEqual(f['enterprise_id'].value, '')
        f.set('name', 'Test Enterprise')
        f.set('support_email', 'ken@testxyz.com')
        f.set('attr_name[0]', 'attr0key')
        f.set('attr_value[0]', 'attr0val')
        f.set('attr_name[1]', 'attr1key')
        f.set('attr_value[1]', 'attr1val')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_enterprise']
        R.mustcontain('Edit Enterprise')
        enterprise_id = f['enterprise_id'].value
        self.assertNotEqual(f['enterprise_id'].value, '')
        return enterprise_id


    def _delete_new_enterprise(self, enterprise_id):
        c = Enterprise.load(enterprise_id)
        self.assertNotEqual(c, None)
        c.delete()
        self.commit()


    @secure
    def test_list_with_new_enterprise(self):
        enterprise_id = self._create_new_enterprise()
        R = self.get('/crm/company/enterprise/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Enterprise')
        self._delete_new_enterprise(enterprise_id)


    @secure
    def test_save_existing(self):
        enterprise_id = self._create_new_enterprise()
        R = self.get('/crm/company/enterprise/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Enterprise')

        R = self.get('/crm/company/enterprise/edit/%s' % enterprise_id)
        R.mustcontain('Edit Enterprise')
        f = R.forms['frm_enterprise']
        self.assertEqual(f['enterprise_id'].value, enterprise_id)
        self.assertEqual(f['name'].value, 'Test Enterprise')
        self.assertEqual(f['support_email'].value, 'ken@testxyz.com')

        f.set('name', 'Test Enterprise New')
        f.set('support_email', 'ken@testxyz.com New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_enterprise']
        R.mustcontain('Edit Enterprise')

        self.assertEqual(f['enterprise_id'].value, enterprise_id)
        self.assertEqual(f['name'].value, 'Test Enterprise New')
        self.assertEqual(f['support_email'].value, 'ken@testxyz.com New')

        self._delete_new_enterprise(enterprise_id)


    @secure
    def test_quickstart(self):
        R = self.get('/crm/company/quickstart')
        R.mustcontain('Quickstart')
        f = R.forms['frm_quick']

        f.set('ent_name', 'Test Enterprise')
        f.set('cmp_name', 'Test Company')
        f.set('st_domain', 'test.com')
        f.set('u_username', 'xxuser@testing.com')
        f.set('u_fname', 'Ken')
        f.set('u_lname', 'Bedwell')
        f.set('u_email', 'utest@testing.com')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 200)

        f = R.forms['frm_quick']
        enterprise_id = f['enterprise_id'].value
        Enterprise.full_delete(enterprise_id, False)

        Users.full_delete('xxuser@testing.com')
        transaction.commit()


