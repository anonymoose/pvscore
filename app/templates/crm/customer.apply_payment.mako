
<%inherit file="customer.base.mako"/>\

<%
total_applied = c.order.total_payments_applied()
total_discounts = c.order.total_discounts_applied()
total_due = c.order.total_payments_due()
pre_order_balance = c.customer.get_current_balance()+total_due
%>

<form id="frm_apply_payment">
    <input type="hidden" name="pmt_customer_id" id="customer_id" value="${c.customer.customer_id}">
    <input type="hidden" name="pmg_order_id" id="order_id" value="${c.order.order_id}">
    <input type="hidden" id="total_price" value="${c.order.total_price()}">
    <input type="hidden" id="total_due" value="${total_due}">
    <input type="hidden" id="total_applied" value="${total_applied}">
    <input type="hidden" name="pmt_type" value="${'FullPayment' if not c.discount else 'Discount'}">
    <table width="100%">
      <tr>
        <td>Total Order Price</td>
        <td align="right">$${h.money(c.order.total_price())}</td>
        <td>&nbsp;</td>
      </tr>
      % if not c.discount:
        <tr>
          <td>Total Payments Applied</td>
          <td align="right">-$${h.money(total_applied)}</td>
          <td>&nbsp;</td>
        </tr>
      % else:
        <tr>
          <td>Total Discounts Applied</td>
          <td align="right">$${h.money(total_discounts)}</td>
          <td>&nbsp;</td>
        </tr>
      % endif
      <tr>
        <td></td>
        <td><hr/></td>
        <td></td>
      </tr>
      <tr>
        <td>Total Amount Due</td>
        <td align="right">$${h.money(total_due)}</td>
        <td>&nbsp;</td>
      </tr>
      % if pre_order_balance > 0 and pre_order_balance != total_due:
        <tr>
          <td>Current Customer Balance</td>
          <td align="right">-$${h.money(pre_order_balance)}</td>
          <td>
            <input type="hidden" name="pre_order_balance" id="pre_order_balance" value="${pre_order_balance}"/>
          </td>
        </tr>
        <tr>
          <td></td>
          <td><hr/></td>
          <td></td>
        </tr>
        <tr>
          % if not c.discount:
            <td>Amount</td>
            <td align="right">${h.text('pmt_amount', size=10, value=h.money(total_due-pre_order_balance), onblur="customer_check_payment_amount()")}</td>
          % else:
            <td>Discount Amount</td>
            <td align="right">-${h.text('pmt_amount', size=10, value='0.00')}</td>
          % endif
          <td>&nbsp;</td>
        </tr>
      % else:
        <tr>
          <td></td>
          <td><hr/></td>
          <td></td>
        </tr>
        <tr>
          % if not c.discount:
            <td>Amount</td>
            <td align="right">${h.text('pmt_amount', size=10, value=h.money(total_due), onblur="customer_check_payment_amount()")}</td>
          % else:
            <td>Discount Amount</td>
            <td align="right">-${h.text('pmt_amount', size=10, value='0.00')}</td>
          % endif
          <td>
            <input type="hidden" name="pre_order_balance" id="pre_order_balance" value="0"/>
          </td>
        </tr>
        % if not c.discount:
          <tr><td>&nbsp;</td><td></td><td></td></tr>
          <tr>
            <td>Payment Method</td>
            <td align="right">${h.select('pmt_method', 'Credit Card', c.payment_methods)}</td>
            <td> </td>
          </tr>
        % endif
      % endif
      <tr>
        <td>Note</td>
        <td align="right">${h.text('pmt_note', size=50)}</td>
        <td>&nbsp;</td>
      </tr>
    </table>
</form>
