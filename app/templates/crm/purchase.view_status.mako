
<%inherit file="purchase.base.mako"/>\

<form id="frm_status"> 
  <table>
    <tr valign="top">
      <td>
        <table>
          <tr><td>Event</td><td><b>${c.status.event.display_name}</b><td></tr>
          <tr><td>Type</td><td>${c.status.fk_type}<td></tr>
          <tr><td>Create Dt</td><td>${c.status.create_dt}<td></tr>
          <tr><td>Created By</td><td>${c.status.username}<td></tr>
          <tr colspan="2"><td>&nbsp;</td></tr>
          <tr valign="top">
            <td>Note</td><td>${h.literal(c.status.note)}</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>



