import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.company import Company, Enterprise
from app.model.crm.campaign import Campaign
import transaction
from zope.sqlalchemy import mark_changed
from app.model.core.users import Users

# T app.tests.controllers.test_crm_users

class TestCrmUsers(TestController):
    
    def _create_new(self):
        # probably a better way to get the preferred enterprise here.
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]

        R = self.get('/crm/users/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        self.assertEqual(f['username'].value, '')
        f.set('username', 'test@tester.com')
        f.set('email', 'test@tester.com')
        f.set('fname', 'Test')
        f.set('lname', 'User')
        f.set('password', 'fishsticks')
        f.set('confirm', 'fishsticks')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_users']
        R.mustcontain('Edit Users')
        username = f['username'].value
        self.assertEqual(f['username'].value, 'test@tester.com')
        self.assertEqual(f['email'].value, 'test@tester.com')
        return username


    def _delete_new(self, username):
        Users.full_delete(username)
        self.commit()

    @secure
    def test_save_password(self):
        username = self._create_new()
        u = Users.load(username)
	orig_pwd = u.password
        R = self.post('/crm/users/save_password',
                      {'username': username,
                       'password': 'fud'})
        R.mustcontain('True')
        u.invalidate_caches()
        u = Users.load(username)
        self.assertNotEqual(u.password, orig_pwd)
        self._delete_new(username)


    @secure
    def test_create_new(self):
        username = self._create_new()
        self._delete_new(username)


    @secure
    def test_show_new(self):
        R = self.get('/crm/users/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        self.assertEqual(f['username'].value, '')
        self.assertEqual(f['fname'].value, '')


    @secure
    def test_list_with_new(self):
        username = self._create_new()
        R = self.get('/crm/users/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('test@tester.com')
        self._delete_new(username)


    @secure
    def test_edit_current(self):
        R = self.get('/crm/users/edit_current')
        self.assertEqual(R.status_int, 200)
        R.mustcontain(UID)


    @secure
    def test_save_existing(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]

        username = self._create_new()
        R = self.get('/crm/users/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('test@tester.com')

        R = self.get('/crm/users/edit/%s' % username)
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        f.set('fname', 'Testnew')
        f.set('lname', 'Usernew')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_users']
        R.mustcontain('Edit User')

        self.assertEqual(f['username'].value, username)
        self.assertEqual(f['fname'].value, 'Testnew')
        self.assertEqual(f['lname'].value, 'Usernew')

        self._delete_new(username)


