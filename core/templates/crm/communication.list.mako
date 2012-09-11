
<%inherit file="communication.base.mako"/>\

<h1>Communication List</h1>

% if comms:
<div id="result_list">
  <table class="results sortable table table-striped" width="100%">
    <thead>
      <tr>
        <td>ID</td>
        <td>Name</td>
        <td>Create Date</td>
      </tr>
    </thead>
    <tbody>
      % for cmp in comms:
      <tr>
        <td>${cmp.comm_id}</td>
        <td>${h.link_to(cmp.name, '/crm/communication/edit/%d' % cmp.comm_id)}</td>
        <td nowrap>${cmp.create_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

