
customer_show_detail = function() {
    $('#div_cust_main').hide('fast', function() {
        $('#div_customer_detail').show('slow');
    });
};

customer_dashboard_find = function() {
    $('#customer_find_subsection').css('visibility', 'visible');
};

/* KB: [2010-10-08]: *********************************************
Status Management
*/
customer_status = function(order_id) {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/status_dialog/' + $_('#customer_id'),
                                                 order_id:order_id}),
                            title: (order_id ? 'Status Order' : 'Status Account'),
                            width:590,
                            height:380,
                            on_ok:
                            function() {
                                pvs.form.post('#frm_status',
                                              pvs.ajax.api({root: '/crm/customer/save_status/'+$_('#customer_id'),
                                                           order_id:order_id}),
                                              function(response) {
                                                  if (pvs.is_true(response)) {
                                                      customer_show_orders();
                                                  } else {
                                                      pvs.alert('Unable to status:\n'+response);
                                                  }
                                              }
                                             );
                           }
                          });
    } else {
        pvs.alert('Create customer first');
    }
};

customer_status_order_item = function(order_id, order_item_id) {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/status_dialog/' + $_('#customer_id'),
                                                 order_item_id:order_item_id}),
                            title: (order_id ? 'Status Order' : 'Status Account'),
                            width:590,
                            height:380,
                            on_ok:
                            function() {
                                pvs.form.post('#frm_status',
                                              pvs.ajax.api({root: '/crm/customer/save_status/'+$_('#customer_id'),
                                                           order_item_id:order_item_id}),
                                              function(response) {
                                                  if (pvs.is_true(response)) {
                                                      customer_edit_order(order_id);
                                                  } else {
                                                      pvs.alert('Unable to status:\n'+response);
                                                  }
                                              }
                                             );
                           }
                          });
    } else {
        pvs.alert('Create customer first');
    }
};

customer_delete = function(order_item_id) {
    if ($_('#customer_id')) {
        var answer = confirm("Really Delete Customer?")
        if (answer) {
            pvs.ajax.call(pvs.ajax.api({root: '/crm/customer/delete/'+$_('#customer_id')}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              pvs.alert('Customer Deleted');
                              pvs.browser.goto_url('/crm/customer/dialog/crm/customer.search');
                          } else {
                              pvs.alert('Unable to delete:\n'+response);
                          }
                      });
        }
    } else {
        pvs.alert('Save customer first');
    }
};

/* KB: [2010-10-08]: *********************************************
Billing Management
*/
customer_edit_billing_method = function() {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/edit_billing_dialog/' + $_('#customer_id')}),
                           title:('Edit Billing'),
                           width:540,
                           height:570,
                           validator: {
                               form : '#frm_billing',
                               rules : {
                                   type: 'required',
                                   account_holder: 'required',
                                   account_addr: 'required',
                                   account_city: 'required',
                                   account_state: {
                                       required: true,
                                       maxlength: 2
                                   },
                                   account_zip: {
                                       required: true,
                                       digits: true,
                                       maxlength: 5
                                   },
                                   account_country: 'required',
                                   _cc_num: {
                                       required: false,
                                       creditcard: true
                                   },
                                   cc_exp: 'required'
                               }
                           },
                           on_ok:
                           function() {
                               pvs.form.post('#frm_billing',
                                            pvs.ajax.api({root: '/crm/customer/edit_billing/'+$_('#customer_id')}),
                                                  function(response) {
                                                      if (pvs.is_true(response)) {
                                                          $('#flashes').html('Saved order.');
                                                      } else {
                                                          pvs.alert('Unable to save billing:\n'+response);
                                                      }
                                                  }
                                                 );
                           }
                          });
    } else {
        pvs.alert('Create customer first');
    }
};

/* KB: [2010-09-16]: *********************************************
Comms
*/
customer_send_email = function() {
    pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/communication/send_comm_dialog'}),
                        title: 'Select Communication',
                        width:700,
                        height:430,
                        after_display_impl:
                        function() {
                            comm_fixup_message();
                        },
                        on_ok:
                        function() {
                            var msg = null;
                            try {
                            msg = tinyMCE.get('message').getContent();
                            tinyMCE.remove(tinyMCE.get('message'));
                            } catch (e) {
                            }

                            pvs.ajax.post_array(pvs.ajax.api({root: '/crm/communication/send_customer_comm/' + $_('#customer_id') + '/' + $_('#comm_id')}),
                                                function(response) {
                                                    if (pvs.is_true(response)) {
                                                        pvs.alert('Your Email has been sent.');
                                                    } else {
                                                        pvs.alert('Unable to send email:\n'+response);
                                                    }
                                                },
                                                {msg: msg}
                                               );
                        }
                       });
};

