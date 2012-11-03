
<%inherit file="site.base.mako"/>\

<h1>${site.domain} Content List</h1>

% if contents:
<div id="result_list">
  <table width="100%" class="table table-striped">
    <tbody>
    % for s in contents:
    <tr>
      <td nowrap>${h.link_to(s.name, '/cms/content/edit/%s/%s' % (s.site_id, s.content_id))}</td>
      <td nowrap>${s.creator.email}</td>
      <td nowrap>${h.date_time(s.create_dt)}</td>
    </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

