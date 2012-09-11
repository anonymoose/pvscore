
<%inherit file="template.base.mako"/>\

<h1>Template List</h1>

% if hasattr(c, 'templates'):
<div id="result_list">
  <table width="100%">
    <tr>
      <th>Name</th>
      <th>Path</th>
      <th nowrap>Create Dt</th>
    </tr>
    % for t in c.templates:
    <tr>
      <td nowrap>${h.link_to(t.name, '/cms/template/edit/%d' % t.template_id)}</td>
      <td>${t.relative_path}</td>
      <td nowrap>${t.create_dt}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