customer_view_packing_slip = function(order_id, comm_id) {
    pvs.browser.open_window('packing_slip',
                            pvs.ajax.dialog({root: '/crm/communication/view_comm_dialog/'+$_('#customer_id') + '/' + comm_id,
                                            order_id: order_id}),
                            700, 600);
};

customer_show_status = function(status_id) {
    pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/show_status_dialog/'+$_('#customer_id')+'/'+status_id}),
                        title: 'Status',
                        width:680,
                        height:400});
};

/* KB: [2010-09-16]: *********************************************
Order Management
*/

customer_add_product_oncheck = function(id) {
    if ($('#chk_'+id).attr('checked')) {
        $('#quant_'+id).val('1.0');
    } else {
        $('#quant_'+id).val('');
    }
};

customer_prep_add_product_autocomplete = function(products, product_ids) {
    $("#prod_complete1").autocomplete(products, {
        matchContains: true,
        minChars: 0
    });

    $("#prod_complete1").result(function(event, data, formatted) {
        var product_id = product_ids[data];
        $('#chk_'+product_id).attr('checked', true);
        customer_add_product_oncheck(product_ids[data]);
        $("#prod_complete1").val('');
        $("#chk_"+product_id).parent().parent().parent().insertAfter($('#add_product_header'));
    });
};

customer_barcode_add_order = function() {
    if ($_('#email') == '* Email address for receipt') {
        $('#email').val('');
    }
    var cnt = 0;
    var obj = {};
    $('.product_chk:checked').each(function(i) {
        cnt++;
        if (obj[this.value]) {
            obj[this.value] += parseFloat($('#quant_'+this.value).val());
        } else {
            obj[this.value] = parseFloat($('#quant_'+this.value).val());
        }
    });
    if (cnt > 0) {
        var company_id = $_('#company_id');
        pvs.dialog.wait();
        pvs.ajax.post_array(pvs.ajax.api({root: '/crm/customer/add_order_and_apply/'+$_('#customer_id')+'/'+$_('#pmt_method'),
                                         email: $_('#email'), campaign_id: $_('#campaign_id'),
                                         incl_tax: $('#incl_tax').attr('checked') ? 1 : 0}),
                            function(response) {
                                pvs.dialog.unwait();
                                if (pvs.is_true(response)) {
                                    pvs.browser.goto_url('/crm/customer/barcode_order_dialog/'+$_('#pos_email')+'/'+company_id+'?done=1');
                                } else {
                                    $('#alerts').html('Unable to save products:\n'+response);
                                }
                            },
                            {products: obj}
                           );
    } else {
        $('#alerts').html('No items entered.');
    }
};

/* KB: [2011-07-27]: bar code comes across as ean8 where 00017077 = product ID 1707 */
customer_barcode_add_item = function(barcode_value) {
    if (!barcode_value) {
        $('#alerts').html('Invalid Barcode');
        return;
    }
    var pid = parseInt(barcode_value.substring(0,7).replace(/^0*/, ''));
    if (!pid) {
         $('#alerts').html('Invalid Barcode: '+barcode_value);
    }
    _customer_barcode_add_item_impl(pid);
};

