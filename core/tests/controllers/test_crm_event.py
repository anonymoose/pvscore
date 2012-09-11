from pvscore.tests import TestController, secure
from pvscore.model.core.statusevent import StatusEvent

# T pvscore.tests.controllers.test_crm_event

class TestCrmEvent(TestController):
    
    def _create_new(self):
        R = self.get('/crm/event/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Event')
        f = R.forms['frm_event']
        self.assertEqual(f['event_id'].value, '')
        f.set('display_name', 'Test Event')
        f.set('short_name', 'TestEvent')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_event']
        R.mustcontain('Edit Event')
        event_id = f['event_id'].value
        self.assertEqual(f['display_name'].value, 'Test Event')
        self.assertEqual(f['short_name'].value, 'TestEvent')
        return event_id


    def _delete_new(self, event_id):
        StatusEvent.full_delete(event_id)
        self.commit()


    @secure
    def test_create_new(self):
        event_id = self._create_new()
        self._delete_new(event_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/event/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Event')
        f = R.forms['frm_event']
        self.assertEqual(f['event_id'].value, '')
        self.assertEqual(f['short_name'].value, '')


    @secure
    def test_list_with_new(self):
        event_id = self._create_new()
        R = self.get('/crm/event/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Event')
        self._delete_new(event_id)


    @secure
    def test_save_existing(self):
        event_id = self._create_new()
        R = self.get('/crm/event/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Event')

        R = self.get('/crm/event/edit/%s' % event_id)
        R.mustcontain('Edit Event')
        f = R.forms['frm_event']
        f.set('display_name', 'Test Event')
        f.set('short_name', 'TestEvent')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_event']
        R.mustcontain('Edit Event')

        self.assertEqual(f['event_id'].value, event_id)
        self.assertEqual(f['display_name'].value, 'Test Event')
        self.assertEqual(f['short_name'].value, 'TestEvent')

        self._delete_new(event_id)


