<%!
import math
%>

<%inherit file="customer.edit.base.mako"/>\

<h1>Apply Payment to Order</h1>

<div class="container">
  <form id="frm_apply_payment" method="POST" action="/crm/customer/apply_payment/${customer.customer_id}/${order.order_id}">
    <input type="hidden" name="bill_cc_token" id="bill_cc_token" value=""/>
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
              ${h.select('pmt_method', 'Apply Balance' if pre_order_balance > 0 else 'Cash', payment_methods, onchange="customer_payment_method_change()")}
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

        % if enterprise.is_credit_card_enabled():
        <div class="well" id="credit_card_info" style="display:none;">
          <div class="row">
            <div class="span8">
              <div class="alert">
                <strong>Note:</strong> This will run the credit card at ${enterprise.billing_method} for $${h.nvl(h.money(total_due))}.  
                <p>
                If you are using a credit card machine, select "Credit Card (offline)" above.
                </p>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="span5">
              <label for="cc_owner">Name on Card</label>
              ${h.text('cc_owner', value='%s %s' % (customer.fname, customer.lname), autocomplete='off', class_="input-xxlarge")}
            </div>
          </div>
          <div class="row">
            <div class="span3">
              <label for="bill_cc_num">Credit Card Number</label>
              ${h.text('bill_cc_num', autocomplete='off', class_="secret")}
            </div>
            <div class="span3">
              <label for="ccsave_expiration">Expiration Month</label>
              <select class="month validate-cc-exp required-entry"
                      name="bill_exp_month" id="bill_exp_month" autocomplete="off">
                <option selected="selected" value="">Month</option>
                <option value="01">January</option>
                <option value="02">February</option>
                <option value="03">March</option>
                <option value="04">April</option>
                <option value="05">May</option>
                <option value="06">June</option>
                <option value="07">July</option>
                <option value="08">August</option>
                <option value="09">September</option>
                <option value="10">October</option>
                <option value="11">November</option>
                <option value="12">December</option>
              </select>
            </div>
            <div class="span2">
              <label>Expiration Year</label>
              <select class="year required-entry" name="bill_exp_year" id="bill_exp_year" autocomplete="off">
                <option selected="selected" value="">Year</option>
                % for y in range(h.this_year(), h.this_year() + 10):
                % if y == h.this_year() + 1:
                <option value="${str(y)[2:]}" selected>${y}</option>
                % else:
                <option value="${str(y)[2:]}">${y}</option>
                % endif
                % endfor
              </select>
            </div>
          </div>
          <div class="row">
            <div class="span3">
              <label>Card Verification Number</label>
              ${h.text('bill_cc_cvv', autocomplete='off', class_="secret")}
            </div>
          </div>
        </div>
        % endif

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
      <div class="span3">
        <span id="payment-errors" style="color:red;"></span>
      </div>
    </div>
    <div class="row">
      <div class="span3 offset6">
        <a href="#" class="btn btn-primary btn-large" data-loading-text="Loading..." onclick="customer_apply_payment_submit()">Save</a>
        <a href="/crm/customer/edit_order_dialog/${customer.customer_id}/${order.order_id}" class="btn btn-link btn-large">Cancel</a>
      </div>
    </div>
  </form>
</div>