_customer_barcode_add_item_impl = function(pid) {
    pvs.ajax.call(pvs.ajax.api({root: '/crm/product/json/'+pid+'/'+$_('#campaign_id')}),
                  function(response) {
                          var prod = pvs.json.decode(response);
                          if (prod) {
                              var sub_tot = parseFloat($('#sale_subtotal').html());
                              sub_tot += parseFloat(prod.unit_price);
                              if (prod.unit_price == '0.0') {
                                  pvs.alert(prod.name + ' does not have a price in the selected campaign.  Try again.', 300);
                                  return;
                              }

                              var tax = sub_tot * ($('#incl_tax').attr('checked') ? parseFloat($_('#tax_rate')) : 0.0);
                              $('#sale_subtotal').html(sub_tot.toFixed(2));
                              $('#sale_tax').html(tax.toFixed(2));
                              $('#sale_total').html((tax+sub_tot).toFixed(2));
                              var prod_price = parseFloat(prod.unit_price).toFixed(2);
                              var img = 'no pic';
                              if (prod.primary_image) {
                                  img = '<a href="'+prod.primary_image+'" class="lb"><img src="'+prod.primary_image+'" style="width:45px;"></a>';
                              }
                              $('#result_list').append('<tr id="prod_row_'+pid+'">'+
                                                       '<td nowrap><label><input class="product_chk" id="chk_'+pid+'" name="chk_'+pid+'" '+
                                                       '                         onchange="customer_barcode_remove_product('+pid+')" value="'+pid+'" checked="checked" type="checkbox">'+prod.name+'</label></td>'+
                                                       '<td>'+img+'</td>'+
                                                       '<td style="text-align:right;">$'+prod_price+
                                                       '<input type="hidden" value="1" name="quant_'+pid+'" id="quant_'+pid+'">'+
                                                       '<input type="hidden" value="'+prod_price+'" id="prod_unit_price_'+pid+'">'+
                                                       '</td>'+
                                                       '</tr>');
                              $(".lb").fancybox({
	                          'transitionIn'	 :	'elastic',
	                          'transitionOut'	 :	'elastic',
	                          'speedIn'	 :	400,
	                          'speedOut'	 :	200,
	                          'overlayShow'	 :	true,
	                          'overlayOpacity' : 0.5,
	                          'overlayColor'   : '#333',
	                          'width'          : 840
                              });
                          }



                  });
};

customer_barcode_prep_add_product_autocomplete = function(products, product_ids) {
    $("#prod_complete2").autocomplete(products, {
        matchContains: true,
        minChars: 0
    });

    $("#prod_complete2").result(function(event, data, formatted) {
        var product_id = product_ids[data];
        _customer_barcode_add_item_impl(product_id);
        $("#prod_complete2").val('');
    });
};

customer_barcode_remove_product = function(product_id) {
    var prod_price = parseFloat($_('#prod_unit_price_'+product_id));
    $('#prod_row_'+product_id).remove();
    var sub_total = parseFloat($('#sale_subtotal').html());
    sub_total -= prod_price;
    var tax = sub_total * ($('#incl_tax').attr('checked') ? parseFloat($_('#tax_rate')) : 0.0);
    $('#sale_subtotal').html(sub_total.toFixed(2));
    $('#sale_tax').html(tax.toFixed(2));
    $('#sale_total').html((tax+sub_total).toFixed(2));
};

customer_barcode_tax_recalc = function() {
    var sub_total = parseFloat($('#sale_subtotal').html());
    var tax = sub_total * ($('#incl_tax').attr('checked') ? parseFloat($_('#tax_rate')) : 0.0);
    $('#sale_subtotal').html(sub_total.toFixed(2));
    $('#sale_tax').html(tax.toFixed(2));
    $('#sale_total').html((tax+sub_total).toFixed(2));
};

customer_add_order_submit = function() {
    pvs.dialog.wait();
    var obj = {};
    $('.product_chk:checked').each(function(i) {
        obj[this.value] = $('#quant_'+this.value).val();
    });
    pvs.ajax.post_array(pvs.ajax.api({root: '/crm/customer/add_order/'+$_('#customer_id')}),
                        function(response) {
                            var order_id = parseInt(response);
                            if (order_id && order_id != NaN) {
                                $('#flashes').append('Saved order.');
                                customer_show_orders();
                            } else {
                                pvs.dialog.unwait();
                                pvs.alert('Unable to save products:\n'+response);
                            }
                        },
                        {products: obj}
                       );
};

customer_add_order_orig = function() {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/add_order_dialog/' + $_('#customer_id')}),
                           title:'Add Order',
                           width: $(window).width()*.60,
                           height:$(document).height()*.75,
                           on_ok:
                           function() {
                               var obj = {};
                               $('.product_chk:checked').each(function(i) {
                                   obj[this.value] = $('#quant_'+this.value).val();
                               });
                               pvs.ajax.post_array(pvs.ajax.api({root: '/crm/customer/add_order/'+$_('#customer_id')}),
                                                  function(response) {
                                                      var order_id = parseInt(response);
                                                      if (order_id && order_id != NaN) {
                                                          $('#flashes').append('Saved order.');
                                                          customer_show_orders();
                                                      } else {
                                                          pvs.alert('Unable to save products:\n'+response);
                                                      }
                                                  },
                                                  {products: obj}
                                                 );
                           }
                          });
    } else {
        pvs.alert('Create customer first.');
    }
};

