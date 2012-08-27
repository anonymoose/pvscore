
<%!
from app.model.core.users import Users
from pylons.controllers.util import redirect
%>

<%inherit file="customer.base.mako"/>\

<%
c.company_name = (c.company_name if hasattr(c, 'company_name') else '')
c.fname = (c.fname if hasattr(c, 'fname') else '')
c.lname = (c.lname if hasattr(c, 'lname') else '')
c.email = (c.email if hasattr(c, 'email') else '')
c.phone = (c.phone if hasattr(c, 'phone') else '')
c.external_cart_id = (c.external_cart_id if hasattr(c, 'external_cart_id') else '')

if hasattr(c, 'customers') and len(c.customers) == 1:
   redirect('/crm/customer/edit/%s' % c.customers[0].customer_id)
%>

<h1>Customer Search</h1>
<strong>Use full or partial matching on any/all fields to find customers.  Values are combined to narrow results.</strong>
<hr>
<div id="frm_users_search">
  ${h.secure_form(h.url('/crm/customer/search'))}
  <div class="_50">
    <label for="fname">First Name</label>
    ${h.text('fname', size=50, value=c.fname)}
  </div>
  <div class="_50">
    <label for="lname">Last Name</label>
    ${h.text('lname', size=50, value=c.lname)}
  </div>
  <div class="_50">
    <label for="company_name">Company Name</label>
    ${h.text('company_name', size=50, value=c.company_name)}
  </div>
  <div class="_50">
    <label for="email">Email Address</label>
    ${h.text('email', size=50, value=c.email)}
  </div>
  <div class="_50">
    <label for="phone">Phone</label>
    ${h.text('phone', size=50, value=c.phone)}
  </div>
  <div class="_50">
    <label for="external_cart_id">External Cart ID</label>
    ${h.text('external_cart_id', size=50, value=c.external_cart_id)}
  </div>
  <div class="align-right">
    ${h.submit('submit', 'Search', class_="form-button")}&nbsp;
  </div>
  ${h.end_form()}
</div>

% if hasattr(c, 'customers'):
<div id="result_list">
  <table class="results sortable">
    % for cust in c.customers:
    <tr>
      <td>${h.link_to(cust.email if cust.email else '*no email*', '/crm/customer/edit/%d' % cust.customer_id)}</td>
      <td>${cust.fname}</td>
      <td>${cust.lname}</td>
      <td>${cust.phone}</td>
      <td>${cust.company_name}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
