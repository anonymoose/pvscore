
<%inherit file="customer.base.mako"/>\

% if len(events) > 1:
<form id="frm_dialog" method="POST" action="/crm/customer/save_status/${customer.customer_id}"> 
  <input type="hidden" name="redir" value="${redir}"/>

  % if order_item:
  <input type="hidden" name="order_item_id" value="${order_item.order_item_id}"/>
  % elif order:
  <input type="hidden" name="order_id" value="${order.order_id}"/>
  % endif
  
  <table>
    <tr valign="top">
      <td>
        <table>
          <tr>
            <td>
              <label for="event_id">Event</label>
              ${h.select('event_id', None, events)}
            <td>
          </tr>
          <tr valign="top">
            <td>
              <label for="note">Note</label>
              ${h.textarea('note', rows=6, style="width: 510px;")}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>
% else:

No workflow events for this item.

<script>
$('#btn_ok_dlg_standard').remove();
</script>

% endif


