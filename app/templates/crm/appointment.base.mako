<%inherit file="/crm2/base.mako"/>\

${next.body()}

<%def name="other_head()">
  ${h.javascript_link('/plugs/appointment/static/js/appointment.js')}
</%def>

<%def name="left_col()">
<div class="left_align_top">
  <h2>Appointments</h2>
  <ul class="side-list">
    <li><a href="/plugin/appointment/this_day">Today</a></li>
    <li><a href="/plugin/appointment/this_month">This Month</a></li>
    <li><a href="/plugin/appointment/show_search">Search</a></li>
    <li><a href="/plugin/appointment/list">List</a></li>
    <li><a href="/plugin/appointment/new">New</a></li>
  </ul>
</div>
</%def>

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>



