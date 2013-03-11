
<%inherit file="product.base.mako"/>\

<div>
  <h1>Edit Discount</h1>
  <form method="POST" action="/crm/discount/save" id="frm_discount">
    ${h.hidden('discount_id', value=discount.discount_id)}
    <div class="well">
      <h3>General Information</h3>
      <div class="row">
        <div class="span6">
          <label for="">Name</label>
          ${h.text('name', class_="input-xxlarge", value=discount.name)}
        </div>
        <div class="span2">
          <label for="">Code</label>
          ${h.text('code', value=discount.code)}
        </div>
      </div>
      <div class="row">
        <div class="span9">
          <label for="">Description</label>
          ${h.textarea('description', discount.description, style="width: 93%; height: 120px;")}
        </div>
      </div>
      <div class="row">
        <div class="span2">
          <label for="">$ Amount Off</label>
          ${h.text('amount_off', class_="input-small", value=discount.amount_off)}
        </div>
        <div class="span2">
          <label for="">% Off</label>
          ${h.text('percent_off', class_="input-small", value=discount.percent_off)}
        </div>
        <div class="span2">
          <label for="">Start Date</label>
          ${h.text('start_dt', class_="input-small datepicker", autocomplete="off", value=discount.start_dt if discount.start_dt else tomorrow)}
        </div>
        <div class="span2">
          <label for="">End Date</label>
          ${h.text('end_dt', class_="input-small datepicker", autocomplete="off", value=discount.end_dt if discount.end_dt else plus14)}
        </div>
      </div>
      <div class="row">
        <div class="span2">
          ${h.chkbox('web_enabled', checked=discount.web_enabled, label=' Web Enabled?')}    
        </div>
        <div class="span2">
          ${h.chkbox('store_enabled', checked=discount.store_enabled, label=' Store Enabled?')}    
        </div>
      </div>
    </div>

    <div class="row">
      <div class="span4">
        <h3>Included Products</h3>
      </div>
      <div class="span1" style="margin-top:20px;">
        ${h.help("""Select products effected by this discount.""")}
      </div>
    </div>
    <div class="row">
      <div class="span4">
        <div style="overflow: scroll; height: 250px;">
          <table>
            <tr><th></th><th>Include?</th></tr>
            % for p in included_products:
            <tr>
              <td>${p.product.name}</td>
              <td nowrap>${h.checkbox('product_incl_%s' % p.product.product_id, checked=True, value=p.product.product_id, class_='product_chk')}</td>
            </tr>
            % endfor
            
            % for p in not_included_products:
            <tr>
              <td>${p.name}</td>
              <td nowrap>${h.checkbox('product_incl_%s' % p.product_id, value=p.product_id, class_='product_chk')}</td>
            </tr>
            % endfor
          </table>
        </div>
      </div>
    </div>
    
    <div class="row">
      <div class="span2 offset8">
        <input type="submit" name="submit2" class="btn btn-primary" value="Save"/>
        <a class="btn btn-warning" href="javascript:discount_delete()">Delete</a>
      </div>
    </div>
  </form>
</div>

