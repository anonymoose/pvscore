
pvs.onload.push(function() {
    $('#prod_complete').typeahead({
        source: function(typeahead, query) {
            $.ajax({
                url: "/crm/product/autocomplete_by_name",
                dataType: "json",
                type: "GET",
                data: {
                    max_rows: 15,
                    search_key: query,
                    ajax: 1
                },
                success: function(data) {
                    var return_list = [], i = data.length;
                    while (i--) {
                        return_list[i] = {id: data[i].product_id, value: data[i].name, cost: data[i].unit_cost};
                    }
                    typeahead.process(return_list);
                }
            });
        },
        onselect: function(obj) {
            $('#quantity').val(1);
            $('#order_note').val(obj.value);
            $('#product_id').val(obj.id);
            var cost = obj.cost;
            if (cost) {
                $('#unit_cost').val(parseFloat(cost).toFixed(2));
                $('#amount').val((parseFloat(cost) * parseFloat(1)).toFixed(2));
            }
        }
    });
});


purchase_accept_order_item = function() {
    if ($('#frm_order_item').validate().form()) {
        var product_id = $('#product_id').val();
        pvs.form.post('#frm_order_item', 
                  pvs.ajax.api({root: '/crm/purchase/save_purchase_order_item/'+$_('#purchase_order_id'),
                                product_id: product_id}),
                  function(response) {
                      var resp = pvs.json.decode(response);
                      $('#po_items').append('<tr>'+
                                            '<td><img src="/static/icons/silk/accept.png" class="clickable" title="Complete" alt="Complete" border="0" onclick="purchase_complete_order_item(this, '+resp.id+')"></td>'+
                                            '<td><img src="/static/icons/silk/delete.png" class="clickable" title="Delete" alt="Delete" border="0" onclick="purchase_delete_order_item(this, '+resp.id+')"></td>'+
                                            '<td><img src="/static/icons/silk/page_edit.png" class="clickable" title="Edit" alt="Edit" border="0" onclick="purchase_edit_order_item(this, '+resp.id+', '+product_id+')"></td>'+
                                            '<td>'+$_('#prod_complete')+'</td>'+
                                            '<td>'+$_('#order_note')+'</td>'+
                                            '<td>'+$_('#quantity')+'</td>'+
                                            '<td>'+parseFloat($_('#unit_cost')).toFixed(2)+'</td>'+
                                            '<td>'+parseFloat($_('#amount')).toFixed(2)+'</td>'+
                                            '</tr>');
                      $('#product_id').val('');
                      $('#order_item_id').val('');
                      $('#prod_complete').val('');
                      $('#order_note').val('');
                      $('#quantity').val('');
                      $('#unit_cost').val('');
                      $('#amount').val('');
                  });
    } else {
        $('#frm_order_item').validate().showErrors();
    }
};

purchase_show_items = function() {
    if ($_('#purchase_order_id')) {
        pvs.ui.menu_highlight('link_orders');
        pvs.dialog.wait();
        $('#div_purchase_detail').load(pvs.ajax.dialog({root: '/crm/purchase/edit_items/'+$_('#purchase_order_id')}),
                                       function() {
                                           pvs.dialog.unwait();
                                           $('#frm_order_item').validate({
                                               rules : {
                                                   prod_complete: 'required',
                                                   order_item_complete: 'required',
                                                   quantity: {
                                                       required: true,
                                                       min: 1,
                                                       number: true
                                                   },
                                                   unit_cost: {
                                                       required: true, 
                                                       min: 0,
                                                       number: true
                                                   }
                                               },
                                               messages: {
                                                   prod_complete: " ",
                                                   quantity: {
                                                       required: " ",
                                                       min: " ",
                                                       number: " "
                                                   },
                                                   unit_cost: " "
                                               }
                                           });
                                       });
    }
};


purchase_show_history = function(offset) {
    if ($_('#purchase_order_id')) {
        pvs.ui.menu_highlight('link_history');
        pvs.dialog.wait('#div_purchase_detail');
        $('#div_purchase_detail').load(pvs.ajax.dialog({root: '/crm/purchase/show_history/'+$_('#purchase_order_id'),
                                                        offset: offset}),
                                       function() {
                                          pvs.dialog.unwait('#div_purchase_detail');
                                      });
    } else {
        pvs.alert('Must Save PO first.');
    }
};

purchase_delete_order_item = function(elem, order_item_id) {
    pvs.ajax.call(pvs.ajax.api({root: '/crm/purchase/delete_purchase_order_item/'+$_('#purchase_order_id')+'/'+order_item_id}),
                  function(response) {
                      if (pvs.is_true(response)) {
                          $(elem).parent().parent().remove();
                      } else {
                          pvs.alert('Unable to save order:\n'+response);
                      }
                  });
    
};

purchase_edit_order_item = function(elem, order_item_id, product_id) {
    pvs.ajax.call(pvs.ajax.api({root: '/crm/purchase/order_item_json/'+$_('#purchase_order_id')+'/'+order_item_id}),
                  function(response) {
                      $(elem).parent().parent().remove();
                      var poi = pvs.json.decode(response); 
                      $('#product_id').val(product_id);
                      $('#order_item_id').val(poi.order_item_id);
                      $('#prod_complete').val(poi.prod_name);
                      $('#order_note').val(poi.note);
                      $('#quantity').val(poi.quantity);
                      $('#unit_cost').val(parseFloat(poi.unit_cost).toFixed(2));
                      $('#amount').val((parseFloat(poi.unit_cost) * parseFloat(poi.quantity)).toFixed(2));
                  });
};

purchase_complete = function() {
    if ($_('#purchase_order_id')) {
        pvs.confirm("Complete purchase order?", "Purchase",
                    function() {
                        pvs.ajax.call(pvs.ajax.api({root: '/crm/purchase/complete/'+$_('#purchase_order_id')}),
                                      function(response) {
                                          if (pvs.is_true(response)) {
                                              pvs.alert('Purchase Order Completed.');
                                              pvs.browser.goto_url('/crm/purchase/edit/'+$_('#purchase_order_id'));
                                          } else {
                                              pvs.alert('Unable to save order:\n'+response);
                                          }
                                      });
                        
                    });
    } else {
        pvs.alert('Save purchase order first');
    }
};

purchase_complete_order_item = function(elem, order_item_id) {
    if ($_('#purchase_order_id')) {
        pvs.confirm("Complete purchase order item?", "Purchase",
                    function() {
                        pvs.ajax.call(pvs.ajax.api({root: '/crm/purchase/complete_item/'+$_('#purchase_order_id')+'/'+order_item_id}),
                                      function(response) {
                                          if (pvs.is_true(response)) {
                                              pvs.alert('Purchase Order Item Completed.');
                                              pvs.browser.goto_url('/crm/purchase/edit/'+$_('#purchase_order_id'));
                                          } else {
                                              pvs.alert('Unable to complete order item:\n'+response);
                                          }
                                      });
                    });
    } else {
        pvs.alert('Save purchase order first');
    }
};

pvs.onload.push(function() {
    $('#frm_purchase').validate(
         pvs.validate.options(
             {
                 vendor_id: 'required',
                 company_id: 'required',
                 shipping_cost: {
                     min: 0,
                     number: true
                 },
                 tax : {
                     min:0,
                     number: true
                 }
             },
             {
                 shipping_cost : 'Number > 0 please',
                 tax : 'Number > 0 please'
             }
         )
    );

    pvs.ui.init_datepicker('#from_dt');
    pvs.ui.init_datepicker('#to_dt');

});