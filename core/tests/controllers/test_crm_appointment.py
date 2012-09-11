from pvscore.tests import TestController, secure
from pvscore.model.crm.appointment import Appointment
import pvscore.lib.util as util

# T pvscore.tests.controllers.test_crm_appointment

TEST_CUSTOMER_ID = 220
YESTERDAY = util.yesterday()
TODAY = util.today()
TOMORROW = util.tomorrow()

class TestCrmAppointment(TestController):

    @secure
    def test_show_new(self):
        R = self.get('/crm/appointment/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Appointment')
        f = R.forms['frm_appointment']
        self.assertEqual(f['title'].value, '')


    def _create_new(self):
        # create the appointment and ensure he's editable.
        R = self.get('/crm/appointment/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Appointment')
        f = R.forms['frm_appointment']
        self.assertEqual(f['appointment_id'].value, '')
        f.set('title', 'Test Appointment')
        f.set('phone', '9041234567')
        f.set('description', 'Test Description')
        f.set('start_dt', util.format_date(TOMORROW))
        f.set('start_time', '09:00')
        f.set('end_time', '10:00')        
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_appointment']
        R.mustcontain('Edit Appointment')
        appointment_id = f['appointment_id'].value
        self.assertNotEqual(f['appointment_id'].value, '')
        return appointment_id


    def _create_new_for_customer(self):
        # create the appointment and ensure he's editable.
        R = self.get('/crm/appointment/new_for_customer/%s' % TEST_CUSTOMER_ID)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('New Appointment')
        f = R.forms['frm_appointment']

        self.assertEqual(f['appointment_id'].value, '')
        self.assertEqual(f['customer_id'].value, str(TEST_CUSTOMER_ID))

        f.set('title', 'Test Customer Appointment')
        f.set('phone', '9041234567')
        f.set('description', 'Test Description')
        f.set('start_dt', util.format_date(TOMORROW))
        f.set('start_time', '09:00')
        f.set('end_time', '10:00')        

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)

        f = R.forms['frm_appointment']
        R.mustcontain('Edit Customer Appointment')
        appointment_id = f['appointment_id'].value
        self.assertNotEqual(f['appointment_id'].value, '')
        self.assertEqual(f['customer_id'].value, str(TEST_CUSTOMER_ID))
        return appointment_id


    def _delete_new(self, appointment_id):
        Appointment.full_delete(int(str(appointment_id)))
        self.commit()


    @secure
    def test_create_new(self):
        appointment_id = self._create_new()
        self._delete_new(appointment_id)

    @secure
    def test_list(self):
        appointment_id = self._create_new()
        R = self.get('/crm/appointment/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Appointment')
        self._delete_new(appointment_id)


    @secure
    def test_edit_existing(self):
        appointment_id = self._create_new()
        R = self.get('/crm/appointment/edit/%s' % appointment_id)
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_appointment']
        R.mustcontain('Edit Appointment')
        self.assertEqual(str(f['appointment_id'].value) , str(appointment_id))
        
        self.assertEqual(f['title'].value, 'Test Appointment')
        self.assertEqual(f['description'].value, 'Test Description')

        f.set('title', 'Test Appointment New')
        f.set('description', 'Test Description New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_appointment']
        R.mustcontain('Edit Appointment')

        self.assertEqual(f['title'].value, 'Test Appointment New')
        self.assertEqual(f['description'].value, 'Test Description New')
        self._delete_new(appointment_id)


    @secure
    def test_create_new_for_customer(self):
        appointment_id = self._create_new_for_customer()
        self._delete_new(appointment_id)


    @secure
    def test_edit_existing_for_customer(self):
        appointment_id = self._create_new_for_customer()
        R = self.get('/crm/appointment/edit_for_customer/%s/%s' % (TEST_CUSTOMER_ID, appointment_id))
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_appointment']
        R.mustcontain('Edit Customer Appointment')
        self.assertEqual(str(f['appointment_id'].value) , str(appointment_id))
        self.assertEqual(str(f['customer_id'].value) , str(TEST_CUSTOMER_ID))
        
        self.assertEqual(f['title'].value, 'Test Customer Appointment')
        self.assertEqual(f['description'].value, 'Test Description')

        f.set('title', 'Test Customer Appointment New')
        f.set('description', 'Test Description New')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_appointment']
        R.mustcontain('Edit Customer Appointment')

        self.assertEqual(f['title'].value, 'Test Customer Appointment New')
        self.assertEqual(f['description'].value, 'Test Description New')
        self.assertEqual(str(f['customer_id'].value) , str(TEST_CUSTOMER_ID))
        self._delete_new(appointment_id)


    @secure
    def test_list_for_customer(self):
        appointment_id = self._create_new_for_customer()
        R = self.get('/crm/appointment/show_appointments/%s' % TEST_CUSTOMER_ID)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Customer Appointment')
        self._delete_new(appointment_id)
        

    @secure
    def test_search(self):
        appointment_id1 = self._create_new_for_customer()
        appointment_id2 = self._create_new()

        R = self.get('/crm/appointment/show_search')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Appointment Search')
        f = R.forms["frm_appointment_search"]
        f.set('title', 'Test')
        R = f.submit('submit')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Appointment Search')
        R.mustcontain('Test Appointment')
        R.mustcontain('Test Customer Appointment')
        R.mustcontain('/crm/appointment/edit_for_customer/%s/%s' % (TEST_CUSTOMER_ID, appointment_id1))
        R.mustcontain('/crm/appointment/edit/%s' % appointment_id2)
        self._delete_new(appointment_id2)
        self._delete_new(appointment_id2)


    @secure
    def test_day_view(self):
        appointment_id1 = self._create_new_for_customer()
        appointment_id2 = self._create_new()
        
        R = self.get('/crm/appointment/day_view/%s/%s/%s' % (TOMORROW.year, TOMORROW.month, TOMORROW.day))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Appointment')
        R.mustcontain('Test Customer Appointment')
        R.mustcontain('/crm/appointment/edit_for_customer/%s/%s' % (TEST_CUSTOMER_ID, appointment_id1))
        R.mustcontain('/crm/appointment/edit/%s' % appointment_id2)
        R.mustcontain('/crm/appointment/day_view/%s/%s/%s' % (TODAY.year, TODAY.month, TODAY.day))

        self._delete_new(appointment_id2)
        self._delete_new(appointment_id2)

        R = self.get('/crm/appointment/tomorrow')
        self.assertEqual(R.status_int, 200)

        R = self.get('/crm/appointment/this_day')
        self.assertEqual(R.status_int, 200)


    @secure
    def test_month_view(self):
        appointment_id1 = self._create_new_for_customer()
        appointment_id2 = self._create_new()
        
        R = self.get('/crm/appointment/month_view/%s/%s' % (TOMORROW.year, TOMORROW.month))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('/crm/appointment/edit_for_customer/%s/%s' % (TEST_CUSTOMER_ID, appointment_id1))
        R.mustcontain('/crm/appointment/edit/%s' % appointment_id2)

        self._delete_new(appointment_id2)
        self._delete_new(appointment_id2)

        R = self.get('/crm/appointment/this_month')
        self.assertEqual(R.status_int, 200)
        
        
              

