
<%inherit file="users.base.mako"/>\
<%
c.username = (c.username if hasattr(c, 'username') else '')
c.fname = (c.fname if hasattr(c, 'fname') else '')
c.lname = (c.lname if hasattr(c, 'lname') else '')
c.email = (c.email if hasattr(c, 'email') else '')
%>

<h1>User Search</h1>
<strong>Use full or partial matching on any/all fields to find users.  Values are combined to narrow results.</strong>
<hr>
<div id="frm_users_search"> 
  ${h.secure_form(h.url('/crm/users/search'))}
  <div class="_50">
    <label for="username">Username</label>
    ${h.text('username', size=50, value=c.username)}
  </div>
  <div class="_50">
    <label for="fname">First Name</label>
    ${h.text('fname', size=50, value=c.fname)}
  </div>
  <div class="_50">
    <label for="lname">Last Name</label>
    ${h.text('lname', size=50, value=c.lname)}
  </div>
  <div class="_50">
    <label for="email">Email Address</label>
    ${h.text('email', size=50, value=c.email)}
  </div>
  <div class="align-right">
    ${h.submit('search', 'Search', class_="form-button")}
  </div>
  ${h.end_form()}
</div>

% if hasattr(c, 'users'):
<div id="result_list">
  <table class="results">
    % for u in c.users:
    <tr>
      <td>${h.link_to(u.username, '/crm/users/edit/%s' % u.username)}</td>
      <td>${u.fname}</td>
      <td>${u.lname}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

