
<%inherit file="siteedit.base.mako"/>\

<h1>Site List</h1>

% if hasattr(c, 'sites'):
<div id="result_list">
  <table width="100%" class="sortable">
    % for p in c.sites:
    <tr>
      <td nowrap>${h.link_to(p.domain, '/cms/siteedit/edit/%d' % p.site_id)}</td>
      <td nowrap>${p.create_dt}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

