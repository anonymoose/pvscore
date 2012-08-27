
<%inherit file="customer.base.mako"/>\

<form id="frm_return_item">
    <input type="hidden" name="original_quantity" id="original_quantity" value="${c.order_item.quantity}">
    <input type="hidden" name="original_total" id="original_total" value="${c.order_item.total()}">
    <input type="hidden" name="original_unit_price" id="original_unit_price" value="${c.order_item.unit_price}">
    <table width="100%">
      <tr>
        <td>Original Price</td>
        <td align="right">$${h.money(c.order_item.unit_price)}</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>Original Quantity</td>
        <td align="right">${h.money(c.order_item.quantity)}</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>Quantity Returned</td>
        <td align="right">${h.text('quantity_returned', size=10, value=c.order_item.quantity, onblur="customer_check_return_quantity()")}</td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>Credit Amount</td>
        <td align="right">${h.text('credit_amount', size=10, value=h.money(c.order_item.total()), onblur="customer_check_return_credit()")}</td>
        <td>&nbsp;</td>
      </tr>
      <tr><td colspan="3">&nbsp;</td></tr>
      <tr>
        <td>Return Type</td>
        <td nowrap>
          <label><input type="radio" name="rt_refund" id="rt_refund" 
                        onclick='$("#rt_refund").val("T"); $("#rt_refund").attr("checked", "checked"); $("#rt_creditincrease").val(""); $("#rt_creditincrease").attr("checked", "");'>Refund</label>&nbsp;
          <label><input type="radio" name="rt_creditincrease" id="rt_creditincrease" checked="checked"
                        onclick='$("#rt_creditincrease").val("T"); $("#rt_creditincrease").attr("checked", "checked"); $("#rt_refund").val(""); $("#rt_refund").attr("checked", "");'>Store Credit</label>
        <td nowrap></td></td>
      </tr>
      <tr><td colspan="3">&nbsp;</td></tr>
      <tr>
        <td>&nbsp;</td>
        <td nowrap>${h.checkbox('update_inventory', checked=True, value=1, label='Update Inventory?')}</td></td>
        <td>&nbsp;</td>
      </tr>
    </table>
</form>
