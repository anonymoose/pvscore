
<%inherit file="customer.edit.base.mako"/>\

<h1>Customer Appointment List</h1>

% if appointments:
<div id="result_list">
  <table class="results table table-striped table-condensed">
    <thead>
      <th>&nbsp;</th>
      <th>Title</th>
      <th>Starts</th>
      <th>Phone</th>
    </thead>
    <tbody>
      % for a in appointments:
      <tr>
        <td><a href="/crm/appointment/edit_for_customer/${a.customer_id}/${a.appointment_id}"><img src="/static/icons/silk/page_edit.png" border="0"/></a></td>
        <td nowrap>${a.title}</td>
        <td nowrap>${a.start_dt} @ ${a.start_time}</td>
        <td>${h.nvl(a.phone)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

