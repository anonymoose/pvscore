
<%inherit file="product.edit.base.mako"/>\

<h3>Product Event History</h3>

<div id="result_list">
  <table width="100%">
    <tr>
      <td>&nbsp;</td>
      <th nowrap>What Happened</th>
      <th>Created</th>
      <th>User</th>
      <th>Note</th>
    </tr>
    % for s in history:
    <tr>
      <td><img src="/static/icons/silk/page_edit.png" border="0" onclick="product_show_status(${s.status_id})"></td>
      <td nowrap>${s.fk_type} ${s.event.display_name}</td>
      <td nowrap>${h.date_time(s.create_dt)}</td>
      <td>${s.username}</td>
      <td>${h.literal(s.note[0:60]+'...') if s.note else ''}</td>
    </tr>
    % endfor
  </table>
</div>

