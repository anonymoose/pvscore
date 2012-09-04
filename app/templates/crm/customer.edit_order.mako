
<%inherit file="customer.edit.base.mako"/>\

% if customer.fname and customer.lname:
<h1>Edit Order for <i><b>${customer.fname} ${customer.lname}</i></b></h1>
% else:
<h1>Edit Order</h1>
% endif

<style>
.dl-horizontal dt {
  width: 160px;
  margin-right: 10px;
}
</style>

<div class="container">
  <form id="frm_edit_order">
    <input type="hidden" id="oi_order_id" value="${order.order_id}">
    <input type="hidden" id="total_price" value="${total_price}">
    <input type="hidden" id="order_dirty" value="0">
    <div class="row">
      <div class="span9">
        <div class="well">
          <div class="row">
            <div class="span4">
              <dl class="dl-horizontal" style="text-overflow:clip;">
                <dt>Total</dt>
                <dd id="oi_total_price">$${h.money(total_price)}</dd>
                <dt>Payments Applied</dt>
                <dd id="oi_payments_applied">$${h.nvl(h.money(total_payments_applied), '0.00')}</dd>
                <dt>Discounts Applied</dt>
                <dd id="oi_discounts_applied">$${h.nvl(h.money(total_discounts_applied), '0.00')}</dd>
                <dt>Creator</dt>
                <dd>${order.user_created if order.user_created else 'Customer'}</dd>
              </dl>
            </div>
            <div class="span4">
              <div class="row" style="margin-top: 32px;">
                <div class="span3">
                % if order.order_id and total_payments_applied < total_price:
                  <a href="javascript:customer_order_apply_payment()"><h2>Pay</h2></a>
                % endif
                </div>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="span3">
              <label for="">Shipping Total</label>
              ${h.text('shipping_total', class_="input-small", value=h.money(order.shipping_total), onblur='customer_order_recalc()')}
            </div>
            % if comm_packing_slip_id:
            <div class="span2">
              % if order.shipping_note:
              <label for="">Shipping Note</label>
              ${order.shipping_note if order.shipping_note else ''}
              % endif
              &nbsp;
            </div>
            <div class="span2">
              <a href="javascript:customer_view_packing_slip(${order.order_id}, ${comm_packing_slip_id})">View Packing Slip</a>
            </div>
            % endif
            % if order.external_cart_id:
            <div class="span2">
              <label for="">External Cart ID</label>
              ${h.nvl(order.external_cart_id)}
            </div>
            % endif
          </div>

          <div class="row">
            <div class="span3">
              <label for="order_create_dt">Created Dt</label>
              ${h.text('order_create_dt', class_="input-small", value=order.create_dt)}
            </div>
          </div>

        </div> <!-- well -->
      </div>
    </div>

    <div class="row">
      <div class="span9">
        <table width="100%">
          <thead id="result_list_header">
            <th>&nbsp</td>
            <th>&nbsp</td>
            <th>&nbsp</td>
            <th>Product</th>
            <th nowrap>Unit Price</th>
            <th>Quantity</th>
            <th nowrap>Sub Total</th>
          </thead>
          % for oi in order.active_items:
          <tr id="oi_${oi.order_item_id}">
            % if total_payments_applied > 0:
              <td><img src="/static/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                       onclick="customer_delete_order_item('${oi.order_item_id}')"  class="img_delete"
                       style="display:none;">
              </td>
              <td>
                <img src="/static/icons/silk/comment_add.png" 
                     border="0" title="Status Order" alt="Status Order" 
                     onclick="customer_status_order_item(%{oi.order_id} ${oi.order_item_id})"/>
              </td>
              <td><img src="/static/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0" 
                       onclick="customer_return_order_item('${order.order_id}', '${oi.order_item_id}', ${oi.quantity}, ${oi.total()})" class="img_return"></td>
              <td width="40%">${oi.product.name}</td>
              <td>$${h.text('unit_price[%d]' % oi.order_item_id, class_="input-small", value=h.money(oi.unit_price), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;" >${h.text('quantity[%d]' % oi.order_item_id, class_="input-small", value=h.money(oi.quantity), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">$${h.money(oi.total())}</td>
            % else:
              <td><img src="/static/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                       onclick="customer_delete_order_item('${oi.order_item_id}')" class="img_delete"></td>
              <td>
                <img src="/static/icons/silk/comment_add.png" 
                     border="0" title="Status Order" alt="Status Order" 
                     onclick="customer_status_order_item(${oi.order_id}, ${oi.order_item_id})"/>
              </td>
              <td><img src="/static/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0" 
                       onclick="customer_return_order_item('${order.order_id}', '${oi.order_item_id}', ${oi.quantity}, ${oi.total()})" class="img_return"
                       style="display:none;"></td>
              <td width="40%">${oi.product.name}</td>
              <td>$${h.text('unit_price[%d]' % oi.order_item_id, class_="input-small", value=h.money(oi.unit_price), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;" >${h.text('quantity[%d]' % oi.order_item_id, class_="input-small", value=h.money(oi.quantity), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">$${h.money(oi.total())}</td>
            % endif
          </tr>
          % endfor
          % for d in order.discounts:
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
            <td><img src="/static/icons/silk/add.png" border="0" onclick="customer_add_order_item(${order.order_id})"></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </div>
    </div>

    <div class="row">
      <div class="span2 offset7">
        <a href="#" class="btn btn-primary btn-large" onclick="customer_edit_order_submit()">Save</a>
        <a href="/crm/customer/show_orders/${customer.customer_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>


<script>
  var oi_ids = [
  % for oi in order.active_items:
  ${oi.order_item_id},
  % endfor
  -1
  ];
</script>

