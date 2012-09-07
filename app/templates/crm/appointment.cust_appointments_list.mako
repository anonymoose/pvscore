
<%inherit file="/crm2/customer.edit.base.mako"/>\


<h1>Customer Appointment List</h1>

% if hasattr(c, 'appointments'):
<div id="result_list">
  <table class="results">
    % for a in c.appointments:
    <tr>
      <td><img src="/public/images/icons/silk/page_edit.png" border="0" onclick="appointment_edit(${a.appointment_id})"></td>
      <td nowrap>${a.title}</td>
      <td nowrap>${a.start_dt}</td>
      <td>${a.phone}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

