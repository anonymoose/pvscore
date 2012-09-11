
<%inherit file="/crm2/customer.base.mako"/>\

<div id="frm_appointment"> 
  ${h.secure_form(h.url('/crm/customer/save_appointment'))}
  <table>
    <tr><td><label for="fname"></label></td><td>${h.text('fname', size=50, value=c.customer.fname)}</td></tr>
    <tr><td><label for="lname">Last Name</label></td><td>${h.text('lname', size=50, value=c.customer.lname)}</td></tr>
    <tr valign="top"><td><label for="notes">Notes</label></td><td>${h.textarea('notes', c.customer.notes, style="width: 100%; height: 200px;")}</td></tr>
  </table>
  ${h.end_form()}
</div>
