
<%inherit file="template.base.mako"/>\

<%!
import app.lib.util as util
%>

<div id="frm_template"> 
  <h1>Edit Template</h1>

  ${h.secure_form(h.url('/cms/template/save'))}
  ${h.hidden('template_id', value=c.template.template_id)}
  ${h.hidden('enterprise_id', value=c.template.enterprise_id if c.template.enterprise_id else util.get_enterprise_id())}

  <div class="_50">
    <label for="">Name</label>
    ${h.text('name', size=50, value=c.template.name)}
  </div>
  <div class="_50">
    <label for="">Description</label>
    ${h.text('description', size=50, value=c.template.description)}
  </div>
  <div class="_50">
    <label for="">Path</label>
    ${h.text('path', size=50, value=c.template.path)}
  </div>
  <div class="_50">
    <label for="">File</label>
    ${h.text('file', size=50, value=c.template.file)}
  </div>
  % if c.template.template_id:
  <div class="_50">
    <label for="">Create Date</label>
    ${h.nvl(c.template.create_dt)}
  </div>
  <div class="_50">
    <label for="">Delete Date</label>
    ${h.nvl(c.template.delete_dt)}
  </div>
  % endif
  <div class="clear"></div>
  <div class="align-right">
    ${h.submit('submit', 'Submit', class_="form-button")}
  </div>
  ${h.end_form()}
</div>
