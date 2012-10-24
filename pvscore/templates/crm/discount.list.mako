
<%inherit file="product.base.mako"/>\



<h1>Discount List</h1>

% if hasattr(c, 'discounts'):
<div id="result_list">
  <table width="100%" class="sortable">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th nowrap>$ Off</th>
        <th nowrap>% Off</th>
        <th nowrap>Start Dt</th>
        <th nowrap>End Dt</th>
      </tr>
    </thead>
    % for d in c.discounts:
    <tr>
      <td>${d.discount_id}</td>
      <td nowrap>${h.link_to(d.name, '/crm/discount/edit/%s' % d.discount_id)}</td>
      <td nowrap>${d.name}</td>
      <td class="rt" nowrap>${h.money(d.percent_off)}</td>
      <td class="rt" nowrap>${h.money(d.amount_off)}</td>
      <td nowrap>${d.start_dt}</td>
      <td nowrap>${d.end_dt}</td>
    </tr>
    % endfor
  </table>
</div>
% endif




