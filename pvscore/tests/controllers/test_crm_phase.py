from pvscore.tests import TestController, secure
from pvscore.model.crm.customer import CustomerPhase

# T pvscore.tests.controllers.test_crm_phase

class TestCrmPhase(TestController):

    def _create_new(self):
        R = self.get('/crm/phase/new')
        assert R.status_int == 200
        R.mustcontain('Edit Phase')
        f = R.forms['frm_phase']
        self.assertEqual(f['phase_id'].value, '')
        f.set('display_name', 'Test Phase')
        f.set('short_name', 'TestPhase')
        f.set('color', 'LightBlue')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_phase']
        R.mustcontain('Edit Phase')
        phase_id = f['phase_id'].value
        self.assertEqual(f['display_name'].value, 'Test Phase')
        self.assertEqual(f['short_name'].value, 'TestPhase')
        self.assertEqual(f['color'].value, 'LightBlue')
        return phase_id


    def _delete_new(self, phase_id):
        CustomerPhase.full_delete(phase_id)
        self.commit()


    @secure
    def test_create_new(self):
        phase_id = self._create_new()
        self._delete_new(phase_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/phase/new')
        assert R.status_int == 200
        R.mustcontain('Edit Phase')
        f = R.forms['frm_phase']
        self.assertEqual(f['phase_id'].value, '')
        self.assertEqual(f['short_name'].value, '')


    @secure
    def test_list_with_new(self):
        phase_id = self._create_new()
        R = self.get('/crm/phase/list')
        assert R.status_int == 200
        R.mustcontain('Test Phase')
        self._delete_new(phase_id)


    @secure
    def test_save_existing(self):
        phase_id = self._create_new()
        R = self.get('/crm/phase/list')
        assert R.status_int == 200
        R.mustcontain('Test Phase')

        R = self.get('/crm/phase/edit/%s' % phase_id)
        R.mustcontain('Edit Phase')
        f = R.forms['frm_phase']
        f.set('display_name', 'Test Phase')
        f.set('short_name', 'TestPhase')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        assert R.status_int == 200
        f = R.forms['frm_phase']
        R.mustcontain('Edit Phase')

        self.assertEqual(f['phase_id'].value, phase_id)
        self.assertEqual(f['display_name'].value, 'Test Phase')
        self.assertEqual(f['short_name'].value, 'TestPhase')

        self._delete_new(phase_id)


