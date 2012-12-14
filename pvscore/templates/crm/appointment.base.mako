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
      <li><hr></li>
      <li>
        <form id="frm_appointment_search" method="POST" action="/crm/appointment/search" class="form-inline">
          <input type="hidden" name="inline" value="1"/>
          <input name="title" type="text"
                 placeholder="Appointment Search"
                 id="appointment_search" data-provide="typeahead" data-source="[]" maxlength="30" autocomplete="off"/>
        </form>
      </li>
    </ul>
  </div>
</div>
</%def>



