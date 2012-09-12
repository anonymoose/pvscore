
<%inherit file="product.base.mako"/>\

<div> 
  <h1>Edit Product Category</h1>
  <form method="POST" action="/crm/product/category/save" id="frm_category">
    ${h.hidden('category_id', value=category.category_id)}

    <div class="well">
      <div class="row">
        <div class="span3">
          <label for="name">Name</label>
          ${h.text('name', size=50, value=category.name)}
        </div>
        <div class="span3">
          <label for="company_id">Company</label>
          ${h.select('company_id', category.company_id, companies)}
        </div>
      </div> 

      <div class="row">
        <div class="span8">
          <label for="description">Description</label>
          ${h.textarea('description', style="width: 100%;height: 70px;", content=category.description)}
        </div>
      </div>

      <div class="row">
        <div class="span7">
          <h3>Search Engine Keywords</h3>
          <div class="row">
            <div class="span3">
              <label for="seo_keywords">Keywords</label>
              ${h.text('seo_keywords', class_="input-xlarge", value=category.seo_keywords)}
            </div>
            <div class="span4">
              <label for="seo_title">Title</label>
              ${h.text('seo_title', class_="input-xlarge", value=category.seo_title)}
            </div>
            <div class="span4">
              <label for="seo_description">Description</label>
              ${h.text('seo_description', class_="input-xlarge", value=category.seo_description)}
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="span9">
          <div class="row">
            <div class="span4">
              % if all_products:
              <h3>Child Products</h3>
              <div style="overflow: scroll; height: 400px;">
                <table>
                  <tr><th></th><th>Include?</th></tr>
                  % for p in category.products:
                  <tr>
                    <td>${p.name}</td>
                    <td nowrap>${h.checkbox('child_incl_%d' % p.product_id, checked=True, value=p.product_id, class_='product_chk')}</td>
                  </tr>
                  % endfor          
                  <%
                     kids = category.products
                     non_kids = []
                     for p in all_products:
                        found = False
                        for kid in kids:
                           if kid.product_id == p.product_id:
                              found = True
                              break
                        if found == False:
                           non_kids.append(p)
                  %>

                  % for p in non_kids:
                  <tr>
                    <td>${p.name}</td>
                    <td nowrap>${h.checkbox('child_incl_%d' % p.product_id, checked=False, value=p.product_id, class_='product_chk')}</td>
                  </tr>
                  % endfor          
                </table>
              </div>
              % endif
    
              <div class="span3">
                % if category.category_id:
                <table>
                  <tr><td>Create Date</td><td>${h.nvl(category.create_dt)}</td></tr>
                  <tr><td>Mod Date</td><td>${h.date_time(h.nvl(category.mod_dt))}</td></tr>
                  <tr><td>Delete Date</td><td>${h.nvl(category.delete_dt)}</td></tr>
                </table>
                % endif
              </div>
              <div class="span2 offset7">
                <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</div>


<%def name="other_foot()">\
<script>
/* KB: [2011-08-20]: You can't do this onload.  Not sure why, but this mimics the script block at the end of the page. */
product_setup_textarea();
</script>
</%def>