
<%inherit file="phase.base.mako"/>\


<h1>Phase List</h1>

% if phases:
<div id="result_list">
  <table class="results sortable table table-striped" width="100%">
    <thead>
      <tr>
        <td>Short Name</td>
        <td>Name</td>
        <td>ID</td>
      </tr>
    </thead>
    <tbody>
      % for ev in phases:
      <tr>
        <td>${h.link_to(ev.short_name, '/crm/phase/edit/%s' % ev.phase_id)}</td>
        <td>${ev.display_name}</td>
        <td>${ev.phase_id}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