customer_check_return_quantity = function() {
    if ($('#quantity_returned')) {
        var ret = parseFloat($_('#quantity_returned'));
        if (isNaN(ret)) {
            alert('Quantity returned must be a number');
            $('#quantity_returned').val($_('#original_quantity'))
            return;
        }
        var orig = parseFloat($_('#original_quantity'));
        if (ret > orig) {
            alert('Quantity returned must be less or equal than amount due.');
            $('#quantity_returned').val($_('#original_quantity'))
            return;
        }

        $('#credit_amount').val((ret*parseFloat($_('#original_unit_price'))).toFixed(2));
    }
};

customer_check_return_credit = function() {
    if ($('#credit_amount')) {
        var amt = parseFloat($_('#credit_amount'));
        if (isNaN(amt)) {
            alert('Credit Amount must be a number');
            $('#credit_amount').val($_('#original_total'))
            return;
        }
        var tot = parseFloat($_('#original_total'));
        if (amt > tot) {
            alert('Credit Amount returned must be less or equal than amount due.');
            $('#credit_amount').val($_('#original_total'))
            return;
        }
    }
};

customer_check_payment_amount = function() {
    if ($('#pmt_amount')) {
        var amt = parseFloat($_('#pmt_amount'));
        if (isNaN(amt)) {
            alert('Payment Amount must be a decimal number');
            return;
        }
        var tot = parseFloat($_('#total_due'));
        if (amt > tot) {
            alert('Payment amount must be less than amount due.');
            return;
        }

        if (tot == amt) {
            $('#pmt_type').val('FullPayment')
        } else {
            $('#pmt_type').val('PartialPayment')
        }
    }
};

customer_return_order_item = function(order_id, order_item_id, quantity, amt) {
    if ($_('#oi_order_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/return_item_dialog/' + $_('#customer_id')+'/'+order_id+'/'+order_item_id}),
                            title:'Return Item',
                            width: $(window).width()*.40,
                            height:$(document).height()*.4,
                            dialog_id: 'dialog4',
                            validator: {
                                form: '#frm_return_item',
                                rules: {
                                    quantity_returned: {
                                        required: true,
                                        number: true,
                                        min: 1,
                                        max: quantity
                                    },
                                    credit_amount: {
                                        required: true,
                                        number: true,
                                        min: 0,
                                        max: amt
                                    }
                                },
                                messages: {
                                    quantity_returned: ' ',
                                    credit_amount: ' '
                                }
                            },
                            on_ok:
                            function() {
                                var original_quantity = parseFloat($_("#original_quantity"));
                                var original_total = parseFloat($_("#original_total"));
                                var original_unit_price = parseFloat($_("#original_unit_price"));
                                var quantity_returned = parseFloat($_('#quantity_returned'));
                                var credit_amount = parseFloat($_('#credit_amount'));
                                pvs.form.post('#frm_return_item',
                                              pvs.ajax.api({root: '/crm/customer/return_item/'+$_('#customer_id')+'/'+order_id+'/'+order_item_id}),
                                              function(response) {
                                                  if (pvs.is_true(response)) {
                                                      if (original_quantity == quantity_returned) {
                                                          customer_delete_order_item(order_item_id);
                                                      } else {
                                                          $('#quantity'+order_item_id).val((original_quantity - quantity_returned).toFixed(1))
                                                      }
                                                      customer_order_recalc();
                                                  } else {
                                                      pvs.alert('Unable to return products:\n'+response);
                                                  }
                                              }
                                             );
                            }
                           });
    } else {
        pvs.alert('Save order first.');
    }
};

customer_apply_credit = function() {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/apply_credit_dialog/' + $_('#customer_id')}),
                            title:'Apply Credit Balance',
                            width: $(window).width()*.30,
                            height:$(document).height()*.4,
                            on_ok:
                            function() {
                                if ($_('#can_apply_credit') == '1') {
                                    customer_show_balance();
                                    customer_show_orders();
                                } else {
                                    customer_show_balance();
                                    customer_show_orders();
                                }
                            }
                           });
    }
};

