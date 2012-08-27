
<%inherit file="customer.base.mako"/>\

<table>
  <tr valign="top">
    <td>
      <div id="Confirm">
        <p>Why are you canceling this order?</p>
      </div>
    </td>
  <tr>
  </tr>
    <td>
      ${h.textarea('cancel_reason', style="width: 250px; height: 100px;")}
    </td>
  </tr>
</table>

