
<%inherit file="product.edit.base.mako"/>\

<h3>Sales</h3>

<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <th>Date</th>
        <th>Campaign</th>
        <th>Quantity</th>
        <th>Revenue</th>
        <th>Cost</th>
        <th>Profit</th>
      </tr>
    </thead>
    % for s in sales:
    <tr>
      <td nowrap>${s.create_dt}</td>
      <td nowrap>${s.campaign}</td>
      <td>${s.quantity}</td>
      <td>${h.money(s.revenue)}</td>
      <td>${h.money(s.cost)}</td>
      <td>${h.money(s.profit)}</td>
    </tr>
    % endfor
  </table>
</div>

