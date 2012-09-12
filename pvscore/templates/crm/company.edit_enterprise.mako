
<%inherit file="company.base.mako"/>\

<div>
  <h1>Edit Enterprise</h1>
  <div class="container">
    
    <form method="POST" action="/crm/company/enterprise/save" id="frm_enterprise">
      ${h.hidden('enterprise_id', value=the_enterprise.enterprise_id)}
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=the_enterprise.name)}
          </div>
          <div class="span3">
            <label for="logo_path">Logo Path</label>
            ${h.text('logo_path', size=50, value=the_enterprise.logo_path)}
          </div>
          
          <div class="span3">
            <label for="logo_path">Support Email</label>
            ${h.text('support_email', size=50, value=the_enterprise.support_email)}
          </div>
          <div class="span2">
            <label for="">Billing Method</label>
            ${h.select('billing_method', the_enterprise.billing_method, billing_methods)}
          </div>


          <div class="span3">
            <label for="copyright">Copyright</label>
            ${h.text('copyright', size=50, value=the_enterprise.copyright)}
          </div>
          <div class="span3">
            <label for="logo_path">Logo Path (PDF)</label>
            ${h.text('logo_path_pdf', size=50, value=the_enterprise.logo_path_pdf)}
          </div>
          <div class="span3">
            <label for="logo_path">Support Phone</label>
            ${h.text('support_phone', size=20, value=the_enterprise.support_phone)}
          </div>
        </div>
      </div>

      <div class="row">
        <div class="span6">
          <h3>Company Attributes</h3>
          <table>
            <%
               attrs = the_enterprise.get_attrs()
               idx = 0
               %>
            % for attr_name in attrs:
            <tr>
              <td>${h.text('attr_name[%d]' % idx, size=30, value=attr_name)}</td><td>${h.text('attr_value[%d]' % idx, size=30, value=attrs[attr_name])}</td>
            </tr>
            <% idx = idx + 1 %>
            % endfor
            % for i in range(idx,10):
            <tr>
              <td>${h.text('attr_name[%d]' % i, size=30)}</td><td>${h.text('attr_value[%d]' % i, size=30)}</td>
            </tr>
            <% idx = idx + 1 %>
            % endfor
          </table>
        </div>
        <div class="span6">
          <label for="name">CRM Stylesheet</label>
          ${h.textarea('crm_style', style="width: 100%; height: 100px;", content=the_enterprise.crm_style)}
        </div>
      </div>
      
      <div class="row">
        <div class="span2 offset10">
          <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
        </div>
      </div>
    </form>
  </div>
</div>

