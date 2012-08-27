<%!
    from app.lib.plugin import plugin_registry
%>

<%inherit file="customer.edit.base.mako"/>\

% if c.customer.fname and c.customer.lname:
<h1>Edit Order for <i><b>${c.customer.fname} ${c.customer.lname}</i></b></h1>
% else:
<h1>Edit Order</h1>
% endif

<%
total_price = c.order.total_price()
total_payments_applied = c.order.total_payments_applied()
total_discounts_applied = c.order.total_discounts_applied()
%>
<form id="frm_edit_order">
<input type="hidden" id="oi_order_id" value="${c.order.order_id}">
<input type="hidden" id="total_price" value="${total_price}">
<div class="_100">
  <label for="">Total</label>
  <span id="oi_total_price" align="right">$${h.money(total_price)}</span>
</div>
<div class="clear"></div>
<div class="_25">
  <label for="">Payments Applied</label>
  <span id="oi_payments_applied"
        % if c.order.order_id and total_payments_applied < total_price:
        style="color:red;"
        % endif
        align="right">$${h.money(total_payments_applied)}</span>
</div>
<div class="_25">
      % if c.order.order_id and total_payments_applied < total_price:
      <a href="javascript:customer_apply_payment(${c.order.order_id})">Apply Payment</a>
      % endif
</div>
<div class="clear"></div>
<div class="_25">
  <label for="">Discounts Applied</label>
  <span id="oi_discounts_applied">$${h.money(total_discounts_applied)}</span>
  <td>&nbsp;</td>
</div> 
<div class="_25">
  <a href="javascript:customer_apply_discount(${c.order.order_id})">Apply Discount</a>
</div> 
<div class="clear"></div>
<div class="bump"></div>
<div class="_50">
  <label for="">Created Dt</label>
  ${h.text('order_create_dt', size=10, value=c.order.create_dt)}
</div>
<div class="_50">
  <label for="">Creator</label>
  ${c.order.user_created if c.order.user_created else 'Customer'}
</div>
<div class="clear"></div>
<div class="_50">
  <label for="">Shipping Total</label>
    <td>${h.text('shipping_total', size=10, value=h.money(c.order.shipping_total), onblur='customer_order_recalc()')}</td>
</div>
% if c.comm_packing_slip_id:
<div class="_25">
  <label for="">Shipping</label>
  ${c.order.shipping_note if c.order.shipping_note else ''}
</div>
<div class="_25">
  <a href="javascript:customer_view_packing_slip(${c.order.order_id}, ${c.comm_packing_slip_id})">View Packing Slip</a>
</div>
% endif
<div class="clear"></div>

% if c.order.external_cart_id:
<div class="_25">
  <label for="">External Cart ID</label>
  ${h.nvl(c.order.external_cart_id)}
</div>
% endif

<table width="100%">
  <tr valign="top">
    <td colspan="4">
      <div id="result_list">
        <table width="100%">
          <thead id="result_list_header">
            <td>&nbsp</td>
            <td>&nbsp</td>
            <td>&nbsp</td>
            <th>Product</th>
            <th nowrap>Unit Price</th>
            <th>Quantity</th>
            <th nowrap>Sub Total</th>
          </thead>
          % for oi in c.order.active_items:
          <tr id="oi_${oi.order_item_id}">
            % if total_payments_applied > 0:
              <td><img src="/public/images/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                       onclick="customer_delete_order_item('${oi.order_item_id}')"  class="img_delete"
                       style="display:none;">
              </td>
              <td>
                <img src="/public/images/icons/silk/comment_add.png" 
                     border="0" title="Status Order" alt="Status Order" 
                     onclick="customer_status_order_item(%{oi.order_id} ${oi.order_item_id})"/>
              </td>
              <td><img src="/public/images/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0" 
                       onclick="customer_return_order_item('${c.order.order_id}', '${oi.order_item_id}', ${oi.quantity}, ${oi.total()})" class="img_return"></td>
              <td width="40%">${oi.product.name}</td>
              <td>${h.text('unit_price[%d]' % oi.order_item_id, size=10, value=h.money(oi.unit_price), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;" >${h.text('quantity[%d]' % oi.order_item_id, size=10, value=h.money(oi.quantity), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">${h.money(oi.total())}</td>
            % else:
              <td><img src="/public/images/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                       onclick="customer_delete_order_item('${oi.order_item_id}')" class="img_delete"></td>
              <td>
                <img src="/public/images/icons/silk/comment_add.png" 
                     border="0" title="Status Order" alt="Status Order" 
                     onclick="customer_status_order_item(${oi.order_id}, ${oi.order_item_id})"/>
              </td>
              <td><img src="/public/images/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0" 
                       onclick="customer_return_order_item('${c.order.order_id}', '${oi.order_item_id}', ${oi.quantity}, ${oi.total()})" class="img_return"
                       style="display:none;"></td>
              <td width="40%">${oi.product.name}</td>
              <td>${h.text('unit_price[%d]' % oi.order_item_id, size=10, value=h.money(oi.unit_price), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;" >${h.text('quantity[%d]' % oi.order_item_id, size=10, value=h.money(oi.quantity), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">${h.money(oi.total())}</td>
            % endif
          </tr>
          % endfor
          % for d in c.order.discounts:
          <tr>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td width="40%">Discount: ${d.note}</td>
              <td></td>
              <td></td>
              <td style="text-align:right;" >-$${h.money(d.amount)}</td>
          </tr>
          % endfor
          <tr>
            <td><img src="/public/images/icons/silk/add.png" border="0" onclick="customer_add_order_item(${c.order.order_id})"></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </div>
    </td>
  </tr>
</table>
<div class="align-right">
  ${h.button('cancel', 'Cancel', onclick='customer_show_orders()', class_="form-button")}
  ${h.button('save', 'Save Order', onclick='customer_edit_order_submit()', class_="form-button")}
</div>
</form>


<!-- KB: [2012-01-15]: Render the plugins, but only if they care about this order somehow. -->
% for plugin_name in plugin_registry:
  % if plugin_registry[plugin_name].can_edit_order(c.order) > 0:
    <hr>
    <p>
    ${plugin_registry[plugin_name].render_edit_order(c.order)}
    </p>
  % endif
% endfor


<script>
  var oi_ids = [
  % for oi in c.order.active_items:
  ${oi.order_item_id},
  % endfor
  -1
  ];
</script>
