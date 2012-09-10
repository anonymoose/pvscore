from app.tests import TestController, secure
from app.model.crm.comm import Communication
from app.model.crm.customer import Customer

# T app.tests.controllers.test_crm_comm

TEST_CUSTOMER_ID = 220

class TestCrmCommunication(TestController):
    
    def _create_new(self):
        R = self.get('/crm/communication/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Email Template')
        f = R.forms['frm_comm']
        self.assertEqual(f['comm_id'].value, '')
        f.set('name', 'Test Comm')
        f.set('from_addr', 'from@pvs.com')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_comm']
        R.mustcontain('Edit Email Template')
        comm_id = f['comm_id'].value
        self.assertEqual(f['name'].value, 'Test Comm')
        self.assertEqual(f['from_addr'].value, 'from@pvs.com')
        return comm_id


    def _delete_new(self, comm_id):
        Communication.full_delete(comm_id)
        self.commit()


    @secure
    def test_create_new(self):
        comm_id = self._create_new()
        self._delete_new(comm_id)


    @secure
    def test_show_new(self):
        R = self.get('/crm/communication/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Email Template')
        f = R.forms['frm_comm']
        self.assertEqual(f['comm_id'].value, '')
        self.assertEqual(f['name'].value, '')
        self.assertEqual(f['from_addr'].value, '')


    @secure
    def test_list_with_new(self):
        comm_id = self._create_new()
        R = self.get('/crm/communication/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Comm')
        self._delete_new(comm_id)


    @secure
    def test_save_existing(self):
        comm_id = self._create_new()
        R = self.get('/crm/communication/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Comm')

        R = self.get('/crm/communication/edit/%s' % comm_id)
        R.mustcontain('Edit Email Template')
        f = R.forms['frm_comm']
        f.set('name', 'Test Comm New')
        f.set('from_addr', 'fromnew@pvs.com')

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_comm']
        R.mustcontain('Edit Email Template')

        self.assertEqual(f['comm_id'].value, comm_id)
        self.assertEqual(f['name'].value, 'Test Comm New')
        self.assertEqual(f['from_addr'].value, 'fromnew@pvs.com')

        self._delete_new(comm_id)


    @secure
    def test_view_comm_dialog(self):
        cust = Customer.load(TEST_CUSTOMER_ID)
        order = cust.get_active_orders()[0]
        R = self.get('/crm/communication/view_comm_dialog/%s/3?order_id=%s&dialog=1' % (TEST_CUSTOMER_ID, order.order_id))
        self.assertEqual(R.status_int, 200)
        R.mustcontain('%s %s' % (cust.fname, cust.lname))


    @secure
    def test_send_comm_dialog(self):
        R = self.get('/crm/communication/send_comm_dialog?customer_id=%s&dialog=1' % TEST_CUSTOMER_ID)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('No communications configured for users to send.')

        
