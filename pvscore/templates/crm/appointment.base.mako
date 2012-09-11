<%inherit file="base.mako"/>\

${next.body()}

<%def name="left_col()">
<div class="left_align_top">
  <div class="well sidebar-nav">
    <ul class="nav nav-list">
      <li><a href="/crm/appointment/this_day">Today</a></li>
      <li><a href="/crm/appointment/this_month">This Month</a></li>
      <li><a href="/crm/appointment/show_search">Search</a></li>
      <li><a href="/crm/appointment/list">List</a></li>
      <li><a href="/crm/appointment/new">New</a></li>
    </ul>
  </div>
</div>
</%def>



