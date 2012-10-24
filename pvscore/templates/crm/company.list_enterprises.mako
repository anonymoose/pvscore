
<%inherit file="company.base.mako"/>\

<h1>Enterprise List</h1>

% if enterprises:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
    % for cmp in enterprises:
    <tr>
      <td>${cmp.enterprise_id}</td>
      <td>${h.link_to(cmp.name, '/crm/company/enterprise/edit/%s' % cmp.enterprise_id)}</td>
      <td nowrap>${cmp.create_dt}</td>
    </tr>
    % endfor
    </thead>
  </table>
</div>
% endif
