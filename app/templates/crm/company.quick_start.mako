
<%inherit file="company.base.mako"/>\

<h1>Quickstart:  Create a new enterprise</h1>
<form method="POST" action="/crm/company/provision" id="frm_quick">
% if not done:
<div> 
    <table>
      <tr><td><h3>Company Info</h3></td></tr>
      <tr><td><label for="ent_name">Enterprise Name</label></td><td>${h.text('ent_name', size=50)}<td></tr>
      <tr><td><label for="cmp_name">Company Name</label></td><td>${h.text('cmp_name', size=50)}<td></tr>
      <tr><td><label for="st_domain">Domain</label></td><td>${h.text('st_domain', size=50)}</td></tr>
      <tr><td><h3>User Info</h3></td></tr>
      <tr><td><label for="u_username">Username</label></td><td>${h.text('u_username', size=50)}</td></tr>
      <tr><td><label for="u_fname">First Name</label></td><td>${h.text('u_fname', size=50)}<td></tr>
      <tr><td><label for="u_lname">Last Name</label></td><td>${h.text('u_lname', size=50)}<td></tr>
      <tr><td><label for="u_email">Email Address</label></td><td>${h.text('u_email', size=50)}<td></tr>

      <tr><td><input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/></td></tr>
    </table>

</div>

% else:
    <table>
      <input type="enterprise_id" name="enterprise_id" value="${enterprise.enterprise_id}"/>
      <tr><td><label for="ent_name">Enterprise ID</label></td><td>${enterprise.enterprise_id}<td></tr>
      <tr><td><label for="ent_name">Company ID</label></td><td>${company.company_id}<td></tr>
      <tr><td><label for="ent_name">Campaign ID</label></td><td>${campaign.campaign_id}<td></tr>
      <tr><td><label for="ent_name">User ID</label></td><td>${user.username}<td></tr>
      <tr><td><label for="ent_name">Site ID</label></td><td>${site.site_id}<td></tr>
    </table>

% endif
</form>
