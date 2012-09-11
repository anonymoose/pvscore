
<%inherit file="purchase.base.mako"/>\

<h1>Purchase Order List</h1>

% if purchases:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <td>Name</td>
        <td>Total</td>
        <td>Created</td>
        <td>Note</td>
      </tr>
    </thead>
    <tbody>
      % for po in purchases:
      <tr>
        <td nowrap>${h.link_to(po.vendor.name, '/crm/purchase/edit/%d' % po.purchase_order_id)}</td>
        <td>${h.money(po.total())}</td>
        <td nowrap>${po.create_dt}</td>
        <td>${h.nvl(po.note)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif
