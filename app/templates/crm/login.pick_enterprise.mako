<%inherit file="/common/default_header.mako"/>\

<%def name="other_head()">
    ${h.stylesheet_link('/public/css/login.css')}
</%def>

<%def name="meta_title()">
${c.site.company.enterprise.name} CRM Login
</%def>

<div id="container"> 

${h.secure_form(h.url('/crm/login/pick_enterprise'))}
  <div id="dialog">

    <input type="hidden" name="path" value="${h.nvl(c.path)}"/>
    <input type="hidden" name="vars" value="${h.nvl(c.vars)}"/>

    <table cellspacing="10" id="standard"> 
      <tr><td width="100" align="right">Enterprise</td><td>${h.select('enterprise_id', None, c.enterprises)}</td></tr>
      <tr><td colspan="2">or...</td></tr>  
      <tr><td width="100" nowrap>Input Enterprise ID</td><td>${h.text('aux_enterprise_id', size=10)}</td></tr> 
    </table> 
    
    <div style="text-align:center; padding-bottom: 10px;"><input name="submit" type="submit" value="Login" /></div> 
  </div> 
${h.end_form()}
</div> 
