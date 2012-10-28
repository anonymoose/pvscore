
<%inherit file="product.base.mako"/>\

${next.body()}

<%def name="left_col()">
  <input type="hidden" id="product_menu_selected" value="${request.url.split('/')[5]}"/>
  <input type="hidden" id="product_id" value="${product.product_id}"/>
  <div class="well sidebar-nav">
    <ul class="nav nav-list">
      % if product.product_id:
      <li class="nav-header">${product.name}</li>
      <li id="edit">${h.link_to('Edit Product', '/crm/product/edit/%s' % product.product_id)}</li>
      <li><a href="#dlg_product_status" role="button" data-toggle="modal">Status</a></li>
      <li id="show_sales">${h.link_to('Sales', '/crm/product/show_sales/%s' % product.product_id)}</li>
      <li id="show_orders">${h.link_to('Orders', '/crm/product/show_orders/%s' % product.product_id)}</li>
      <li id="show_history">${h.link_to('History', '/crm/product/show_history/%s' % product.product_id)}</li>
      <li id="show_returns">${h.link_to('Returns', '/crm/product/show_returns/%s' % product.product_id)}</li>
      <li id="show_purchases">${h.link_to('Purchases', '/crm/product/show_purchases/%s' % product.product_id)}</li>
      <li><hr/></li>
      % endif
      <li><a href="/crm/product/list">List All Products</a></li>
      % if request.ctx.user.priv.edit_product:
      <li><a href="/crm/product/new">Add New Product</a> </li>
      % endif
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
  
  % if product.product_id:
  <div class="well sidebar-nav">
    <span><h3>Product Images</h3>&nbsp;&nbsp;<a href="javascript:product_picture_edit_image()">Add Image</a></span>
    <div id="product_images">
      % for img in product.images:
      <img id="pi_${img.id}" width="100"
           src="/cms/asset/show/${img.id}"
           onclick="product_picture_delete_image('${img.id}', true)"/>
      % endfor
    </div>
  </div>
  % endif
</%def>


<!-- Modals -->
<div class="modal hide fade" id="dlg_product_status">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    <h3>Product Status</h3>
  </div>
  <div class="modal-body">
    <form id="frm_status" action="/crm/product/save_status" method="POST"> 
      <input type="hidden" id="event_product_id" name="product_id" value="${product.product_id}"/>
      <div class="row">
        <div class="span5">
          <label for="event_id">Event</label>
          ${h.select('event_id', None, events)}
        </div>
      </div>
      <div class="row">
        <div class="span5">
          <label for="note">Note</label>
          ${h.textarea('note', rows=10, style="width: 100%; height: 100px;", class_='content_editor')}
        </div>
      </div>
    </form>
  </div>
  <div class="modal-footer">
    <button class="btn btn-primary" onclick="$('#frm_status').submit()">Save changes</button>
    <button class="btn btn-link" data-dismiss="modal" aria-hidden="true">Cancel</button>
  </div>
</div>

