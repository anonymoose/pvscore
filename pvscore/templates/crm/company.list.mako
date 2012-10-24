
<%inherit file="company.base.mako"/>\

<h1>Company List</h1>

% if companies:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <tbody>
    % for cmp in companies:
    <tr>
      <td>${cmp.company_id}</td>
      <td nowrap>${h.link_to(cmp.name, '/crm/company/edit/%s' % cmp.company_id)}</td>
      <td nowrap>${cmp.create_dt}</td>
    </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

