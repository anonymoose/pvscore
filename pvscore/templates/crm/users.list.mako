
<%inherit file="users.base.mako"/>\

<h1>User List</h3>
% if users:
<div id="result_list">
  <table class="results sortable table table-striped" width="100%">
    <thead>
      <tr>
        <td>Username</td>
        <td>First Name</td>
        <td>Last Name</td>
        <td>Vendor</td>
      </tr>
    </thead>
    <tbody>
      % for u in users:
      <tr>
        <td>${h.link_to(u.username, '/crm/users/edit/%s' % u.user_id)}</td>
        <td>${u.fname}</td>
        <td>${u.lname}</td>
        <td>${u.vendor.name if u.vendor else ''}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

<%def name="draw_body()">\
${self.draw_body_no_left_col()}
</%def>
