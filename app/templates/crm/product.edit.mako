
<%inherit file="product.edit.base.mako"/>\

<div id="div_product_edit">
  <div class="container">
    <form method="POST" action="/crm/product/save" id="frm_product">
      ${h.hidden('product_id', value=product.product_id)}

      <div class="row">
        <div class="span7">
          <h1>Edit Product&nbsp;&nbsp;<font color="green">${'Status: ' + product.status.event.display_name if product.status else ''}</font></h1>
        </div>
        <div class="span2 offset1">
          % if request.ctx.user.priv.edit_product:
          <input type="submit" name="submit1" class="btn btn-primary btn-small" value="Save"/>
          % endif
        </div>
      </div>
      
      <div class="row">
        <div class="span9">
          <div class="well">
            <h3>General Information</h3>    
            <div class="row">
              <div class="span3">
                <label for="name">Name</label>
                ${h.text('name', size=50, value=product.name)}
              </div>
              <div class="span3">
                % if len(product_categories) >= 1:
                <label for="category_id">Category</label>
                ${h.select('category_id', product_categories[0].category_id if len(product_categories) == 1 else None, categories)}
                % endif
              </div>
            </div> 
            
            <div class="row">
              <div class="span8">
                <label for="description">Simple Description</label>
                ${h.textarea('description', style="width: 100%; height: 70px;", content=product.description)}
              </div>
            </div> 
            <div class="row">
              <div class="span8">
                <label for="detail_description">Detailed Description</label>
                ${h.textarea('detail_description', style="width: 100%; height: 100px;", content=product.detail_description)}
              </div>
            </div>
            <div class="row">
              <div class="span7">
                <h3>Search Engine Keywords</h3>
                <div class="row">
                  <div class="span3">
                    <label for="seo_keywords">Keywords</label>
                    ${h.text('seo_keywords', class_="input-xlarge", value=product.seo_keywords)}
                  </div>
                  <div class="span4">
                    <label for="seo_title">Title</label>
                    ${h.text('seo_title', class_="input-xlarge", value=product.seo_title)}
                  </div>
                  <div class="span4">
                    <label for="seo_description">Description</label>
                    ${h.text('seo_description', class_="input-xlarge", value=product.seo_description)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span7">
                <h3>Details</h3>
                <div class="row">
                  <div class="span3">
                    <label for="company_id">Company</label>
                    ${h.select('company_id', product.company_id, companies)}
                  </div>
                  <div class="span3">
                    <label for="type">Product Type</label>
                    ${h.select('type', product.type, product_types)}
                  </div>
                </div>
                <div class="row">
                  <div class="span2">
                    <label for="unit_cost">Unit Cost</label>
                    ${h.text('unit_cost', class_="input-small", value=product.unit_cost)}
                  </div>
                  <div class="span2">
                    <label for="weight">Weight</label>
                    ${h.text('weight', class_="input-small", value=product.weight)}
                  </div>
                  <div class="span2">
                    <label for="handling_price">Handling Price</label>
                    ${h.text('handling_price', class_="input-small", value=product.handling_price)}
                  </div>
                </div>
              </div>
              <div class="span1">
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('subscription', checked=product.subscription, label=' Subscription?')} 
                  </div>
                </div>
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('enabled', checked=product.enabled, label=' Enabled?')}
                  </div>
                </div>
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('featured', checked=product.featured, label=' Featured?')}
                  </div>
                </div>
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('special', checked=product.special, label=' Special?')}
                  </div>
                </div>
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('web_visible', checked=product.web_visible, label=' Web Visible?')}
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="span7">
                <h3>Inventory</h3>
                <div class="row">
                  <div class="span2">
                    <label for="prod_inventory">Inventory Adjust</label>
                    ${h.text('prod_inventory', class_="input-small")}
                  </div>
                  <div class="span2">
                    <label for="inventory_par">Inventory Par</label>
                    ${h.text('inventory_par', class_="input-small", value=product.inventory_par)}
                  </div>
                  <div class="span3">
                    ${h.checkbox('show_negative_inventory', checked=product.show_negative_inventory, label=' Show When Negative Inventory?')}
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="span7">
                <div class="row">
                  <div class="span2">
                    <label for="sku">SKU</label>
                    ${h.text('sku', class_="input-small", value=product.sku)}
                  </div>
                  <div class="span2">
                    <label for="third_party_id">Third Party ID</label>
                    ${h.text('third_party_id', class_="input-small", value=product.third_party_id)}
                  </div>
                </div>      
              </div>              
            </div>
            <div class="row">
              <div class="span7">
                <h3>Supplier Information</h3>
                <div class="row">
                  <div class="span3">
                    <label for="manufacturer">Manufacturer</label>
                    ${h.text('manufacturer', size=50, value=product.manufacturer)}
                  </div>
                  % if not request.ctx.user.is_vendor_user():
                  <div class="span3">
                    <label for="vendor_id">Supplier</label>
                    ${h.select('vendor_id', product.vendor_id, vendors)}
                  </div>
                  % endif
                </div>
              </div>
            </div>            
          </div>
        </div>      
      </div>
      <div class="row">
        <div class="span9">
          <div class="row">
            <div class="span3">
              <h3>Product Attributes</h3>
              <div style="overflow: scroll; height: 400px;">
                <table>
                  <%
                     attrs = product.get_attrs()
                     idx = 0
                     %>
                  % for attr_name in attrs:
                  <tr>
                    <td>${h.text('attr_name[%d]' % idx, class_="input-small", value=attr_name)}</td>
                    <td>${h.text('attr_value[%d]' % idx, class_="input-small", value=attrs[attr_name])}</td>
                  </tr>
                  <% idx = idx + 1 %>
                  % endfor
                  % for i in range(idx,30):
                  <tr>
                    <td>${h.text('attr_name[%d]' % i, class_="input-small")}</td><td>${h.text('attr_value[%d]' % i, class_="input-small")}</td>
                  </tr>
                  <% idx = idx + 1 %>
                  % endfor
                </table>
              </div>
            </div>
            <div class="span3" id="result_list">
              <h3>Product Pricing</h3>
              <table>
                <tr>
                  <th>Campaign</th>
                  <th>Price</th>
                  <th>Discount Price</th>
                </tr>
                % for cmp in campaigns:
                <tr>
                  <td nowrap>${cmp.name}</td>
                  <td>${h.text('campaign_price[%d]' % cmp.campaign_id, class_="input-small", value=h.money(cmp.get_product_retail_price(product)))}</td>
                  <td>${h.text('campaign_discount[%d]' % cmp.campaign_id, class_="input-small", value=h.money(cmp.get_product_discount_price(product)))}</td>
                </tr>
                % endfor
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="span9">
          <div class="row">
            <div class="span4">
              % if product.can_have_children() and other_products and not request.ctx.user.is_vendor_user():
              <h3>Child Products</h3>
              <div style="overflow: scroll; height: 400px;">
                <table>
                  <tr><th></th><th>Include?</th><th>Quantity</th></tr>
                  % for p in children:
                  <tr>
                    <td>${p.child.name}</td>
                    <td nowrap>${h.checkbox('child_incl_%d' % p.child.product_id, checked=True, value=p.child.product_id, class_='product_chk')}</td>
                    <td nowrap>${h.text('child_quantity_%d' % p.child.product_id, value=p.child_quantity, class_="input-small")}</td>
                  </tr>
                  % endfor
                  
                  % for p in non_children:
                  <tr>
                    <td>${p.name}</td>
                    <td nowrap>${h.checkbox('child_incl_%d' % p.product_id, value=p.product_id, class_='product_chk')}</td>
                    <td nowrap>${h.text('child_quantity_%d' % p.product_id, class_="input-small")}</td>
                  </tr>
                  % endfor
                </table>
              </div>
              % endif
            </div>
            <div class="span3">
              <h3>Product Creation Details</h3>
              % if product.product_id:
              <table>
                <tr><td>Create Date</td><td>${h.nvl(product.create_dt)}</td></tr>
                <tr><td>Mod Date</td><td>${h.nvl(product.mod_dt)}</td></tr>
                <tr><td>Delete Date</td><td>${h.nvl(product.delete_dt)}</td></tr>
              </table>
              % endif
            </div>
            <div class="span2 offset7">
              % if request.ctx.user.priv.edit_product:
              <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
              % endif
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>


<%def name="other_foot()">\
<script>
/* KB: [2011-08-20]: You can't do this onload.  Not sure why, but this mimics the script block at the end of the page. */
product_setup_textarea();
</script>
</%def>