customer_apply_payment_method_change = function() {
    if ($_('#oi_order_id')) {

    }
};

customer_apply_payment = function(order_id) {
    customer_apply_payment_impl(order_id,
                                'Apply Payment',
                                pvs.ajax.dialog({root: '/crm/customer/apply_payment_dialog/' + $_('#customer_id')+'/'+order_id}));
};

customer_apply_discount = function(order_id) {
    customer_apply_payment_impl(order_id,
                                'Apply Discount',
                                pvs.ajax.dialog({root: '/crm/customer/apply_payment_dialog/' + $_('#customer_id')+'/'+order_id,
                                                discount: 1}),
                                'Discount',
                                1);
};

customer_apply_payment_impl = function(order_id, title, url, pmt_type, discount) {
    if ($_('#oi_order_id')) {
        pvs.dialog.display({url:url,
                            title:title,
                            width: $(window).width()*.40,
                            height:410,
                            dialog_id: 'dialog4',
                            validator: {
                                form : '#frm_apply_payment',
                                rules : {
                                    pmt_method: 'required',
                                    pmt_amount: {
                                        required: true,
                                        min: 0.01,
                                        number: true
                                    }
                                },
                                messages: {
                                    pmt_method: ' ',
                                    pmt_amount: ' '
                                }
                            },
                            on_ok:
                            function() {
                                var pmt_applied = 0;
                                var pmt_amount = parseFloat($_('#pmt_amount'))
                                pmt_applied = parseFloat($_('#total_applied')) + pmt_amount;
                                if (parseFloat($_('#pmt_amount')) > 0 && parseFloat($_('#pmt_amount')) < parseFloat($_('#total_due'))) {
                                    $('#pmt_type').val('PartialPayment');
                                }
                                if (pmt_type) {
                                    $('#pmt_type').val(pmt_type);
                                }
                                pvs.form.post('#frm_apply_payment',
                                              pvs.ajax.api({root: '/crm/customer/apply_payment/'+$_('#customer_id')+'/'+order_id}),
                                              function(response) {
                                                  if (pvs.is_true(response)) {
                                                      if (!discount) {
                                                          if ($('#oi_payments_applied')) {
                                                              $('#oi_payments_applied').html('$'+pmt_applied.toFixed(2));
                                                              for (var i=0 ; i<oi_ids.length ; i++) {
                                                                  var oid = oi_ids[i];
                                                                  if (oid && oid != -1) {
                                                                      $('#unit_price'+oid+'').attr('disabled', 'disabled');
                                                                      $('#quantity'+oid+'').attr('disabled', 'disabled');
                                                                      $('.img_return').show();
                                                                      $('.img_delete').hide();
                                                                  }
                                                              }
                                                          }
                                                      } else {
                                                          $('#oi_total_price').html('$'+(parseFloat($_('#total_price'))-pmt_applied).toFixed(2));
                                                          var rndid = Math.floor(Math.random()*1000)
                                                          $('#result_list_header').append('<tr>'+
                                                                                          '<td>'+
                                                                                          '<img src="/public/images/icons/silk/delete.png" border="0" onclick="customer_delete_discount('+rndid+'_)">'+
                                                                                          '</td>'+
                                                                                          '<td>&nbsp;</td>'+
                                                                                          '<td width="25%">Discount</td>'+
                                                                                          '<td>&nbsp;</td>'+
                                                                                          '<td>&nbsp;</td>'+
                                                                                          '<td>'+pmt_amount+'</td>'+
                                                                                          '</tr>');
                                                      }
                                                  } else {
                                                      pvs.alert('Unable to save products:\n'+response);
                                                  }
                                              }
                                             );
                            }
                           });
    } else {
        pvs.alert('Save order first.');
    }
};

