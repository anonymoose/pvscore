
<%inherit file="customer.edit.base.mako"/>\



<h1>Customer Billing Activity</h1>
<div class="container">
  <div class="row">
    <div class="span9">
      <div id="result_list">
        <table width="100%" class="sortable results table table-striped">
          <thead>
            <tr>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <th>Type</th>
              <th>Created</th>
              <th>User</th>
              <th>Amount</th>
              <th nowrap>Order ID</th>
              <th>Note</th>
            </tr>
          </thead>
          % for b in billings[offset:offset+50]:
          <tr>
            <td><img src="/static/icons/silk/page_edit.png" border="0" onclick="customer_show_billing(${b.journal_id})"></td>
            <td>
              <img src="/static/icons/silk/delete.png" border="0" title="Delete Billing" alt="Delete Billing" onclick="customer_cancel_billing(${b.journal_id})">
            </td>
            <td nowrap>${b.type}</td>
            <td nowrap>${b.create_dt}</td>
            <td>${b.user_created}</td>
            <td align="left">${h.money(b.amount)}</td>
            <td>${b.order_id}</td>
            <td>${b.note[0:60]+'...' if b.note else ''}</td>
          </tr>
          % endfor
        </table>
        <ui class="pager">
          <li class="previous">
            <a href="javascript:customer_show_billing(${offset-50 if offset > 0 else 0})">&larr; prev</a>
          </li>
          <li class="next">
            <a href="javascript:customer_show_billing(${offset+50})">next &rarr;</a>
          </li>
      </div>
    </div>
  </div>
</div>

