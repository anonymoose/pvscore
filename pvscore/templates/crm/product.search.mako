
<%inherit file="product.base.mako"/>\

<%
from pylons.controllers.util import redirect
c.name = (c.name if hasattr(c, 'name') else '')
c.description = (c.description if hasattr(c, 'description') else '')
c.company_id = (c.company_id if hasattr(c, 'company_id') else '')
c.sku = (c.sku if hasattr(c, 'sku') else '')

if hasattr(c, 'products') and len(c.products) == 1:
   redirect('/crm/product/edit/%s' % c.products[0].product_id)

%>

<h1>Product Search</h1>
<strong>Use full or partial matching on any/all fields to find products.  Values are combined to narrow results.</strong>

<hr>

<div id="frm_product_search"> 
  ${h.secure_form(h.url('/crm/product/search'))}
  <table>
    <div class="_50">
      <label for="name">Name</label>
      ${h.text('name', size=50, value=c.name)}
    </div>
    <div class="_50">
      <label for="description">Description</label>
      ${h.text('description', size=50, value=c.description)}
    </div>
    <div class="_50">
      <label for="sku">Sku</label>
      ${h.text('sku', size=50, value=c.sku)}
    </div>
    <div class="_50">
      <label for="company_id">Company</label>
      ${h.select('company_id', None, c.companies)}
    </div>
    <div class="align-right">
      ${h.submit('search', 'Search', class_="form-button")}
    </div>
  </table>
  ${h.end_form()}
</div>


% if hasattr(c, 'products'):
<div id="result_list">
  <table class="results sortable">
    % for p in c.products:
    <tr>
      <td nowrap>${h.link_to(p.name, '/crm/product/edit/%d' % p.product_id)}</td>
      <td>${p.sku}</td>
      <td nowrap>${p.create_dt}</td>
    </tr>
    % endfor
  </table>
</div>
% endif

