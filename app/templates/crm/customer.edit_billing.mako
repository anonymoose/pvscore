
<%inherit file="customer.base.mako"/>\


<form id="frm_billing"> 
  ${h.hidden('customer_id', value=c.customer.customer_id)}
  ${h.hidden('billing_id', value=c.customer.billing.billing_id)}
  <table>
    <tr valign="top">
      <td>
        <table>
          <tr><td><label for="type">Type</label></td><td>${h.select('type', c.customer.billing.type, c.billing_types)}<td></tr>
          <tr><td><label for="is_primary">Primary ?</label></td><td>${h.checkbox('is_primary', checked=True, disabled=True)}</td>
          <tr><td nowrap><label for="account_holder">Account Holder</label></td><td>${h.text('account_holder', size=50, value=c.customer.billing.account_holder)}</td></tr>
          <tr><td><label for="account_addr">Address</label></td><td>${h.text('account_addr', size=50, value=c.customer.billing.account_addr)}</td></tr>
          <tr><td><label for="account_city">City</label></td><td>${h.text('account_city', size=50, value=c.customer.billing.account_city)}</td></tr>
          <tr><td><label for="account_state">State</label></td><td>${h.text('account_state', size=50, value=c.customer.billing.account_state)}</td></tr>
          <tr><td><label for="account_zip">Zip</label></td><td>${h.text('account_zip', size=50, value=c.customer.billing.account_zip)}</td></tr>
          <tr><td><label for="account_country">Country</label></td><td>${h.text('account_country', size=50, value=c.customer.billing.account_country)}</td></tr>
          <tr><td><label for="cc_token">Card Ref #</label></td><td>${h.text('cc_token', size=20, value=c.customer.billing.cc_token)}</td></tr>
          <tr><td nowrap><label for="cc_num">New Credit Card #</label></td><td>${h.text('cc_num', size=20)}</td></tr>
          <tr><td><label for="cc_last_4">Current Card</label></td><td>**** **** **** ${c.customer.billing.cc_last_4}</td></tr>
          <tr><td><label for="cc_exp">Expiration</label></td><td>${h.text('cc_exp', size=7, value=c.customer.billing.cc_exp)}</td></tr>
          <tr><td><label for="note">Note</label></td><td>${h.text('note', size=50, value=c.customer.billing.note)}</td></tr>
        </table>
      </td>
    </tr>
  </table>
</form>



