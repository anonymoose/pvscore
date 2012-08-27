
<%inherit file="customer.base.mako"/>\

<table>
  <tr valign="top">
    <td>
        <table width="100%">
          <tr><td>Type</td><td><b>${c.journal.type}</b></td></tr>
          <tr><td>Created</td><td>${c.journal.create_dt}</td></tr>
          <tr><td>User</td><td>${c.journal.user_created}</td></tr>
          <tr><td>Amount</td><td>${h.money(c.journal.amount)}</td></tr>
          <tr><td nowrap>Order ID</td><td>${c.journal.order_id}</td></tr>
          <tr valign="top"><td>Note</td><td>${h.literal(c.journal.note if c.journal.note else '')}</td></tr>
        </table>
    </td>
  </tr>
</table>
