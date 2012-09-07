
<%inherit file="appointment.base.mako"/>\

<h1>Appointment List</h1>

% if appointments:
<div id="result_list">
  <table class="results table table-striped">
    % for a in appointments:
    <tr>
      % if a.customer_id:
      <td nowrap>${h.link_to(a.title, '/crm/appointment/edit_for_customer/%d/%d' % (a.customer_id, a.appointment_id))}</td>
      % else:
      <td nowrap>${h.link_to(a.title, '/crm/appointment/edit/%d' % a.appointment_id)}</td>
      % endif
      <td nowrap>${a.start_dt} @ ${a.start_time}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

