
<%inherit file="customer.edit.base.mako"/>\

<h3>Customer History</h3>

      <div id="result_list">
        <table width="100%" class="sortable results table-striped">
          <thead>
          <tr>
            <td>&nbsp;</td>
            <th>What Happened</th>
            <th>Created</th>
            <th>User</th>
            <th>Note</th>
          </tr>
          </thead>
        % for s in history[offset:offset+50]:
          <tr>
            <td><img src="/public/images/icons/silk/page_edit.png" border="0" onclick="customer_show_status(${s.status_id})"></td>
            <td nowrap>${s.fk_type} ${s.event.display_name}</td>
            <td nowrap>${s.create_dt}</td>
            <td>${s.username[:11]+'...' if s.username and len(s.username)>11 else s.username}</td>
            <td>${s.note[0:60]+'...' if s.note else ''}</td>
          </tr>
        % endfor
          <tr>
            <td>&nbsp;</td>
            <td nowrap><a href="javascript:customer_show_history(${offset-50 if offset > 0 else 0})">&lt;&lt; prev</a>&nbsp;&nbsp;
            <a href="javascript:customer_show_history(${offset+50})">next &gt;&gt;</a></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </div>

