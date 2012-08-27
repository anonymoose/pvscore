
<%inherit file="product.base.mako"/>\


<div id="div_discount">
  ${h.secure_form(h.url('/crm/discount/save'), id="frm_discount")}
  ${h.hidden('discount_id', value=c.discount.discount_id)}

  <h1>Edit Discount</h1>
  <div class="_50">
    <label for="">Name</label>
    ${h.text('name', size=50, value=c.discount.name)}
  </div>
  <div class="_50">
    <label for="">Code</label>
    ${h.text('code', size=50, value=c.discount.code)}
  </div>
  <div class="_50">
    <label for="">Description</label>
    ${h.textarea('description', style="width: 100%; height: 100px;", content=c.discount.description)}
  </div>
  <div class="_50">
    <label for="">Which Item</label>
    ${h.select('which_item', c.discount.which_item, c.which_item_types)}
  </div>
  <div class="_25">
    <label for="">$ Amount Off</label>
    ${h.text('amount_off', size=10, value=c.discount.amount_off)}
  </div>
  <div class="_25">
    <label for="">% Off</label>
    ${h.text('percent_off', size=10, value=c.discount.percent_off)}
  </div>
  <div class="clear"></div>
  <div class="_50">
    ${h.checkbox('web_enabled', checked=c.discount.web_enabled, label='Web Enabled?')}
    ${h.checkbox('store_enabled', checked=c.discount.store_enabled, label='Store Enabled?')}
  </div>
  <div class="_25">
    <label for="">Start Date</label>
    ${h.text('start_dt', size=10, value=c.discount.start_dt)}
  </div>
  <div class="_25">
    <label for="">End Date</label>
    ${h.text('end_dt', size=10, value=c.discount.end_dt)}
  </div>
  % if c.current_user.priv.edit_discount:
  <div class="align-right">
    ${h.submit('submit', 'Submit', class_="form-button")}&nbsp;
  </div>
  % endif
  ${h.end_form()}
</div>

<script>
    $('#frm_discount').validate({
        rules: {
            name: 'required',
            which_item: 'required',
            percent_off: {
                number: true,
                min: 0.0
            },
            amount_off: {
                number: true,
                min: 0.0,
                max: 100.0
            }
        },
        messages: {
            name: ' ',
            type: ' ',
            //sku: ' ',
            percent_off: ' ',
            amount_off: ' '
        }
    });

    if ($('#start_dt')) {
        pvs.ui.init_datepicker('#start_dt');
    }
    if ($('#end_dt')) {
        pvs.ui.init_datepicker('#end_dt');
    }
</script>
