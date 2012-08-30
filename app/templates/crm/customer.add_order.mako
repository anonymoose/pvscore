
<%inherit file="customer.edit.base.mako"/>\

<input type="hidden" name="campaign_id" id="campaign_id" value="${customer.campaign.campaign_id}"/>

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

  <table width="100%" class="table table-striped">
    <tr id="add_product_header">
      <th width="30%">Name</th>
      <th style="text-align:right;">Price</th>
      <th style="text-align:right;">Quantity</th>
      <th style="text-align:right;" nowrap>Current Inventory</th>
    </tr>
    % for p in products:
    <tr>
      <td nowrap>${h.checkbox('chk_%d' % p.product_id, value=p.product_id, label=' %s' % p.name, onchange='customer_add_product_oncheck(%d)' % p.product_id)}</td>
      <td style="text-align:right;">$${h.money(p.get_unit_price(customer.campaign))}</td>
      <td style="text-align:right;">${h.text('quant_%d' % p.product_id, style="width:40px;")}</td>
      <td style="text-align:right;">${p.inventory}</td>
    </tr>
    % endfor
  </table>
</div>


