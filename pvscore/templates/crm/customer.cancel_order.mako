
<%inherit file="customer.edit.base.mako"/>\

<h1>Cancel Order from <i><b>${h.slash_date(order.create_dt)}</i></b></h1>

<div class="container">  
  <form id="frm_cancel" method="POST" action="/crm/customer/cancel_order/${customer.customer_id}/${order.order_id}">
    <div class="row">
      <div class="span9">
        <div class="well">
          <div class="row">
            <div class="span8">
              <label for="cancel_reason">Why are you cancelling this order?</label>
              ${h.textarea('cancel_reason', style="width:800px;")}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="span3 offset6">
        <button type="submit" id="btn_cancel" name="btn_cancel" class="btn btn-primary btn-large" autocomplete="off" data-loading-text="loading...">Cancel Order</button>
        <a href="/crm/customer/show_orders/${customer.customer_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>
