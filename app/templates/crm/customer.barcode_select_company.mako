
<%inherit file="customer.base.mako"/>\


<div id="frm_campaign"> 
  <form action="/crm/customer/barcode_order_dialog2" method="POST">
    <table>
      <tr><td>Company</td><td>${h.select('company_id', None, c.companies)}<td></tr>
      <tr><td>Email</td><td>${h.text('email', size=50, value='POS@yourdomain.com')}<td></tr>
      <tr><td>&nbsp;</td><td>${h.submit('submit', 'Submit')}<td></tr>
    </table>
  </form>
</div>


