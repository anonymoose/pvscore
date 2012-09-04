<%!
import math
%>

<%inherit file="customer.edit.base.mako"/>\

<h1>Apply Payment to Order</h1>

<div class="container">
  <form id="frm_apply_payment" method="POST" action="/crm/customer/apply_payment/${customer.customer_id}/${order.order_id}">
    <div class="row">
      <div class="span9">
        <div class="well">
          <div class="row">
            <div class="span3">
              <label for="">Payment Amount</label>
              ${h.text('pmt_amount', class_="input-small", value=h.money(total_due), onblur="customer_check_payment_amount()")}
              % if pre_order_balance > 0:
              <span class="label label-info">from balance</span>
              % endif
            </div>
            <div class="span3">
              <label for="">Payment Method</label>
              ${h.select('pmt_method', 'Apply Balance' if pre_order_balance > 0 else 'Credit Card', payment_methods)}
            </div>
          </div>
          <div class="row">
            <div class="span5">
              <label for="">Note</label>
              ${h.text('pmt_note', class_="input-xxlarge")}
            </div>
          </div>
        </div><!-- well -->

        <h3>Total Due</h3>
        <div class="well">
          <div class="row">
            <div class="span3">
              <label for="">Total Order Price</label>
              ${h.text('total_price', class_="input-small", value=h.money(order.total_price()), disabled=True)}
            </div>
            <div class="span3">
              <label for="">Total Amount Due</label>
              ${h.text('total_due', class_="input-small", value=h.money(total_due), disabled=True)}
            </div>
            <div class="span2">
              <label for="">Total Applied (Pmt+Disc)</label>
              ${h.text('total_applied', class_="input-small", value=h.money(-1*(total_applied-total_discounts)), disabled=True)}
            </div>
          </div>
        </div>
        % if pre_order_balance > 0:
        <h3>Customer Balance Info</h3>
        <div class="well">
          <div class="row">
            <div class="span3">
              <label for="">Current Customer Balance</label>
              ${h.text('pre_order_balance', class_="input-small", value=h.money(pre_order_balance), disabled=True)}
            </div>
            <div class="span3">
              <label for="">Customer Balance to Apply</label>
              ${h.text('pmt_balance_amount_to_apply', class_="input-small", value=h.money(min(pre_order_balance, total_due)), onblur="customer_check_payment_amount()")}
            </div>
            <div class="span2">
              <label for="">Balance Remaining</label>
              ${h.text('pmt_balance_after_purchase', class_="input-small", value=h.money((-1*pre_order_balance)-total_due), disabled=True)}
            </div>
          </div>
        </div>
        % endif
      </div>
    </div>
    <div class="row">
      <div class="span2 offset7">
        <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
        <a href="/crm/customer/edit_order_dialog/${customer.customer_id}/${order.order_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>
