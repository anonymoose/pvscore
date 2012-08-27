
<%inherit file="customer.base.mako"/>\

<form id="frm_status"> 
  ${h.hidden('customer_id', value=c.customer.customer_id)}

  <table>
    <tr valign="top">
      <td>
        <table>
          <tr><td><label for="event_id">Event</label></td><td>${h.select('event_id', None, c.events)}<td></tr>
          <tr valign="top">
            <td><label for="note">Note</label></td><td>${h.textarea('note', rows=10, style="width: 500px;", class_='content_editor')}</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>



