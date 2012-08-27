<%inherit file="base.mako"/>\

${next.body()}

<%def name="left_col()">\
<div class="left_align_top">
  <h2>Sites</h2>
  <ul class="side-list">
    <li>${h.link_to('List Sites', '/cms/siteedit/list')}</li>
    <li>${h.link_to('New Site', '/cms/siteedit/new')}</li>
  </ul>
</div>
</%def>
