
<%inherit file="product.edit.base.mako"/>\

<h3>Returns</h3>

<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <th>Date</th>
        <th>Customer</th>
        <th>Quantity</th>
        <th nowrap>Credit Amount</th>
        <th>User</th>
      </tr>
    </thead>
    % for r in returns:
    <tr>
      <td nowrap>${r.create_dt}</td>
      <td nowrap>${r.order.customer.email if not request.ctx.user.is_vendor_user() else ''}</td>
      <td>${h.money(r.quantity)}</td>
      <td>${h.money(r.credit_amount)}</td>
      <td>${r.user_created}</td>
    </tr>
    % endfor
  </table>
</div>

