
<%inherit file="company.base.mako"/>\

<div>
  <h1>Edit Company</h1>
  <div class="container">
    <form method="POST" action="/crm/company/save" id="frm_company">
      ${h.hidden('company_id', value=company.company_id)}
      ${h.hidden('enterprise_id', value=company.enterprise_id if company.enterprise_id else request.ctx.enterprise.enterprise_id)}
      
      <h3>General Information</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=company.name)}
          </div>
          <div class="span3">
            <label for="paypal_id">Paypal ID</label>
            ${h.text('paypal_id', size=50, value=company.paypal_id)}
          </div>
          <div class="span3">
            <label for="default_campaign_id">Default Campaign</label>
            ${h.select('default_campaign_id', company.default_campaign_id, campaigns)}
          </div>
        </div>
      </div>
        
      <h3>Address and Phone</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="addr1">Address</label>
            ${h.text('addr1', size=50, value=company.addr1)}
            ${h.text('addr2', size=50, value=company.addr2)}
          
            <label for="city">City</label>
            ${h.text('city', size=50, value=company.city)}

            <label for="state">State</label>
            ${h.text('state', size=50, value=company.state)}

            <label for="zip">Zip</label>
            ${h.text('zip', size=50, value=company.zip)}
          </div>

          <div class="span3">
            <label for="phone">Phone</label>
            ${h.text('phone', size=20, value=company.phone)}
          </div>
          <div class="span3">
            <label for="alt_phone">Alternate Phone</label>
            ${h.text('alt_phone', size=20, value=company.alt_phone)}
          </div>
          <div class="span3">
            <label for="fax">Fax</label>
            ${h.text('fax', size=20, value=company.fax)}
          </div>
          <div class="span3">
            <label for="country">Country</label>
            <select id="country" name="country">
              ${self.country_list()}
            </select>
          </div>
        </div>
      </div>
      
      <h3>Email</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="email">Email</label>
            ${h.text('email', size=50, value=company.email)}
          </div>
          <div class="span3">
            <label for="smtp_username">SMTP Username</label>
            ${h.text('smtp_username', size=50, value=company.smtp_username)}
          </div>
          <div class="span3">
            <label for="smtp_password">SMTP Password</label>
            ${h.password('smtp_password', size=50, value=company.smtp_password)}
          </div>
          <div class="span2">
            <label for="smtp_server">SMTP Server</label>
            ${h.text('smtp_server', size=50, value=company.smtp_server)}
          </div>
        </div>
        <div class="row">
          <div class="span3 offset3">
            <label for="imap_username">IMAP Username</label>
            ${h.text('imap_username', size=50, value=company.imap_username)}
          </div>
          <div class="span3">
            <label for="imap_password">IMAP Password</label>
            ${h.password('imap_password', size=50, value=company.imap_password)}
          </div>
          <div class="span2">
            <label for="imap_server">IMAP Server</label>
            ${h.text('imap_server', size=50, value=company.imap_server)}
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="span6">
          <h3>Company Attributes</h3>
          <table>
            <%
               attrs = company.get_attrs()
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
        
        <div class="row">
          <div class="span2 offset10">
            <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>          


