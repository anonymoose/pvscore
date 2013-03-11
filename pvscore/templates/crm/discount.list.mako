
<%inherit file="product.base.mako"/>\



<h1>Discount List</h1>

% if discounts:
<div id="result_list">
  <table class="results sortable table table-striped">
    <thead>
      <tr>
        <th>Name</th>
        <th>Code</th>
        <th nowrap>$ Off</th>
        <th nowrap>% Off</th>
        <th nowrap>Start Dt</th>
        <th nowrap>End Dt</th>
      </tr>
    </thead>
    <tbody>
      % for d in discounts:
      <tr>
        <td nowrap><a href="/crm/discount/edit/${d.discount_id}">${d.name}</a></td>
        <td>${d.code}</td>
        <td class="rt" nowrap>${h.money(d.percent_off)}</td>
        <td class="rt" nowrap>${h.money(d.amount_off)}</td>
        <td nowrap>${d.start_dt}</td>
        <td nowrap>${d.end_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

