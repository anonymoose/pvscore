<%inherit file="base.mako"/>\

${next.body()}

<%def name="left_col()">\
<div class="left_align_top">
  <h2>Customer Mgmt.</h2>
  <ul class="side-list">
    <li><a href="/crm/customer/dialog/crm/customer.search">Search</a></li>
    % if c.current_user.priv.edit_customer:
    <li><a href="/crm/customer/new">New</a></li>
    % endif
  </ul>
</div>
</%def>


