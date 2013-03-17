
<%inherit file="communication.base.mako"/>\

<h1>Communication List</h1>

% if comms:
<div id="result_list">
  <table class="results sortable table table-striped" width="100%">
    <thead>
      <tr>
        <td>Name</td>
        <td>Create Date</td>
      </tr>
    </thead>
    <tbody>
      % for cmp in comms:
      <tr>
        <td>${h.link_to(cmp.name, '/crm/communication/edit/%s' % cmp.comm_id)}</td>
        <td nowrap>${h.date_time(cmp.create_dt)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

