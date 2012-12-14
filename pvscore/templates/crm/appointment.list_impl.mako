% if appointments:
<div id="result_list">
  <table class="results table table-striped">
    % for a in appointments:
      % if a.customer_id:
      <tr style="${'background-color:%s' % a.customer.phase.color if a.customer.phase else ''}">
        <td nowrap>${h.link_to(a.title, '/crm/appointment/edit_for_customer/%s/%s' % (a.customer_id, a.appointment_id))}</td>
        <td nowrap>${h.link_to(a.customer.email, '/crm/customer/edit/%s' % a.customer_id)}</td>
      % else:
      <tr>
        <td nowrap>${h.link_to(a.title, '/crm/appointment/edit/%s' % a.appointment_id)}</td>
        <td nowrap>&nbsp;</td>
      % endif
        <td nowrap>${h.slash_date(a.start_dt)} @ ${a.start_time}</td>
      </tr>
    % endfor
  </table>
</div>
% endif
