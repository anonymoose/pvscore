discount_delete = function() {
    if ($_('#discount_id')) {
        var answer = confirm("Really Delete Discount?")
        if (answer) {
            pvs.ajax.call(pvs.ajax.api({root: '/crm/discount/delete/'+$_('#discount_id')}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              pvs.alert('Discount Deleted');
                              pvs.browser.goto_url('/crm/discount/list');
                          } else {
                              pvs.alert('Unable to delete:\n'+response);
                          }
                      });
        }
    } else {
        pvs.alert('Save discount first');
    }
};


discount_cart_discount_change = function() {
    if ($('#cart_discount').is(':checked')) {
        $(".included_products").hide();
        $('.product_chk').attr('checked', false);
        $('.cart').show();
    } else {
        $(".included_products").show();
        $('.cart').hide();
    }
};

pvs.onload.push(function() {
    $('#frm_discount').validate(
        pvs.validate.options({
            name: 'required',
            which_item: 'required',
            percent_off: {
                number: true,
                min: 0.0,
                max: 100.0,
                required: function(element) {
                    return $('#amount_off').val().length > 0;
                }
            },
            amount_off: {
                number: true,
                min: 0.0,
                required: function(element) {
                    return $('#percent_off').val().length > 0;
                }
            },
            cart_minimum: {
                number: true,
                min: 0.0
            }
        })
    );
});