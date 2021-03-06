
<%inherit file="product.base.mako"/>\

<h1>Product List</h1>

% if products:
<div id="result_list">
  <table class="results sortable table table-striped">
    <thead>
      <tr>
        <td>&nbsp;</td>
        <td>Categories</td>
        <td>Sku</td>
        <td>Retail</td>

        <td>Web?</td>
        <td>Image?</td>
        <td>Descr?</td>
      </tr>
    </thead>
    <tbody>
      % for p in products:
      <tr>
        <td nowrap>${h.link_to(p.name, '/crm/product/edit/%s' % p.product_id)}</td>
        <td>
          % for i, cat in enumerate(p.categories):
            ${',' if i > 0 else ''} ${cat.name}
          % endfor
        </td>
        <td nowrap>${p.sku}</td>
        <td class="rt" nowrap>${h.money(p.get_max_retail_price())}</td>

        <td class="rt" >${'Y' if p.web_visible else ''}</td>
        <td class="rt" >${'Y' if p.primary_image else ''}</td>
        <td class="rt" >${'Y' if p.detail_description else ''}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif


