/* KB: [2010-11-09]: Functions for use with the front end site. */

cms = function() {
    pub = {
    };
    return pub;
}();

cms.catalog = function() {
    pub = {
        clear_cart : function(elem, on_success, on_fail) {
            pvs.ajax.call(pvs.ajax.api({root: '/cms/cart/clear'}),
                         function(response) {
                             if (pvs.is_true(response)) {
                                 if (on_success) {
                                     on_success(elem);
                                 } else {
                                     pvs.alert('Your Cart has been cleared..');
                                 }
                             } else {
                                 if (on_fail) {
                                     on_fail(elem, response);
                                 } else {
                                     pvs.alert('Unable to clear to cart:\n'+response);
                                 }
                             }
                         });
        },

        add_to_cart_by_name : function(elem, product_name, on_success, on_fail) {
            pvs.ajax.call(pvs.ajax.api({root: '/cms/cart/add_by_name/' + product_name + '/1'}),
                         function(response) {
                             if (pvs.is_true(response)) {
                                 if (on_success) {
                                     on_success(elem, product_name);
                                 } else {
                                     pvs.alert('Your Product has been added to the cart.');
                                 }
                             } else {
                                 if (on_fail) {
                                     on_fail(elem, product_name, response);
                                 } else {
                                     pvs.alert('Unable to add to cart:\n'+response);
                                 }
                             }
                         });
        },

        add_to_cart : function(elem, product_id, on_success, on_fail) {
            pvs.ajax.call(pvs.ajax.api({root: '/cms/cart/add/' + product_id + '/1'}),
                         function(response) {
                             if (pvs.is_true(response)) {
                                 if (on_success) {
                                     on_success(elem, product_id);
                                 } else {
                                     pvs.alert('Your Product has been added to the cart.');
                                 }
                             } else {
                                 if (on_fail) {
                                     on_fail(elem, product_id, response);
                                 } else {
                                     pvs.alert('Unable to add to cart:\n'+response);
                                 }
                             }
                         });
        },

        remove_from_cart : function(elem, product_id, on_success, on_fail) {
            pvs.ajax.call(pvs.ajax.api({root: '/cms/cart/remove/' + product_id}),
                         function(response) {
                             if (pvs.is_true(response)) {
                                 if (on_success) {
                                     on_success(elem, product_id);
                                 } else {
                                     pvs.alert('Your Product has been removed from the cart.');
                                 }
                             } else {
                                 if (on_fail) {
                                     on_fail(elem, product_id, response);
                                 } else {
                                     pvs.alert('Unable to remove from the cart:\n'+response);
                                 }
                             }
                         });
        },

        set_shipping_timeframe : function(elem, timeframe, on_success) {
            pvs.ajax.call(pvs.ajax.api({root: '/cms/cart/set_shipping_timeframe/'+timeframe}),
                  function(response) {
                      if (pvs.is_true(response)) {
                          on_success(elem, timeframe);
                      } else {
                          pvs.alert(response);
                      }
                  });

        },

        goto_checkout : function() {
            pvs.browser.goto_url('/cms/cart/checkout');
        }
    };
    return pub;
}();

