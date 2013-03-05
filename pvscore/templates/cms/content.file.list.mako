
<%inherit file="site.base.mako"/>\

<h1>${request.ctx.site.domain} File List</h1>

% if contents:
<div id="result_list">
  <table width="100%" class="table table-striped">
    <tbody>
    % for s in contents:
    <tr>
      <td nowrap><a href="/cms/content/file/edit/${request.ctx.site.site_id}/${s.id}"><img src="${s.absolute_path}" style="height:100px;" /></a></td>
      <td nowrap>${s.name}</td>
      <td nowrap>${h.date_time(s.create_dt)}</td>
    </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

