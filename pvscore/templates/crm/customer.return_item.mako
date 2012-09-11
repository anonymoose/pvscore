
<%inherit file="customer.edit.base.mako"/>\

<h1>Return <i><b>${order_item.product.name}</b></i></h1>

<div class="container">  
  <form id="frm_return_item" method="POST" action="/crm/customer/return_item/${customer.customer_id}/${order.order_id}/${order_item.order_item_id}">
    <input type="hidden" name="original_quantity" id="original_quantity" value="${order_item.quantity}">
    <input type="hidden" name="original_total" id="original_total" value="${order_item.total()}">
    <input type="hidden" name="original_unit_price" id="original_unit_price" value="${order_item.unit_price}">
    <div class="row">
      <div class="span9">
        <div class="well">
          <div class="row">
            <div class="span3">
              <label>Quantity Returned</label>
              ${h.text('quantity_returned', class_="input-small", value=order_item.quantity, onblur="customer_check_return_quantity()")}
            </div>
            <div class="span3">
              <label>Credit Amount</label>
              $${h.text('credit_amount', class_="input-small", value=h.money(order_item.total()), onblur="customer_check_return_credit()")}
            </div>
            <div class="span2">
              <label class="radio">
                <input type="radio" name="rt_refund_type" id="rt_creditincrease" checked="checked" value="CreditIncrease"/>
                Store Credit
              </label>
              <label class="radio">
                <input type="radio" name="rt_refund_type" id="rt_refund" value="Refund"/>
                Refund
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="span3 offset6">
        <button type="submit" name="btn_return" id="btn_return" class="btn btn-primary btn-large" autocomplete="off" data-loading-text="loading...">Return</button>
        <a href="/crm/customer/edit_order_dialog/${customer.customer_id}/${order.order_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>
