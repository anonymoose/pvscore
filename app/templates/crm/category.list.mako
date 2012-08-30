
<%inherit file="product.base.mako"/>\

<h1>Product Category List</h1>

% if categories:
<div id="result_list">
  <table class="results sortable table table-striped" width="100%">
    <thead>
      <tr>
        <td>ID</td>
        <td width="50%">Name</td>
        <td>Create Date</td>
      </tr>
    </thead>
    <tbody>
      % for pc in categories:
      <tr>
        <td>${pc.category_id}</td>
        <td width="50%" nowrap>${h.link_to(pc.name, '/crm/product/category/edit/%d' % pc.category_id)}</td>
        <td nowrap>${pc.create_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

