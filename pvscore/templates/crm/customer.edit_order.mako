
<%inherit file="customer.edit.base.mako"/>\

% if customer.fname and customer.lname:
<h1>Finalize Order for <i><b>${customer.fname} ${customer.lname}</i></b></h1>
% else:
<h1>Finalize Order</h1>
% endif

<div class="container">
  <form id="frm_edit_order">
    <input type="hidden" id="oi_order_id" value="${order.order_id}">
    <input type="hidden" id="order_dirty" value="0">
    <input type="hidden" id="total_price" value="${h.money(total_price)}"/>

    <div class="row">
      <div class="span9">
        <div class="well">
          <div class="row">
            <div class="span3">
              <label for="">Shipping Total</label>
              ${h.text('shipping_total', class_="input-small", value=h.nvl(h.money(order.shipping_total),'0.00'), onblur='customer_order_recalc()')}
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
              <a href="javascript:customer_view_packing_slip('${order.order_id}', '${comm_packing_slip_id}')">View Receipt</a>
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
            <div class="span2">
              <label for="">Created by</label>
              ${order.user_created if order.user_created else 'Customer'}
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
            <th style="text-align:left;">Product</th>
            <th style="text-align:right;">Quantity</th>
            <th nowrap style="text-align:right;">Unit Price</th>
            <th nowrap style="text-align:right;">Sub Total</th>
          </thead>
          % for oi in order.active_items:
          <tr id="oi_${oi.order_item_id}">
            % if total_payments_applied > 0:
              <td>
                <img src="/static/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                     onclick="customer_delete_order_item('${oi.order_item_id}')"  class="img_delete"
                     style="visibility:hidden;">
              </td>
              <td>
                <a data-toggle="modal" data-target="#dlg_standard"
                   href="/crm/customer/status_dialog/${customer.customer_id}?order_item_id=${oi.order_item_id}&dialog=1">
                  <img src="/static/icons/silk/comment_add.png" 
                       border="0" title="Status Order" alt="Status Order" onclick="$('#dlg_standard_title').html('Status')"/>
                </a>
              </td>
              <td><a href="/crm/customer/return_item_dialog/${customer.customer_id}/${oi.order_id}/${oi.order_item_id}"><img src="/static/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0"/></td>
              <td width="40%">${oi.product.name}</td>
              <td style="text-align:right;" >${h.text('quantity[%s]' % oi.order_item_id, class_="input-small", value=h.money(oi.quantity), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;">$${h.text('unit_price[%s]' % oi.order_item_id, class_="input-small", value=h.money(oi.unit_price), onblur='customer_order_recalc()', disabled=True)}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">$${h.money(oi.total())}</td>
            % else:
              <td>
                <img src="/static/icons/silk/delete.png" title="Delete Item" alt="Delete Item" border="0" 
                     onclick="customer_delete_order_item('${oi.order_item_id}')"
                     class="img_delete">
              </td>
              <td>
                <a data-toggle="modal" data-target="#dlg_standard"
                   href="/crm/customer/status_dialog/${customer.customer_id}?order_item_id=${oi.order_item_id}&dialog=1">
                  <img src="/static/icons/silk/comment_add.png" 
                     border="0" title="Status Order" alt="Status Order"/>
                </a>
              </td>
              <td><a disabled="true" href="/crm/customer/return_item_dialog/${customer.customer_id}/${oi.order_id}/${oi.order_item_id}">
                  <img src="/static/icons/silk/arrow_refresh.png" title="Return Item" alt="Return Item" border="0" style="visibility:hidden;"/></td>
              <td width="40%">${oi.product.name}</td>
              <td style="text-align:right;" >${h.text('quantity[%s]' % oi.order_item_id, class_="input-small", value=h.money(oi.quantity), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;">$${h.text('unit_price[%s]' % oi.order_item_id, class_="input-small", value=h.money(oi.unit_price), onblur='customer_order_recalc()')}</td>
              <td style="text-align:right;" id="oi_total_${oi.order_item_id}">$${h.money(oi.total())}</td>
            % endif
          </tr>
          % endfor

          <tr id="oi_new">
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td width="40%">
                ${h.text('add_product_complete', class_="input-large", placeholder="Add New Product")}
              </td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
          </tr>

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
            <td>&nbsp;</td>
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
      <div class="offset5 span4">
        <dl class="dl-horizontal" style="text-overflow:clip;">
          <dt>Product Total</dt>
          <dd id="oi_total_price">$${h.money(total_price)}</dd>
          <dt>Shipping Total</dt>
          <dd id="oi_shipping_total">$${h.nvl(h.money(order.shipping_total),'0.00')}</dd>
          <dt>Payments Applied</dt>
          <dd id="oi_payments_applied">$${h.nvl(h.money(total_payments_applied), '0.00')}</dd>
          <dt>Discounts Applied</dt>
          <dd id="oi_discounts_applied">$${h.nvl(h.money(total_discounts_applied), '0.00')}</dd>
          <dt>&nbsp;</dt>
          <dd><hr/></dd>
          <dt>Remaining Balance</dt>
          <dd id="oi_total_due">$${h.nvl(h.money(total_due))}</dd>
        </dl>
      </div>
    </div>

    <div class="row">
      <div class="span3 offset6">
        % if order.order_id and total_payments_applied < total_price:
           <a href="#" id="btn_pay" class="btn btn-success btn-large" data-loading-text="loading..." onclick="customer_edit_order_submit()">Pay</a>
        % else:
           <a href="#" id="btn_pay" class="hidden btn btn-success btn-large" data-loading-text="loading..." onclick="customer_edit_order_submit()">Pay</a>
        % endif
        <a href="/crm/customer/show_orders/${customer.customer_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>


<script>
  var oi_ids = [
  % for oi in order.active_items:
  '${oi.order_item_id}',
  % endfor
  -1
  ];
</script>


