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
      <li class="nav-header">${last_site.domain}</li>
      <li><a href="/cms/site/edit/${last_site.site_id}">Edit Site</a></li>
      <li><a href="http://${last_site.domain}" target="_blank">Visit Site</a></li>
      <li><hr></li>
      <li class="nav-header">Files</li>
      <li><a href="/cms/content/file/list/${last_site.site_id}">List ${last_site.domain} Files</a></li>
      <li><a href="/cms/content/file/new/${last_site.site_id}">Add File for ${last_site.domain}</a></li>
      <li><hr></li>
      <li class="nav-header">Content Blocks</li>
      <li><a href="/cms/content/list/${last_site.site_id}">List ${last_site.domain} Content</a></li>
      <li><a href="/cms/content/new/${last_site.site_id}">Add Content for ${last_site.domain}</a></li>
    % else:
      <li class="nav-header">Select a site</li>
      <li><a href="/cms/site/list">List Websites</a></li>
    % endif
    </ul>
  </div>
</%def>

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
