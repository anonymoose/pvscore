
<%inherit file="product.edit.base.mako"/>\

<h3>Orders</h3>

<div id="result_list">
  <table width="100%" class="results sortable table-striped">
    <thead>
      <tr>
        <th>Date</th>
        <th>Customer</th>
        <th>Campaign</th>
        <th>Quantity</th>
        <th>Revenue</th>
        <th>Cost</th>
        <th>Profit</th>
      </tr>
    </thead>
    <tbody>
      % for s in orders:
      <tr>
        <td nowrap>${s.create_dt}</td>
        <td nowrap><a href="${'/crm/customer/edit/%s' % s.customer_id if not request.ctx.user.is_vendor_user() else '#'}">${s.email}</a></td>
        <td nowrap>${s.campaign}</td>
        <td>${s.quantity}</td>
        <td>${h.money(s.revenue)}</td>
        <td>${h.money(s.cost)}</td>
        <td>${h.money(s.profit)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>

