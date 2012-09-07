
<%inherit file="customer.edit.base.mako"/>\

<h1>Customer Appointment List</h1>

% if appointments:
<div id="result_list">
  <table class="results table table-striped table-condensed">
    <tbody>
      % for a in appointments:
      <tr>
        <td><img src="/static/icons/silk/page_edit.png" border="0" onclick="appointment_edit(${a.appointment_id})"></td>
        <td nowrap>${a.title}</td>
        <td nowrap>${a.start_dt}</td>
        <td>${a.phone}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

