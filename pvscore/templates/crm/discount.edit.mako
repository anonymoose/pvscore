
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
          <label for="">Code
            ${h.help("""Give this code to cusotmers so they may enter it at checkout.""")}
          </label>
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
          <label for="">% Off
            ${h.help("""If this is a cart discount, this applies to the whole cart.  If this is for individual products then each product's applicable price is 
            reduced by the percentage indicated here.  This is not allowed to be used in conjunction with 'Cart Shipping % Off' to the right.
            <br/>Entering '20' means you want a 20% discount. """)}
          </label>
          ${h.text('percent_off', class_="input-small", value=discount.percent_off)}
        </div>
        <div class="span2 offset4 cart"
           % if not discount.cart_discount:
           style="display:none;"
           % endif
             >
          <label for="">Cart Shipping % Off
            ${h.help("""This percentage discount is applied to apply to the shipping selections.  This is not allowed when using the other '% Off' field to the left.
            <br/>Enter '100' for free shipping.  If '100' is entered, only the cheapest shipping
            option will be presented to the customer.""")}
          </label>
          ${h.text('shipping_percent_off', class_="input-small", value=discount.shipping_percent_off)}
        </div>
      </div>
      <div class="row">
        <div class="span2">
          ${h.chkbox('web_enabled', checked=discount.web_enabled, label=' Web Enabled?', 
              help=h.help("Is this useable by customers visiting the website?"))}
        </div>
        <!--div class="span2">
          ${h.chkbox('store_enabled', checked=discount.store_enabled, label=' Store Enabled?')}    
        </div-->
        <div class="span2 offset2">
          ${h.chkbox('cart_discount', checked=discount.cart_discount, label=' Cart Discount?', onchange="discount_cart_discount_change();")}    
        </div>
        <div class="span2 cart">
          ${h.chkbox('automatic', checked=discount.automatic, label=' Automatic?',
                                  help=h.help("""Should this discount be automatically applied by the system without user intervention?  
                                                <br/><br/><b>Example:</b>'Free shipping with orders over $20' would require automatic checked, cart discount checked, a cart minimum of '20' and a cart shipping % off of '100'"""))}    
        </div>
      </div>
      <div class="row">
        <div class="span2">
          <label for="">Start Date</label>
          ${h.text('start_dt', class_="input-small datepicker", autocomplete="off", value=discount.start_dt if discount.start_dt else tomorrow)}
        </div>
        <div class="span2">
          <label for="">End Date</label>
          ${h.text('end_dt', class_="input-small datepicker", autocomplete="off", value=discount.end_dt if discount.end_dt else plus14)}
        </div>
        <div class="span2 offset2 cart"
           % if not discount.cart_discount:
           style="display:none;"
           % endif
           >
          <label for="">Cart Minimum</label>
          ${h.text('cart_minimum', class_="input-small", value=discount.cart_minimum)}
        </div>
      </div>
    </div>

    <div class="row included_products">
      <div class="span4">
        <h3>Included Products</h3>
      </div>
      <div class="span1" style="margin-top:20px;">
        ${h.help("""Select products effected by this discount.""")}
      </div>
    </div>
    <div class="row included_products">
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

