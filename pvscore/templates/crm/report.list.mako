<%inherit file="report.base.mako"/>\

<h1>Report List</h1>

% if reports:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <td>Report</td>
        <td>Edit</td>
      </tr>
    </thead>
    <tbody>
      % for cmp in reports:
      <tr>
        <td nowrap>${h.link_to(cmp.name, '/crm/report/show/%s' % cmp.report_id)}</td>
        <td>${h.link_to('Edit', '/crm/report/edit/%s' % cmp.report_id)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

