
<%inherit file="customer.edit.base.mako"/>\

<h1>Order List</h1>

<div id="result_list">
  <table width="100%" class="results sortable table table-hover">
    <thead>
      <tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <th>Total</th>
        <th>Due</th>
        <th>Created</th>
        <th>User</th>
        <th nowrap>Status</th>
      </tr>
    </thead>
    % if not len(orders):
    <tr>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      <td style="width:200px;" colspan="5">No Orders Yet.</td>
    </tr>
    % endif
    % for o in orders:
    <%
       due = o.total_payments_due()
       %>
    <tr order_id="${o.order_id}" style="cursor:pointer;">
      % if request.ctx.user.priv.modify_customer_order:
      <td>
        <img src="/static/icons/silk/page_edit.png" title="Edit Order (${o.order_id})" alt="Edit Order (${o.order_id})" border="0" onclick="customer_edit_order(${o.order_id})">
      </td>
      <td>
        <a data-toggle="modal" data-target="#dlg_standard"
           href="/crm/customer/status_dialog/${customer.customer_id}?order_id=${o.order_id}&dialog=1">
          <img src="/static/icons/silk/comment_add.png" 
               border="0" title="Status Order" alt="Status Order"/>
        </a>
      </td>
      <td>
        <a href="/crm/customer/cancel_order_dialog/${customer.customer_id}/${o.order_id}"><img src="/static/icons/silk/delete.png" border="0" title="Delete Order" alt="Delete Order")"></a>
      </td>
      % else:
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      % endif
      <td class="money clickable" nowrap>${h.money(o.total_price())}</td>
      <td class="money clickable" nowrap>
        % if due > 0.00:
        <font color="red"><b>${h.money(due)}</b></font>
        % else:
        ${h.money(due)}
        % endif
      </td>
      <td class="clickable" nowrap>${o.create_dt}</td>
      <td class="clickable">${o.user_created if o.user_created else ''}</td>
      % if o.status:
      <td nowrap><strong><font color="${o.status.event.color}"><a href="javascript:customer_show_status(${o.status.status_id})">${o.status.event.display_name}</a></font></strong></td>
      % else:
      <td>&nbsp;</td>
      % endif
    </tr>
    % if len(o.active_items) > 0:
    <tr class="detail_${o.order_id}" style="display:none;">
      <td colspan="4">&nbsp;</td>
      <td colspan="4">
        <table>
          <tr>
            <td><i>Product</i></td>
            <td><i>Ord</i></td>
            <td><i>Itm</i></td>
            <td><i>Price</i></td>
            <td><i>Quantity</i></td>
            <td nowrap><i>Sub Total</i></td>
          </tr>
          % for i,oi in enumerate(o.active_items):
          <tr>
            <td valign="top">
              <span>
                % if oi.parent_id:
                <img src="/static/corner-dots.gif" border="0" onclick="customer_cancel_order(${o.order_id})">
                % endif
                ${oi.product.name}
              </span>
            </td>
            <td>${oi.order_id}</td><td>${oi.order_item_id}</td>
            <td class="money"  valign="top">
              % if oi.parent_id:
              &nbsp;
              % else: 
              ${h.money(oi.unit_price)}
              % endif
            </td>
            <td class="money" valign="top">${oi.quantity}</td>
            <td class="money" valign="top">${h.money(oi.total())}</td>
          </tr>
          % endfor
        </table>
      </td>
    </tr>
    % endif
    % if o.shipping_total:
    <tr class="detail_${o.order_id}" style="display:none;">
      <td colspan="6">&nbsp;</td>
      <td nowrap>
        Shipping Total
      </td>
      <td>&nbsp;</td>
      <td class="money">&nbsp;</td>
      <td class="money">${h.money(o.shipping_total)}</td>
    </tr>
    % endif
    % endfor
  </table>
</div>

