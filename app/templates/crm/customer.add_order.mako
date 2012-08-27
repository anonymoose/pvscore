
<%inherit file="customer.edit.base.mako"/>\

<input type="hidden" name="campaign_id" id="campaign_id" value="${c.customer.campaign.campaign_id}"/>

<div id="result_list">
  <div class="_50">
    <h1>Add Order</h1>
  </div>
  <div class="_50">
    ${h.button('add_order', 'Add Order', onclick='customer_add_order_submit()', class_="form-button")}
  </div>

  <div class="_100">
    <label for="fname">Search</label>
    ${h.text('prod_complete1', size=50)}
  </div>
  <div class="clear"></div>

  <table width="100%">
    <tr id="add_product_header">
      <th width="30%">Name</th>
      <th style="text-align:right;">Price</th>
      <th style="text-align:right;">Quantity</th>
      <th style="text-align:right;" nowrap>Current Inventory</th>
    </tr>
    % for p in c.products:
    <tr>
      <td nowrap>${h.checkbox('chk_%d' % p.product_id, value=p.product_id, label=p.name, onchange='customer_add_product_oncheck(%d)' % p.product_id, class_='product_chk')}</td>
      <td style="text-align:right;">${h.money(p.get_unit_price(c.customer.campaign))}</td>
      <td style="text-align:right;">${h.text('quant_%d' % p.product_id, style="width:40px;")}</td>
      <td style="text-align:right;">${p.inventory}</td>
    </tr>
    % endfor
  </table>
</div>

<script>
var product_ids = {
% for p in c.products:
"${p.name}": ${p.product_id},
% endfor
'-1': -1
};

var products = [
% for p in c.products:
"${p.name}",
% endfor
''
];

customer_prep_add_product_autocomplete(products, product_ids);
</script>