customer_add_order_item = function(order_id) {
    if ($_('#customer_id')) {
        pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/add_order_item_dialog/' + $_('#customer_id')+'/'+order_id}),
                            title:'Add Order Item',
                            width: $(window).width()*.60,
                            height:$(document).height()*.75,
                            dialog_id: 'dialog4',
                            on_ok:
                            function() {
                                $('.product_chk:checked').each(function(i) {
                                    var product_id = this.value;
                                    var quantity = $_('#quant_'+this.value);
                                    pvs.ajax.call(pvs.ajax.api({root: '/crm/product/json/'+product_id+'/'+$_('#campaign_id')}),
                                                  function(response) {
                                                      var rndid = Math.floor(Math.random()*1000)
                                                      var prod = pvs.json.decode(response);
                                                      oi_ids.push(rndid+'_');
                                                      $('#result_list_header').after('<tr id="oi_'+rndid+'_">'+
                                                                                     '<td>'+
                                                                                     '<input type="hidden" id="product_id'+rndid+'_" name="product_id'+rndid+'_" value="'+prod.product_id+'"/>'+
                                                                                     '<img src="/public/images/icons/silk/delete.png" border="0" onclick="customer_delete_order_item('+rndid+'_)">'+
                                                                                     '</td>'+
                                                                                     '<td>&nbsp;</td>'+
                                                                                     '<td width="25%">'+prod.name+'</td>'+
                                                                                     '<td><input type="text" value="'+prod.unit_price+'" size="10" onblur="customer_order_recalc()" name="unit_price['+rndid+'_]" id="unit_price'+rndid+'_"></td>'+
                                                                                     '<td><input type="text" value="'+quantity+'" size="10" onblur="customer_order_recalc()" name="quantity['+rndid+'_]" id="quantity'+rndid+'_"></td>'+
                                                                                     '<td id="oi_total_'+rndid+'_">'+prod.unit_price+'</td>'+
                                                                                     '</tr>');
                                                  });
                                });
                            }
                           });
    } else {
        pvs.alert('Create customer first.');
    }
};

customer_edit_order = function(order_id) {
    pvs.browser.goto_url('/crm/customer/edit_order_dialog/'+$_('#customer_id')+'/'+order_id);
};

customer_edit_order_prep = function() {
    customer_order_items_to_delete = [];
    customer_order_recalc();
    pvs.ui.init_datepicker('#order_create_dt');
};

customer_edit_order_submit = function() {
    pvs.dialog.wait();
    var ois = {};
    for (var i=0 ; i<oi_ids.length ; i++) {
        var oid = oi_ids[i];
        if (oid && oid != -1) {
            ois[oid] = {unit_price : $_('#unit_price'+oid+''),
                        quantity : $_('#quantity'+oid+''),
                        product_id : $_('#product_id'+oid+'')};
        }
    }

    pvs.ajax.post_array(pvs.ajax.api({root: '/crm/customer/edit_order/'+$_('#customer_id')+'/'+$_('#oi_order_id')}),
                        function(response) {
                            if (pvs.is_true(response)) {
                                customer_show_orders();
                                customer_show_balance();
                            } else {
                                pvs.dialog.unwait();
                                pvs.alert('Unable to save order:\n'+response);
                            }
                        },
                        {order_items_to_delete: customer_order_items_to_delete,
                         order_items: ois,
                         shipping_total: $_('#shipping_total') ? parseFloat($_('#shipping_total')).toFixed(2) : '0.00',
                         create_dt: $_('#order_create_dt')
                        }
                       );
};

customer_cancel_order = function(order_id) {
    pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/dialog/crm/customer.cancel_order'}),
                        title:'Cancel Order',
                        width:285,
                        height:300,
                        on_ok:
                        function() {
                            pvs.ajax.post_array(pvs.ajax.api({root: '/crm/customer/cancel_order/'+$_('#customer_id')}),
                                                function(response) {
                                                    if (pvs.is_true(response)) {
                                                        $('#flashes').append('Deleted order.');
                                                        customer_show_orders()
                                                    } else {
                                                        pvs.alert('Unable to save products:\n'+response);
                                                    }
                                                },
                                                {
                                                    order_id : order_id,
                                                    cancel_reason: $_('#cancel_reason')
                                                }
                                               );
                        }
                       });
};

customer_cancel_billing = function(journal_id) {
    var answer = confirm("Delete billing?")
    if (answer) {
        pvs.ajax.call(pvs.ajax.api({root: '/crm/customer/cancel_billing/'+$_('#customer_id')+'/'+journal_id}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              $('#flashes').append('Billing cancelled.');
                              customer_show_billings();
                          } else {
                              pvs.alert('Unable to cancel billing:\n'+response);
                          }
                      });
    }
};

