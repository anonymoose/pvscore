from app.tests import TestController, secure, UID
from app.model.core.users import Users

# T app.tests.controllers.test_crm_users

class TestCrmUsers(TestController):
    
    def _create_new(self):
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
        usr = Users.load(username)
        orig_pwd = usr.password
        R = self.post('/crm/users/save_password',
                      {'username': username,
                       'password': 'fud'})
        R.mustcontain('True')
        usr.invalidate_caches()
        usr = Users.load(username)
        self.assertNotEqual(usr.password, orig_pwd)
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


