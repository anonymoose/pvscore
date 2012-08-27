
<%inherit file="event.base.mako"/>\


<h1>Event List</h1>

% if events:
<div id="result_list">
  <table class="results sortable table-striped" width="100%">
    <thead>
      <tr>
        <td>Short Name</td>
        <td>Name</td>
        <td>Type</td>
        <td>ID</td>
        <td>Phase</td>
      </tr>
    </thead>
    <tbody>
      % for ev in events:
      <tr>
        <td>${h.link_to(ev.short_name, '/crm/event/edit/%s' % ev.event_id)}</td>
        <td>${ev.display_name}</td>
        <td>${ev.event_type}</td>
        <td>${ev.event_id}</td>
        <td>${ev.phase}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

