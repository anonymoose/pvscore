
<%inherit file="customer.edit.base.mako"/>\

<h3>Customer History</h3>

<div id="result_list">
  <div class="container">
    <div class="row">
      <div class="span9">
        <table width="100%" class="sortable results table table-striped table-condensed">
          <thead>
            <tr>
              <td>&nbsp;</td>
              <th>What Happened</th>
              <th>Created</th>
              <th>User</th>
              <th>Note</th>
            </tr>
          </thead>
          % for s in history:
          <tr>
            <td>
              <a data-toggle="modal" data-target="#dlg_simple"
                 href="/crm/customer/show_status_dialog/${customer.customer_id}/${s.status_id}?dialog=1">
                <img src="/static/icons/silk/page_edit.png" border="0"/>
              </a>
            </td>
            <td nowrap>${s.fk_type} ${s.event.display_name}</td>
            <td nowrap>${h.date_time(s.create_dt)}</td>
            <td>${s.user.email if s.username else ''}</td>
            <td>${s.note[0:60]+'...' if s.note else ''}</td>
          </tr>
          % endfor
        </table>
        <ul class="pager">
          <li class="previous">
            % if offset > 0:
            <a href="/crm/customer/show_history/${customer.customer_id}?offset=${offset-25}">&larr; prev</a> <!-- " -->
            % endif
          </li>
          <li class="next">
            <a href="/crm/customer/show_history/${customer.customer_id}?offset=${offset+25}">next &rarr;</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>

