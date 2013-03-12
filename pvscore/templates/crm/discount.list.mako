
<%inherit file="product.base.mako"/>\



<h1>Discount List</h1>

% if discounts:
<div id="result_list">
  <table class="results sortable table table-striped">
    <thead>
      <tr>
        <th>Name</th>
        <th>Code</th>
        <th>Type</th>
        <th nowrap>% Off</th>
        <th nowrap>Shipping % Off</th>
        <th nowrap>Start Dt</th>
        <th nowrap>End Dt</th>
      </tr>
    </thead>
    <tbody>
      % for d in discounts:
      <tr>
        <td nowrap><a href="/crm/discount/edit/${d.discount_id}">${d.name}</a></td>
        <td>${d.code}</td>
        <td>${'CART' if d.cart_discount else 'PRODUCT'}</td>
        <td class="rt" nowrap>${'%s%%' % h.money(d.percent_off) if d.percent_off else ''}</td>
        <td class="rt" nowrap>${'%s%%' % h.money(d.shipping_percent_off) if d.shipping_percent_off else ''}</td>
        <td nowrap>${d.start_dt}</td>
        <td nowrap>${d.end_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

