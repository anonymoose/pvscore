
<%inherit file="/crm/base.mako"/>\

% if len(comms) > 0:
<table>
  <tr valign="top">
    <td>
      <label for="comm">Communication</label></td><td>${h.select('comm_id', None, comms)}<td></tr>
    </td>
  </tr>
<!--
  <tr valign="top">
    <td><label for="comm">Custom Msg</label></td><td>${h.textarea('message', rows=10, style="width: 500px;", class_='content_editor')}</td>
  </tr>
-->
</table>
% else:

No communications configured for users to send.
<script>
$('#btn_ok_dlg_standard').remove();
</script>

% endif
