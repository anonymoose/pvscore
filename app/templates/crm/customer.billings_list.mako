
<%inherit file="customer.edit.base.mako"/>\



<h1>Customer Billing Activity</h1>

      <div id="result_list">
        <table width="100%" class="sortable results table-striped">
          <thead>
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <th>Type</th>
            <th>Created</th>
            <th>User</th>
            <th>Note</th>
            <th>Amount</th>
            <th nowrap>Order ID</th>
          </tr>
          </thead>
        % for b in billings[offset:offset+50]:
          <tr>
            <td><img src="/public/images/icons/silk/page_edit.png" border="0" onclick="customer_show_billing(${b.journal_id})"></td>
            <td>
              <img src="/public/images/icons/silk/delete.png" border="0" title="Delete Billing" alt="Delete Billing" onclick="customer_cancel_billing(${b.journal_id})">
            </td>
            <td nowrap>${b.type}</td>
            <td nowrap>${b.create_dt}</td>
            <td>${b.user_created}</td>
            <td>${b.note[0:60]+'...' if b.note else ''}</td>
            <td align="left">${h.money(b.amount)}</td>
            <td>${b.order_id}</td>
          </tr>
        % endfor
          <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td nowrap><a href="javascript:customer_show_billings(${offset-50 if offset > 0 else 0})">&lt;&lt; prev</a>&nbsp;&nbsp;
            <a href="javascript:customer_show_billings(${offset+50})">next &gt;&gt;</a></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </div>

