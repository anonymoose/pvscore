from pvscore.tests import TestController, secure, secure_as_root, UID, PVS_ROOT_UID
from pvscore.model.core.users import Users
from pvscore.model.crm.company import Enterprise

# T pvscore.tests.controllers.test_crm_users

class TestCrmUsers(TestController):

    def _create_new(self, set_enterprise_id=False):
        ent = Enterprise.find_by_name('Healthy U Store')
        R = self.get('/crm/users/new')
        assert R.status_int == 200
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        self.assertEqual(f['user_id'].value, '')
        f.set('username', 'test@tester.com')
        f.set('email', 'test@tester.com')
        f.set('fname', 'Test')
        f.set('lname', 'User')
        f.set('password', 'fishsticks')
        f.set('confirm', 'fishsticks')
        if set_enterprise_id:
            f.set('enterprise_id', str(ent.enterprise_id))
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_users']
        R.mustcontain('Edit User')
        user_id = f['user_id'].value
        self.assertEqual(f['username'].value, 'test@tester.com')
        self.assertEqual(f['email'].value, 'test@tester.com')
        usr = Users.load(user_id)
        if set_enterprise_id:
            assert str(usr.enterprise_id) == str(ent.enterprise_id)
        else:
            assert usr.enterprise_id == None
        assert usr is not None
        assert usr.get_email_info() is not None
        return user_id


    def _delete_new(self, user_id):
        Users.full_delete(user_id)
        self.commit()


    @secure
    def test_create_new(self):
        user_id = self._create_new()
        self._delete_new(user_id)


    @secure_as_root
    def test_create_new_as_root(self):
        user_id = self._create_new(True)
        self._delete_new(user_id)


    @secure
    def test_save_password(self):
        self._test_save_password()

    @secure_as_root
    def test_save_password_as_root(self):
        self._test_save_password()


    def _test_save_password(self):
        user_id = self._create_new()
        usr = Users.load(user_id)
        orig_pwd = usr.password
        R = self.post('/crm/users/save_password',
                      {'user_id': user_id,
                       'password': 'fud'})
        R.mustcontain('True')
        usr.invalidate_caches()
        usr = Users.load(user_id)
        self.assertNotEqual(usr.password, orig_pwd)
        self._delete_new(user_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/users/new')
        assert R.status_int == 200
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        self.assertEqual(f['user_id'].value, '')
        self.assertEqual(f['fname'].value, '')


    @secure
    def test_list_with_new(self):
        self._test_list_with_new()


    @secure_as_root
    def test_list_with_new_as_root(self):
        self._test_list_with_new(True)


    def _test_list_with_new(self, as_root=False):
        user_id = self._create_new(as_root)
        R = self.get('/crm/users/list')
        assert R.status_int == 200
        R.mustcontain('test@tester.com')
        self._delete_new(user_id)


    @secure
    def test_edit_current(self):
        R = self.get('/crm/users/edit_current')
        assert R.status_int == 200
        R.mustcontain(UID)


    @secure_as_root
    def test_edit_current_as_root(self):
        R = self.get('/crm/users/edit_current')
        assert R.status_int == 200
        R.mustcontain(PVS_ROOT_UID)


    @secure
    def test_save_existing(self):
        self._test_save_existing()


    @secure_as_root
    def test_save_existing(self):
        self._test_save_existing(True)


    def _test_save_existing(self, as_root=False):
        user_id = self._create_new(as_root)
        R = self.get('/crm/users/list')
        assert R.status_int == 200
        R.mustcontain('test@tester.com')

        R = self.get('/crm/users/edit/%s' % user_id)
        R.mustcontain('Edit User')
        f = R.forms['frm_users']
        f.set('fname', 'Testnew')
        f.set('lname', 'Usernew')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_users']
        R.mustcontain('Edit User')

        self.assertEqual(f['user_id'].value, user_id)
        self.assertEqual(f['fname'].value, 'Testnew')
        self.assertEqual(f['lname'].value, 'Usernew')

        self._delete_new(user_id)


