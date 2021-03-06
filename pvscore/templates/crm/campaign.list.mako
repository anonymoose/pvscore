
<%inherit file="company.base.mako"/>\

<h1>Campaign List</h1>

% if campaigns:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <tbody>
    % for cmp in campaigns:
      <tr>
        <td nowrap>${h.link_to(cmp.name, '/crm/campaign/edit/%s' % cmp.campaign_id)}</td>
        <td nowrap>${h.slash_date(cmp.create_dt)}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

