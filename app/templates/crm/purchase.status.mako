
<%inherit file="purchase.base.mako"/>\

<form id="frm_status"> 
  ${h.hidden('purchase_id', value=c.purchase.purchase_id)}
  <table>
    <tr valign="top">
      <td>
        <table>
          <tr><td>Event</td><td>${h.select('event_id', None, c.events)}<td></tr>
          <tr valign="top">
            <td>Note</td><td>${h.textarea('note', rows=10, style="width: 500px;", class_='content_editor')}</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>



