<%inherit file="base.mako"/>\

${next.body()}

<%def name="left_col()">
  <div class="well sidebar-nav">
    <ul class="nav nav-list">
      <li><a href="/crm/product/list">List All Products</a></li>
      % if request.ctx.user.priv.edit_product:
      <li><a href="/crm/product/new">Add New Product</a> </li>
      % endif
      <li><a href="/crm/product/show_inventory">Edit Inventory</a>
      <li><hr></li>
      % if request.ctx.user.priv.edit_category:
      <li><a href="/crm/product/category/new">Add Product Category</a></li>
      <li><a href="/crm/product/category/list">List Product Categories</a> </li>
      % endif
      <li><hr></li>
      % if request.ctx.user.priv.edit_discount:
      <li><a href="/crm/discount/new">New Discount</a> </li>
      <li><a href="/crm/discount/list">List Discounts</a> </li>
      % endif
      <li>
        <form id="frm_product_search" class="form-inline">
          <input name="product_search" type="text"
                 placeholder="Product Search" 
                 id="product_search" data-provide="typeahead" data-source="[]" maxlength="30" autocomplete="off"/>
        </form>
      </li>
    </ul>
  </div>
</%def>


<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>


