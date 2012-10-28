
<%inherit file="site.base.mako"/>\

<h1>Site List</h1>

% if sites:
<div id="result_list">
  <table width="100%" class="table table-striped">
    <tbody>
    % for s in sites:
    <tr>
      <td nowrap>${h.link_to(s.domain, '/cms/site/edit/%s' % s.site_id)}</td>
      <td nowrap>${s.create_dt}</td>
    </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

