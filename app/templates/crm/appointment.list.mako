
<%inherit file="appointment.base.mako"/>\

<h1>Appointment List</h1>

% if hasattr(c, 'appointments'):
<div id="result_list">
  <table class="results">
    % for a in c.appointments:
    <tr>
      <td nowrap>${h.link_to(a.title, '/plugin/appointment/edit/%d' % a.appointment_id)}</td>
      <td nowrap>${a.create_dt}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

