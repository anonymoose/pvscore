/* KB: [2010-11-09]: Functions for use with the front end site. */

is_true = function(val) {
    return (val === true || val === 'True' || val == 'true' || val === 'Y' || val === 'y');
}


cms = function() {
    pub = {
    };
    return pub;
}();

cms.catalog = function() {
    pub = {
        clear_cart : function(elem, on_success, on_fail) {
            $.get('/ecom/cart/clear',
                  function(response) {
                      if (is_true(response)) {
                          if (on_success) {
                              on_success(elem);
                          } else {
                              alert('Your Cart has been cleared..');
                          }
                      } else {
                          if (on_fail) {
                              on_fail(elem, response);
                          } else {
                              alert('Unable to clear to cart:\n'+response);
                          }
                      }
                  });
        },

        add_to_cart : function(elem, product_id, on_success, on_fail) {
            $.get('/ecom/cart/add/' + product_id + '/1',
                  function(response) {
                      if (is_true(response)) {
                          if (on_success) {
                              on_success(elem, product_id);
                          } else {
                              alert('Your Product has been added to the cart.');
                          }
                      } else {
                          if (on_fail) {
                              on_fail(elem, product_id, response);
                          } else {
                              alert('Unable to add to cart:\n'+response);
                          }
                      }
                  });
        },

        update_cart : function(elem, product_id, quantity, on_success, on_fail) {
            $.get('/ecom/cart/update/' + product_id + '/' + quantity,
                  function(response) {
                      if (is_true(response)) {
                          if (on_success) {
                              on_success(elem, product_id);
                          } else {
                              alert('Your cart has been updated.');
                          }
                      } else {
                          if (on_fail) {
                              on_fail(elem, product_id, response);
                          } else {
                              alert('Unable to update cart:\n'+response);
                          }
                      }
                  });
        },

        remove_from_cart : function(elem, product_id, on_success, on_fail) {
            $.get('/ecom/cart/remove/' + product_id,
                  function(response) {
                      if (is_true(response)) {
                          if (on_success) {
                              on_success(elem, product_id);
                          } else {
                              alert('Your Product has been removed from the cart.');
                          }
                      } else {
                          if (on_fail) {
                              on_fail(elem, product_id, response);
                          } else {
                              alert('Unable to remove from the cart:\n'+response);
                          }
                      }
                  });
        },

        set_shipping : function(elem, code, on_success, on_fail) {
            $.get('/ecom/cart/set_shipping/' + code,
                  function(response) {
                      if (is_true(response)) {
                          if (on_success) {
                              on_success(elem, code);
                          } else {
                              alert('Shipping Updated');
                          }
                      } else {
                          if (on_fail) {
                              on_fail(elem, code, response);
                          } else {
                              alert('Unable to update shipping:\n'+response);
                          }
                      }
                  });
        }
    };
    return pub;
}();

