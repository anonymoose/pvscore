
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
          % for b in billings:
          <tr>
            <td>
              <a data-toggle="modal" data-target="#dlg_simple"
                 href="/crm/customer/show_billing_dialog/${customer.customer_id}/${b.journal_id}?dialog=1">
                <img src="/static/icons/silk/page_edit.png" border="0">
              </a>
            </td>
            <td>
              <img src="/static/icons/silk/delete.png" border="0" 
                   title="Delete Billing" alt="Delete Billing" onclick="customer_cancel_billing('${b.journal_id}')"/>
            </td>
            <td nowrap>${b.type}</td>
            <td nowrap>${b.create_dt}</td>
            <td>${b.creator.email if b.creator else 'Customer'}</td>
            <td align="left">${h.money(b.amount)}</td>
            <td><a href="/crm/customer/edit_order_dialog/${b.customer_id}/${b.order_id}">order</a></td>
            <td>${b.note[0:60]+'...' if b.note else ''}</td>
          </tr>
          % endfor
        </table>
        <ui class="pager">
          <li class="previous">
            % if offset > 0:
            <a href="/crm/customer/show_billings/${customer.customer_id}?offset=${offset-25}">&larr; prev</a> <!-- " -->
            % endif
          </li>
          <li class="next">
            <a href="/crm/customer/show_billings/${customer.customer_id}?offset=${offset+25}">next &rarr;</a>
          </li>
      </div>
    </div>
  </div>
</div>

