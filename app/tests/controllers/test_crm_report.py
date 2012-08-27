import pdb
from pyramid import testing
from app.tests import *
from app.tests import Session
import simplejson as json
from app.controllers.crm.login import LoginController
from app.model.crm.report import Report

# T app.tests.controllers.test_crm_report

class TestCrmReport(TestController):
    @secure
    def test_show_new(self):
        R = self.get('/crm/report/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Report')
        f = R.forms['frm_report']
        self.assertEqual(f['name'].value, '')


    @secure
    def test_list_with_new(self):
        report_id = self._create_new()
        R = self.get('/crm/report/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Report')
        self._delete_new(report_id)


    @secure
    def test_create_new(self):
        report_id = self._create_new()
        self._delete_new(report_id)


    @secure
    def test_show(self):
        report_id = self._create_new()
        R = self.get('/crm/report/show/%s' % report_id)
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Description')
        R.mustcontain('Product')  # because show_product_id == True
        R.mustcontain('rpt_product_id')
        self._delete_new(report_id)


    @secure
    def test_results(self):
        report_id = self._create_new()
        R = self.get('/crm/report/results/%s' % report_id)
        json.loads(R.body)
        self._delete_new(report_id)


    @secure
    def test_results_export(self):
        report_id = self._create_new()
        R = self.get('/crm/report/results_export/%s' % report_id)
        self.assertEqual(R.headers['Content-Type'], 'application/vnd.ms-excel; charset=UTF-8')
        self.assertEqual(R.headers['Content-Disposition'], 'attachment; filename="report.xls"')
        self._delete_new(report_id)


    @secure
    def test_save_existing(self):
        report_id = self._create_new()
        R = self.get('/crm/report/list')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Test Report')

        R = self.get('/crm/report/edit/%s' % report_id)
        R.mustcontain('Edit Report')
        f = R.forms['frm_report']
        self.assertEqual(f['report_id'].value, report_id)
        self.assertEqual(f['name'].value, 'Test Report')
        self.assertEqual(f['description'].value, 'Test Description')

        f.set('name', 'Test Report New')
        f.set('description', 'Test Description New')
        f['show_product_id'].checked = True
        f['show_campaign_id'].checked = True
        f['show_vendor_id'].checked = True
        f['show_company_id'].checked = True
        f['show_user_id'].checked = True

        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_report']
        R.mustcontain('Edit Report')

        self.assertEqual(f['report_id'].value, report_id)
        self.assertEqual(f['name'].value, 'Test Report New')
        self.assertEqual(f['description'].value, 'Test Description New')
        self.assertEqual(f['show_product_id'].checked, True)
        self.assertEqual(f['show_campaign_id'].checked, True)
        self.assertEqual(f['show_vendor_id'].checked, True)
        self.assertEqual(f['show_company_id'].checked, True)
        self.assertEqual(f['show_user_id'].checked, True)
        self._delete_new(report_id)


    def _create_new(self):
        R = self.get('/crm/report/new')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Edit Report')
        f = R.forms['frm_report']
        self.assertEqual(f['report_id'].value, '')
        f.set('name', 'Test Report')
        f.set('description', 'Test Description')
        f.set('sql', """
select c.customer_id,
  c.fname,
  c.lname,
  c.email,
  c.create_dt,
  c.city, c.state, c.zip, c.phone from
  crm_customer c, crm_campaign cmp, crm_company comp
  where
  c.campaign_id = cmp.campaign_id
  and cmp.company_id = comp.company_id
  and comp.enterprise_id = {enterprise_id}
""")
        f.set('column_names', """
["Customer ID", "First Name", "Last Name", "Email", "Created",
"City", "State", "Zip", "Phone"]""")

        f.set('column_model', """
[{name:"customer_id",index:"id", width:75},        
 {name:"fname",index:"fname", width:90},        
 {name:"lname",index:"lname", width:100},        
 {name:"email",index:"email", width:80},
 {name:"phone", index:"zip", width:50},
 {name:"city", index:"city", width:50},
 {name:"state", index:"state", width:50},
 {name:"zip", index:"zip", width:50},
   {name:"create_dt", index:"create_dt", width:100}
]""")

        f.set('on_dbl_click', """
var id = G('getGridParam','selrow');   
if (id)  {     
  var ret = G('getRowData',id);
  pvs.browser.goto_url('/crm/customer/edit/'+ret.customer_id);
}""")

        f['show_product_id'].checked = True
        f['show_product_id'].checked = True
        f['show_campaign_id'].checked = True
        f['show_vendor_id'].checked = True
        f['show_company_id'].checked = True
        f['show_user_id'].checked = True
        
        R = f.submit('submit')
        self.assertEqual(R.status_int, 302)
        R = R.follow()
        self.assertEqual(R.status_int, 200)
        f = R.forms['frm_report']
        R.mustcontain('Edit Report')
        report_id = f['report_id'].value
        self.assertNotEqual(f['report_id'].value, '')
        self.assertEqual(f['show_product_id'].checked, True)
        return report_id


    def _delete_new(self, report_id):
        c = Report.load(report_id)
        self.assertNotEqual(c, None)
        c.delete()
        self.commit()

        
