
<%inherit file="product.edit.base.mako"/>\

<h3>Purchases</h3>

<div id="result_list">
  <table width="100%" class="results sortable table-striped">
    <thead>
      <tr>
        <th>Date</th>
        <th>Quantity</th>
        <th nowrap>Unit Cost</th>
        <th nowrap>Item Cost</th>
        <th nowrap>Order Cost</th>
        <th nowrap>Complted Dt</th>
      </tr>
    </thead>
    % for poi in purchase_order_items:
    <tr>
      <td nowrap><a href="${'/crm/purchase/edit/${poi.purchase_order.purchase_order_id' if not request.ctx.user.is_vendor_user() else '#'}">${poi.create_dt}</a></td>
      <td nowrap>${poi.quantity}</td>
      <td>${h.money(poi.unit_cost)}</td>
      <td>${h.money(poi.total())}</td>
      <td>${h.money(poi.purchase_order.total())}</td>
      <td>${poi.complete_dt}</td>
    </tr>
    % endfor
  </table>
</div>




