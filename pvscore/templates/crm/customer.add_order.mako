
<%inherit file="customer.edit.base.mako"/>\

<input type="hidden" name="campaign_id" id="campaign_id" value="${customer.campaign.campaign_id}"/>

<div id="result_list">
  <div class="container">
    <div class="row">
      <div class="span6">
        <h1>Add Order</h1>
      </div>
    </div>
    <div class="row">
      <div class="span4">
        <label for="prod_complete1">Search</label>
        ${h.text('prod_complete1', size=50)}
      </div>
      <div class="offset4 span2">
        <button id="btn_add_order" class="btn btn-primary btn-large" onclick="customer_add_order_submit()" autocomplete="off" data-loading-text="loading...">Order</button>    
      </div>
    </div>
    <div class="row">
      <div class="span9">
        <table width="100%" class="table table-striped table-condensed">
          <tr id="add_product_header">
            <th width="30%">Name</th>
            <th style="text-align:right;">Price</th>
            <th style="text-align:right;">Quantity</th>
            <th style="text-align:right;" nowrap>Current Inventory</th>
          </tr>
          % for p in products:
          <tr>
            <td nowrap>${h.chkbox('chk_%s' % p.product_id, value=p.product_id, label=h.clean(p.name), onchange="customer_add_product_oncheck('%s')" % p.product_id, class_='product_chk')}</td>
            <td style="text-align:right;">$${h.money(p.get_price(customer.campaign))}</td>
            <td style="text-align:right;">${h.text('quant_%s' % p.product_id, style="width:40px;")}</td>
            <td style="text-align:right;">
              ${p.inventory if p.track_inventory else 'n/a'}
            </td>
          </tr>
            % for attr in p.get_product_attributes():
              <tr class="attrs_for_${p.product_id}" style="display:none;">
                <td style="text-align:right;">&nbsp;</td>
                <td>${h.chkbox('attr_%s' % attr.product_id, value=attr.product_id, label='%s : %s' % (attr.attr_class, attr.name), class_='attribute_chk')}</td>
                <td style="text-align:right;">
                  <input type="hidden" id="attribute_parent_${attr.product_id}" value="${p.product_id}"/>
                </td>
                <td style="text-align:right;">
                  ${attr.inventory if attr.track_inventory else 'n/a'}
                </td>
              </tr>
            % endfor
         % endfor
        </table>
      </div>
    </div>
  </div>
</div>


