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


pvs.onload.push(function() {
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
});