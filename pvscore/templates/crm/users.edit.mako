
<%inherit file="users.base.mako"/>\

<div> 
  <h1>Edit User</h1>
  <div class="container">
    <form id="frm_users" method="POST" action="/crm/users/save">
      ${h.hidden('user_id', value=user.user_id)}
      
      <h3>General Information</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="username">Username</label>
            ${h.text('username',  value=user.username)}
          </div>
          <div class="span3">
            <label for="fname">First Name</label>
            ${h.text('fname',  value=user.fname)}
          </div>
          <div class="span3">
            <label for="lname">Last Name</label>
            ${h.text('lname',  value=user.lname)}
          </div>
        </div>    
      </div>
      
      <h3>Security</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="password">Password</label>
            ${h.password('password', value=''.join(['-' for i in range(user.password_len)]) if user.password_len else '',  onclick="$('#password').val('')")}
          </div>
          <div class="span3">
            <label for="confirm">Confirm</label>
            ${h.password('confirm', value=''.join(['-' for i in range(user.password_len)]) if user.password_len else '',  onclick="$('#confirm').val('')")}
          </div>
        </div>    
        <div class="row">
          <div class="span4">
            <b>Permissions</b>
          </div>
        </div>
        <div class="row">
          <div class="span8">
            <table>
              <tr>
                <td nowrap>${h.chkbox('pv_view_customer', checked=priv.view_customer, label='View Customer')}</td>
                <td nowrap>${h.chkbox('pv_edit_customer', checked=priv.edit_customer, label='Edit Customer')}</td>
                <td nowrap>${h.chkbox('pv_view_product', checked=priv.view_product, label='View Product')}</td>
                <td nowrap>${h.chkbox('pv_edit_product', checked=priv.edit_product, label='Edit Product')}</td>
                <td nowrap>${h.chkbox('pv_view_users', checked=priv.view_users, label='View Users')}</td>
                <td nowrap>${h.chkbox('pv_edit_users', checked=priv.edit_users, label='Edit Users')}</td>
                <td nowrap>${h.chkbox('pv_view_campaign', checked=priv.view_campaign, label='View Campaign')}</td>
                <td nowrap>${h.chkbox('pv_edit_campaign', checked=priv.edit_campaign, label='Edit Campaign')}</td>
              </tr>
              <tr>
                <td nowrap>${h.chkbox('pv_view_event', checked=priv.view_event, label='View Event')}</td>
                <td nowrap>${h.chkbox('pv_edit_event', checked=priv.edit_event, label='Edit Event')}</td>
                <td nowrap>${h.chkbox('pv_view_communication', checked=priv.view_communication, label='View Communication')}</td>
                <td nowrap>${h.chkbox('pv_edit_communication', checked=priv.edit_communication, label='Edit Communication')}</td>
                <td nowrap>${h.chkbox('pv_view_report', checked=priv.view_report, label='View Report')}</td>
                <td nowrap>${h.chkbox('pv_edit_report', checked=priv.edit_report, label='Edit Report')}</td>
                <td nowrap>${h.chkbox('pv_view_company', checked=priv.view_company, label='View Company')}</td>
                <td nowrap>${h.chkbox('pv_edit_company', checked=priv.edit_company, label='Edit Company')}</td>
              </tr>
              <tr>
                <td nowrap>${h.chkbox('pv_view_enterprise', checked=priv.view_enterprise, label='View Enterprise')}</td>
                <td nowrap>${h.chkbox('pv_edit_enterprise', checked=priv.edit_enterprise, label='Edit Enterprise')}</td>
                <td nowrap>${h.chkbox('pv_add_customer_order', checked=priv.add_customer_order, label='Add Customer Order')}</td>
                <td nowrap>${h.chkbox('pv_add_customer_billing', checked=priv.add_customer_billing, label='Add Customer Billing')}</td>
                <td nowrap>${h.chkbox('pv_view_purchasing', checked=priv.view_purchasing, label='View Purchasing')}</td>
                <td nowrap>${h.chkbox('pv_edit_purchasing', checked=priv.edit_purchasing, label='Edit Purchasing')}</td>
                <td nowrap>${h.chkbox('pv_cms', checked=priv.cms, label='CMS')}</td>
                <td nowrap>${h.chkbox('pv_send_customer_emails', checked=priv.send_customer_emails, label='Send Emails')}</td>
              </tr>
              <tr>
                <td nowrap>${h.chkbox('pv_modify_customer_order', checked=priv.modify_customer_order, label='Modify Orders')}</td>
                <td nowrap>${h.chkbox('pv_edit_category', checked=priv.edit_category, label='Edit Categories')}</td>
                <td nowrap>${h.chkbox('pv_barcode_order', checked=priv.barcode_order, label='Barcode Order')}</td>
                <td nowrap>${h.chkbox('pv_edit_discount', checked=priv.edit_discount, label='Edit Discounts')}</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
      
      <h3>Email</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="email">Email</label>
            ${h.text('email',  value=user.email)}
          </div>
          <div class="span3">
            <label for="smtp_username">SMTP Username</label>
            ${h.text('smtp_username',  value=user.smtp_username)}
          </div>
          <div class="span3">
            <label for="smtp_password">SMTP Password</label>
            ${h.password('smtp_password',  value=user.smtp_password)}
          </div>
          <div class="span2">
            <label for="smtp_server">SMTP Server</label>
            ${h.text('smtp_server',  value=user.smtp_server)}
          </div>
        </div>
        <div class="row">
          <div class="span3 offset3">
            <label for="imap_username">IMAP Username</label>
            ${h.text('imap_username',  value=user.imap_username)}
          </div>
          <div class="span3">
            <label for="imap_password">IMAP Password</label>
            ${h.password('imap_password',  value=user.imap_password)}
          </div>
          <div class="span2">
            <label for="imap_server">IMAP Server</label>
            ${h.text('imap_server',  value=user.imap_server)}
          </div>
        </div>
      </div>
      
      <h3>Advanced</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="type">User Type</label>
            ${h.select('type', user.type, user_types)}
          </div>
          <div class="span3">
            <label for="api_key">API Key</label>
            ${h.text('api_key',  value=user.api_key)}
          </div>
          
          <div class="span3">
            <label for="vendor_id">Vendor</label>
            ${h.select('vendor_id', str(user.vendor_id), vendors)}
          </div>
          
          <div class="span2">
            <label for="vendor_id">Timezone</label>
            ${h.select('tz_offset', user.tz_offset, [(5, 'EST'), (6, 'CST'), (7, 'MST'), (8, 'PST')])}
          </div>
        </div>
        <div class="row">
          <div class="span6">
            <label for="login_link">Login Link</label>
            ${h.text('login_link', size=100, value=user.login_link)}
          </div>
        </div>
      </div>
      
      % if request.ctx.user.priv.edit_users:
        <div class="row">
          <div class="span2 offset10">
            <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
          </div>
        </div>
      % endif
    </form>
  </div>
</div>