customer_order_recalc = function() {
    if ($('#frm_edit_order').length > 0) {
        var total = 0.0;
        for (var i=0 ; i<oi_ids.length ; i++) {
            var oid = oi_ids[i];
            if (oid && oid != -1) {
                var unit_price = $_('#unit_price'+oid+'')
                if (unit_price) unit_price = parseFloat(unit_price);
                var quantity = $_('#quantity'+oid+'');
                if (quantity) quantity = parseFloat(quantity);
                var sub_tot = unit_price * quantity;
                pvs.ui.set('#oi_total_'+oid, '$'+sub_tot.toFixed(2));
                total += sub_tot;
            }
        }
        if ($_('#shipping_total')) {
            total += parseFloat($_('#shipping_total'));
        }
        pvs.ui.set('#oi_total_price', '$' + total.toFixed(2));
    }
};

customer_delete_order_item = function(order_item_id) {
    if (oi_ids.length > 1) {
        customer_order_items_to_delete.push(order_item_id);
        for (var i=0 ; i<oi_ids.length ; i++) {
            if (oi_ids[i] == order_item_id) {
                delete oi_ids[i]
            }
        }

        $('#oi_'+order_item_id).fadeOut(function() {
            $('#oi_'+order_item_id).remove();
        });
        customer_order_recalc();
    } else {
        pvs.alert("You can't delete the last item in an order.");
    }
};

var customer_order_items_to_delete = [];

customer_edit_appointment = function() {
    appointment_edit();
};

customer_orders_list_init = function() {
    //setup the clickable rows in the order list to expand contract.
    $('.clickable').click(function() {
        var order_id = $(this).parent().attr('order_id');
        $('.detail_'+order_id).toggle();
    });
};

pvs.onload.push(customer_orders_list_init);

customer_show_appointments = function(offset) {
    if ($_('#customer_id')) {
        customer_show_detail();
        pvs.ui.menu_highlight('link_appointments');
        pvs.dialog.wait();
        $('#div_customer_detail').load(pvs.ajax.dialog({root: '/plugin/appointment/show_appointments/'+$_('#customer_id'),
                                                        offset: offset}),
                                      function() {
                                          pvs.dialog.unwait();
                                      });
    }
};

customer_show_billing = function(journal_id) {
    pvs.dialog.display({url:pvs.ajax.dialog({root: '/crm/customer/show_billing_dialog/'+$_('#customer_id')+'/'+journal_id}),
                        title: 'Billing Entry',
                        width:680,
                        height:400});
};

customer_show_balance = function() {
    pvs.ajax.call(pvs.ajax.dialog({root:'/crm/customer/get_balance/'+$_('#customer_id')}),
                  function(balance) {
                      $('#balance').val(parseFloat(balance).toFixed(2));
                  });
};

pvs.onload.push(function () {
    if ($('#prod_complete2').length && window.products) {
        customer_barcode_prep_add_product_autocomplete(products, product_ids);
    }

    if ($('#customer_form').length) {
        $('#customer_form').validate(
            pvs.validate.options(
                {
                    fname: 'required',
                    lname: 'required',
                    
                    //password: 'required',
                    email: {
                        required: true,
                        email: true
                    },
                    state: {
                        maxlength: 2
                    },
                    zip: {
                        digits: true,
                        maxlength: 5
                    },
                    phone: { phoneUS: true },
                    alt_phone: { phoneUS: true },
                    fax: { phoneUS: true }
                }
            )
        );
    }
});

pvs.onload.push(function() {
    $('#lname_complete').typeahead({
        source: function(typeahead, query) {
            $.ajax({
                url: "/crm/customer/autocomplete",
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
                        return_list[i] = {id: data[i].customer_id, value: data[i].name};
                    }
                    typeahead.process(return_list);
                }
            });
        },
        onselect: function(obj) {
            pvs.browser.goto_url('/crm/customer/edit/'+obj.id);
        }
    });
});


customer_show_edit = function() {
    pvs.browser.goto_url('/crm/customer/edit/'+$_('#customer_id'));
};


customer_show_orders = function() {
    pvs.browser.goto_url('/crm/customer/show_orders/'+$_('#customer_id'));
};