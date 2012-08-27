
<%inherit file="customer.base.mako"/>\

<input type="hidden" id="customer_id" value="${c.customer.customer_id}">
<input type="hidden" id="company_id" value="${c.company.company_id}">
<input type="hidden" id="pos_email" value="${c.customer.email}">
<input type="hidden" id="tax_rate" value="${c.customer.campaign.tax_rate}">

<div id="checkout" style="height:1000px;">
% if request.GET.get('done', None):
<h1>Order Complete</h1>
<a href="/crm/customer/barcode_order_dialog/${c.customer.email}/${c.company.company_id}">Next Order</a>
% else:

<div class="_50">
  <label for="campaign_id">Campaign</label>
  ${h.select('campaign_id', c.company.default_campaign_id, c.campaigns)}
</div>

<div class="_50">
  <label for="prod_complete2">Search</label>
  ${h.text('prod_complete2', size=50)}
</div>
<div class="clear"></div>      
<div class="_100">
  <table width="100%" id="result_list">
    <tr id="add_product_header">
      <th width="80%">&nbsp;</th>
      <th>&nbsp;</th>
    </tr>
  </table>
  <br>
  <table width="100%">
    <tr>
      <td width="80%">Subtotal</td>
      <td>$<span id="sale_subtotal">0.00</span></td>
    </tr>
    <tr>
      <td>Tax</td>
      <td>$<span id="sale_tax">0.00</span></td>
    </tr>
    <tr>
      <td>Total</td>
      <td>$<span id="sale_total">0.00</span></td>
    </tr>
  </table>
</div>

<div class="clear"></div>

<div class="_50">
  ${h.select('pmt_method', 'Credit Card', c.payment_methods)}
</div>
<div class="_50">
  ${h.text('email', size=20, value="* Email address for receipt", onfocus="$('#email').val('');")}
</div>
<div class="clear"</div>
<div class="_50">
  ${h.checkbox('incl_tax', checked=True, label="Tax?", onchange="customer_barcode_tax_recalc();")}
</div>
<div class="_50">
  ${h.button('btn_complete', 'Done', onclick="customer_barcode_add_order();", class_="form-button")}
</div>

<font color="red"><h1><div id="alerts"></div></h1></font>

<script>
var product_ids = {
% for p in c.products:
"${p.name}": ${p.product_id},
% endfor
'-1': -1
};

var product_skus = {
% for p in c.products:
"${p.sku}": {"product_id" : ${p.product_id},
             "name" : "${p.name}"
            },
% endfor
'-1': -1
}

var products = [
% for p in c.products:
"${p.name}",
% endfor
''
];

</script>

% endif
</div>
