
<%inherit file="product.edit.base.mako"/>\

<div id="div_product_edit">
  <div class="container">
    <form method="POST" action="/crm/product/save" autocomplete="off" id="frm_product">
      ${h.hidden('product_id', value=product.product_id)}
      % if parent_product:
          ${h.hidden('parent_id', value=request.GET.get('parent_id'))}
      % endif
      ${h.hidden('is_attribute', value=is_attribute)}
      <div class="row">
        <div class="span7">
          % if parent_product:
          <h1>Edit Attribute for <a href="/crm/product/edit/${parent_product.product_id}">${parent_product.name}</a></h1>
          % else:
          <h1>Edit Product&nbsp;&nbsp;<font color="green">${'Status: ' + product.status.event.display_name if product.status else ''}</font></h1>
          % endif
        </div>
        <div class="span3">
          % if request.ctx.user.priv.edit_product:
          <input type="submit" name="submit1" class="btn btn-primary" value="Save"/>
            % if parent_product:
            <a href="/crm/product/new?is_attribute=True&parent_id=${parent_product.product_id}">New Attribute</a>
            % endif
          % endif
        </div>
      </div>

      <div class="row">
        <div class="span9">
          <div class="well">
            <h3>General Information</h3>
            % if parent_product:
              <div class="row">
                <div class="span3">
                  <label for="attr_class">Attribute
                    ${h.help("""<b>Example:</b>  If the parent product was a 'Shirt' and this attribute concerns which 'Color' the shirt should be, 
                    you should create a product attribute with the Name = 'Blue' and the Attribute Class = 'Color'.
                    """)}
                  </label>
                  ${h.text('attr_class', class_="input-large", value=product.attr_class)}
                </div>
                <div class="span3">
                  <label for="name">Name
                    ${h.help("""The name of this instance of the attribute.  If the attribute is 'Color', then the name of this one might be 'Blue'.  Create another attribute for 'Red', etc.""")}
                  </label>
                  ${h.text('name', size=50, value=product.name)}
                </div>
              </div>
            % else:
              <div class="row">
                <div class="span3">
                  <label for="name">Name
                    ${h.help("""The name of the product to be displayed on the website and in product lists.<br/>This title is used in links as well to improve search engine placement. """)}
                  </label>
                  ${h.text('name', size=50, value=product.name)}
                </div>
                <div class="span3">
                  % if len(product_categories) >= 1:
                  <label for="category_id">Category</label>
                  ${h.select('category_id', str(product_categories[0].category_id) if len(product_categories) == 1 else None, categories)}
                  % endif
                </div>
              </div>
            % endif

            <div class="row">
              <div class="span8">
                <label for="description">Simple Description
                  ${h.help("""Description of the product.  Use good keyword practices to improve your search engine placement.""")}
                </label>
                ${h.textarea('description', style="width: 100%; height: 70px;", content=product.description)}
              </div>
            </div>
            
            % if not parent_product:
              <div class="row">
                <div class="span8">
                  <label for="detail_description">Detailed Description
                    ${h.help("""Description of the product only used on the product detail page.  Use good keyword practices to improve your search engine placement.""")}
                  </label>
                  ${h.textarea('detail_description', style="width: 100%; height: 100px;", content=product.detail_description)}
                </div>
              </div>
  
              <div class="row">
                <div class="span7">
                  <h3>Search Engine Keywords</h3>
                  <div class="row">
                    <div class="span3">
                      <label for="seo_keywords">Keywords
                        ${h.help("""Search engine keywords embedded in the HTML of the page.  Keywords should be separated by a ',' (comma).  These are read by search engines like Google to help 
                        web users find relevant results to their searches. The more relevant your keywords are to your product description and name, the better the chances of being found by the search engines.
                        """)}
                      </label>
                      ${h.text('seo_keywords', class_="input-xlarge", value=product.seo_keywords)}
                    </div>
                    <div class="span4">
                      <label for="seo_title">Title
                        ${h.help("""Search engine title embedded in the HTML of the page.  This title will be visible in your browser when a user visits the site.  These are read by search engines like Google to help 
                        web users find relevant results to their searches. The more relevant your keywords are to your product description and name, the better the chances of being found by the search engines.
                        """)}
                      </label>
                      ${h.text('seo_title', class_="input-xlarge", value=product.seo_title)}
                    </div>
                    <div class="span4">
                      <label for="seo_description">Description
                        ${h.help("""Search engine description embedded in the HTML of the page.  These are read by search engines like Google to help 
                        web users find relevant results to their searches. The more relevant your description is to your product description and name, the better the chances of being found by the search engines.
                        """)}
                      </label>
                      ${h.text('seo_description', class_="input-xlarge", value=product.seo_description)}
                    </div>
                  </div>
                </div>
              </div>
            % endif
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
                    ${h.select('company_id', str(product.company_id), companies)}
                  </div>
                  % if parent_product:
                  <input type="hidden" name="type" id="type" value="Attr"/>
                  % else:
                  <div class="span3">
                    <label for="type">Product Type
                      ${h.help("""<b>Top Level</b> : Products that appear on a website.  They may have 'child' products, but may not be included as part of a package.<br/>
                                  <b>Child</b>: Products that only appear as part of a package of other products.
                      """)}
                    </label>
                    ${h.select('type', product.type, product_types)}
                  </div>
                  % endif
                </div>
                <div class="row">
                  <div class="span2">
                    <label for="unit_cost">Unit Cost
                      ${h.help("""How much this product costs <em>you.</em>  This goes into margin calculations. """)}
                    </label>
                    ${h.text('unit_cost', class_="input-small", value=product.unit_cost)}
                  </div>
                  <div class="span2">
                    <label for="weight">Weight
                      ${h.help("""Weight in pounds.  Used in shipping calculations.""")}
                    </label>
                    ${h.text('weight', class_="input-small", value=product.weight)}
                  </div>
                  <div class="span2">
                    <label for="handling_price">Handling Price
                      ${h.help("""Optional flat fee added to the price of an item.""")}
                    </label>
                    ${h.text('handling_price', class_="input-small", value=product.handling_price)}
                  </div>
                </div>
                % if not parent_product:
                <div class="row">
                  <div class="span3">                    
                    <label for="url">Action URL
                      ${h.help("""Advanced Feature.  URL to launch after login.  Only used on specialized products.""")}
                    </label>
                    ${h.text('url', size=50, value=product.url)}
                  </div>
                  <div class="span4">
                    <label for="url">Renderer Template
                      ${h.help("""Advanced Feature.  Template to use other than 'product' to show the product on the site.""")}
                    </label>
                    ${h.text('render_template', size=50, value=product.render_template)}
                  </div>
                </div>
                % endif
              </div>
              <div class="span1">
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('enabled', checked=product.enabled, label=' Enabled?')}
                  </div>
                </div>
                % if not parent_product:
                <div class="row">
                  <div class="span2">
                    ${h.checkbox('subscription', checked=product.subscription, label=' Subscription?')}
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
                % endif
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
                    % if parent_product and not product.product_id:
                    ${h.checkbox('track_inventory', checked=False, label=' Track Inventory for this product?')}
                    % else:
                    ${h.checkbox('track_inventory', checked=product.track_inventory, label=' Track Inventory for this product?')}
                    % endif
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
                    ${h.select('vendor_id', str(product.vendor_id), vendors)}
                  </div>
                  % endif
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      % if not is_attribute and product.product_id:
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                <h3>Product Attributes</h3>
              </div>
              <div class="span1" style="margin-top:20px;">
                      ${h.help("""<p>Product Attributes are variations on a product that effect the fullfillment or price of the final purchased item.</p>
                                  <p><b>Example:</b>  If your product is a 'Shirt', then 'Color' and 'Size' would be a class of attributes, and 'Blue', 'Green', 'Small', 'Large' would be individual Attribute values.</p>
                                  <p>A purchase may have multiple attributes.  In this example, a small blue shirt would involve 2 instances of attributes on the 'Shirt' item.</p>
                                  """)}
              </div>
              <div class="span3 offset1" style="margin-top:20px;">
                <a href="/crm/product/new?is_attribute=True&parent_id=${product.product_id}">New Attribute Value</a>
              </div>
            </div>
            <div class="row">
              <div class="span8">
                <div style="overflow: scroll; height: 250px;">
                  <table class="table table-striped">
                    <tr>
                      <th>Attribute</th>
                      <th>Value</th>


                    </tr>
                    <%
                       prod_attrs = product.get_product_attributes()
                       %>
                    % for prod_attr in prod_attrs:
                    <tr>
                      <td>${prod_attr.attr_class}</td>
                      <td><a href="/crm/product/edit/${prod_attr.product_id}?is_attribute=True&parent_id=${product.product_id}">${prod_attr.name}</a></td>
                    </tr>
                    % endfor
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      % endif

      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                % if parent_product:
                <h3>Attribute Pricing</h3>
                % else:
                <h3>Product Pricing</h3>
                % endif
              </div>
              <div class="span1" style="margin-top:20px;">
                ${h.help("""Allows you to vary your pricing by campaign.  See your campaigns <a href='/crm/campaign/list'>here</a>.""")}
              </div>
              <div class="span3">
                % if parent_product:
                <h3>Attribute Keys</h3>
                % else:
                <h3>Product Keys</h3>
                % endif
              </div>
              <div class="span1" style="margin-top:20px;">
                ${h.help("""<em>Advanced Feature</em> The presence or absence of key/values is used by the system to drive behavior.""")}
              </div>
            </div>
            <div class="row">
              <div class="span4" id="result_list">
                <table>
                  <tr>
                    <th>Campaign</th>
                    <th>Price</th>
                    <th>Discount Price</th>
                  </tr>
                  % for cmp in campaigns:
                  <tr>
                    <td nowrap>${cmp.name}</td>
                    <td>${h.text('campaign_price[%s]' % cmp.campaign_id, class_="input-small", value=h.money(product.get_retail_price(cmp)))}</td>
                    <td>${h.text('campaign_discount[%s]' % cmp.campaign_id, class_="input-small", value=h.money(product.get_discount_price(cmp)))}</td>
                  </tr>
                  % endfor
                </table>
              </div>
              <div class="span3">
                <div style="overflow: scroll; height: 250px;">
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
            </div>
          </div>
        </div>
      </div>

      % if not is_attribute:
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span4">
                <h3>Child Products</h3>
              </div>
              <div class="span1" style="margin-top:20px;">
                ${h.help("""Select other products to make up a package.  The product you are on needs to be a top level product for this to work as expected.""")}
              </div>
            </div>
            <div class="row">
              <div class="span4">
                % if product.can_have_children() and other_products and not request.ctx.user.is_vendor_user():
                <div style="overflow: scroll; height: 250px;">
                  <table>
                    <tr><th></th><th>Include?</th><th>Quantity</th></tr>
                    % for p in children:
                    <tr>
                      <td>${p.child.name}</td>
                      <td nowrap>${h.checkbox('child_incl_%s' % p.child.product_id, checked=True, value=p.child.product_id, class_='product_chk')}</td>
                      <td nowrap>${h.text('child_quantity_%s' % p.child.product_id, value=p.child_quantity, class_="input-small")}</td>
                    </tr>
                    % endfor
                    
                    % for p in non_children:
                    <tr>
                      <td>${p.name}</td>
                      <td nowrap>${h.checkbox('child_incl_%s' % p.product_id, value=p.product_id, class_='product_chk')}</td>
                      <td nowrap>${h.text('child_quantity_%s' % p.product_id, class_="input-small")}</td>
                    </tr>
                    % endfor
                  </table>
                </div>
                % endif
              </div>
            </div>
          </div>
        </div>
      </div>
      % endif
      % if request.ctx.user.priv.edit_product:
      <div class="row">
        <div class="span2 offset8">
          <input type="submit" name="submit2" class="btn btn-primary" value="Save"/>
          % if product.product_id:
          <a class="btn btn-warning" href="javascript:product_delete()">Delete</a>
          % endif

        </div>
      </div>
      % endif

      <!--div class="row">
        <div class="span9">
          <div class="row">
            <div class="span3 offset4">
              <h3>Product Creation Details</h3>
              % if product.product_id:
              <table>
                <tr><td>Create Date</td><td>${h.nvl(product.create_dt)}</td></tr>
                <tr><td>Mod Date</td><td>${h.nvl(product.mod_dt)}</td></tr>
                <tr><td>Delete Date</td><td>${h.nvl(product.delete_dt)}</td></tr>
              </table>
              % endif
            </div>
          </div>
        </div>
      </div-->
    </form>
  </div>
</div>


<%def name="other_foot()">\
<script>
/* KB: [2011-08-20]: You can't do this onload.  Not sure why, but this mimics the script block at the end of the page. */
product_setup_textarea();

pvs.onload.push(function() {
  % if parent_product:
    product_validate_product_attribute();
  % else:
    product_validate_product();
  % endif
});

</script>
</%def>
