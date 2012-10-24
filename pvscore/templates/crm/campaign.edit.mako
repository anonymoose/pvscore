
<%inherit file="company.base.mako"/>\

<div>
  <h1>Edit Campaign</h1>
  <div class="container">
    <form method="POST" action="/crm/campaign/save" id="frm_campaign">
      ${h.hidden('campaign_id', value=campaign.campaign_id)}

      <div class="well">
        <h3>General Information</h3>
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=campaign.name)}
          </div>
          <div class="span3">
            <label for="company_id">Company</label>
            ${h.select('company_id', str(campaign.company_id), companies)}
          </div>
          <div class="span3">
            <label for="tax_rate">Tax Rate</label>
            ${h.text('tax_rate', size=50, value=campaign.tax_rate)}
          </div>
          <div class="span2">
            <label for="default_url">Default URL</label>
            ${h.text('default_url', size=50, value=campaign.default_url)}
          </div>
        </div>
      </div>

      <div class="well">
        <h3>Email</h3>
        <div class="row">
        </div>
          
        <div class="row">
          <div class="span3">
            <label for="email">Email</label>
            ${h.text('email', size=50, value=campaign.email)}
          </div>
          <div class="span3">
            <label for="smtp_username">SMTP Username</label>
            ${h.text('smtp_username', size=50, value=campaign.smtp_username)}
          </div>
          <div class="span3">
            <label for="smtp_password">SMTP Password</label>
            ${h.password('smtp_password', size=50, value=campaign.smtp_password)}
          </div>
          <div class="span2">
            <label for="smtp_server">SMTP Server</label>
            ${h.text('smtp_server', size=50, value=campaign.smtp_server)}
          </div>
        </div>
        <div class="row">
          <div class="span3 offset3">
            <label for="imap_username">IMAP Username</label>
            ${h.text('imap_username', size=50, value=campaign.imap_username)}
          </div>
          <div class="span3">
            <label for="imap_password">IMAP Password</label>
            ${h.password('imap_password', size=50, value=campaign.imap_password)}
          </div>
          <div class="span2">
            <label for="imap_server">IMAP Server</label>
            ${h.text('imap_server', size=50, value=campaign.imap_server)}
          </div>
        </div>
      </div>
      <div class="row">
        <div class="span6">
          <h3>Campaign Attributes</h3>
          <table>
            <%
               attrs = campaign.get_attrs()
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
          <h3>Customer Communications</h3>
          <div>
            <label for="comm_post_purchase_id">Post-purchase Communication</label>
            ${h.select('comm_post_purchase_id', str(campaign.comm_post_purchase_id), comms)}
          </div>
          <div>
            <label for="comm_post_cancel_id">Post-cancellation Communication</label>
            ${h.select('comm_post_cancel_id', str(campaign.comm_post_cancel_id), comms)}
          </div>
          <div>
            <label for="comm_packing_slip_id">Packing Slip Communication</label>
            ${h.select('comm_packing_slip_id', str(campaign.comm_packing_slip_id), comms)}
          </div>
          <div>
            <label for="comm_forgot_password_id">Forgot Password Communication</label>
            ${h.select('comm_forgot_password_id', str(campaign.comm_forgot_password_id), comms)}
          </div>
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


