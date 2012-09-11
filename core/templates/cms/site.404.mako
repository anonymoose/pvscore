<%inherit file="/common/default_header.mako"/>\

<%def name="other_head()">
    ${h.stylesheet_link('/public/css/login.css')}
</%def>

<%def name="meta_title()">
Page Not Found
</%def>

<div id="container"> 
<p>${c.site.company.enterprise.name}</p>
<br>
<p>Page Not Found</p> 
</div>

