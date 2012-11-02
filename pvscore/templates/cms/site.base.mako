<%inherit file="/crm/base.mako"/>\

${next.body()}


<%def name="left_col()">
<%
from pvscore.model.cms.site import Site
last_site = None
if 'last_site_id' in request.session:
   last_site = Site.load(request.session['last_site_id'])
%>
  <div class="well sidebar-nav">
    <ul class="nav nav-list">
      % if last_site:
      <li><b><a href="/cms/site/edit/${last_site.site_id}">Edit ${last_site.domain}</a></b></li>
      <li><b><a href="http://${last_site.domain}" target="_blank">Visit ${last_site.domain}</a></b></li>
      <li><hr></li>
      
      % else:
      Select a site
      % endif
    </ul>
  </div>
</%def>

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
