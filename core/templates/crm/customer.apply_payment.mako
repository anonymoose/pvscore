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
          % if pre_order_balance > 0:
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
          % endif
          <div class="row">
            <div class="span5">
              <label for="">Note</label>
              ${h.text('pmt_note', class_="input-xxlarge")}
            </div>
          </div>
        </div><!-- well -->

        <div class="row">
          <div class="offset5 span4">
            <dl class="dl-horizontal" style="text-overflow:clip;">
              <dt>Product Total</dt>
              <dd id="oi_total_price">$${h.money(total_price)}</dd>
              <dt>Shipping Total</dt>
              <dd id="oi_shipping_total">$${h.money(order.shipping_total)}</dd>
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
