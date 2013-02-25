product_show_edit= function() {
    $('#div_product_detail').hide('slow', function() {
        $('#div_product_edit').show('fast');
    });
};

product_show_detail = function() {
    $('#div_product_edit').hide('fast', function() {
        $('#div_product_detail').show('slow');
    });
};

product_dashboard_find = function() {
    $('#product_find_subsection').css('visibility', 'visible');
};

product_setup_textarea = function(id) {
    pvs.form.init_editors();
};

product_delete = function() {
    if ($_('#product_id')) {
        var answer = confirm("Really Delete Product?")
        if (answer) {
            pvs.ajax.call(pvs.ajax.api({root: '/crm/product/delete/'+$_('#product_id')}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              pvs.alert('Product Deleted');
                              pvs.browser.goto_url('/crm/product/list');
                          } else {
                              pvs.alert('Unable to delete:\n'+response);
                          }
                      });
        }
    } else {
        pvs.alert('Save product first');
    }
};


product_picture_delete_image = function(asset_id, do_confirm) {
    if (do_confirm && !confirm('Delete Image?')) {
        return false;
    }
    if (asset_id) {
        pvs.ajax.call(pvs.ajax.api({root: '/crm/product/delete_picture/'+$_('#product_id')+'/'+asset_id}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              $('#pi_'+asset_id).remove()
                          } else {
                              pvs.alert(response);
                          }
                      });
    }
};

var _asset_id = null;
pvs.onload.push(function() {
    if ($('#file_upload').length) {
        var url = pvs.ajax.api({root: '/crm/product/upload_picture/'+$_('#product_id')});
        $('#file_upload').uploadify({
            'uploader'     : '/static/js/jquery/uploadify/uploadify.swf',
            'script'       : url,
            'cancelImg'    : '/static/js/jquery/uploadify/cancel.png',
            'folder'       : '/images',
            'fileExt'      : '*.jpg;*.gif;*.png',
            'scriptAccess' : 'sameDomain',
            'wmode'        : 'transparent',
            'auto'         : true,
            'onComplete'   : function(event, ID, fileObj, response, data) {
                pvs.browser.window_refresh();
            },
            'onError'      : function (event,ID,fileObj,errorObj) {
                pvs.alert(errorObj.type + ' Error: ' + errorObj.info);
            }
        });
    }
});

/* KB: [2013-02-24]: Also used in customer.js prod_complete1 */
product_name_complete_reference = {};

pvs.onload.push(function() {
    $('#product_search').typeahead({
        source: function(query, process) {
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
                    product_name_complete_reference = {};
                    while (i > 0) {
                        i--;
                        product_name_complete_reference[data[i].name] = data[i].product_id;
                        return_list[i] = data[i].name;
                    }
                    process(return_list);
                }
            });
        },
        updater: function(item) {
            var product_id = product_name_complete_reference[item];
            pvs.browser.goto_url('/crm/product/edit/'+product_id);
        }
    });
});

pvs.onload.push(function() {
    $('#' + $('#product_menu_selected').val()).addClass('active');
});

product_show_orders = function() {
    product_show_list_impl('orders');
};

pvs.onload.push(function() {
    $('#frm_discount').validate(
        pvs.validate.options(
            {
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
            })
    );
});

product_validate_product = function() {
    $('#frm_product').validate(
        pvs.validate.options(
            {
                name: 'required',
                company_id: 'required',
                type: 'required',
                //sku: 'required',
                unit_cost: {
                    number: true,
                    min: 0.0
                },
                handling_price: {
                    number: true,
                    min: 0.0
                },
                weight: {
                    number: true,
                    min: 0.0
                },
                prod_inventory: {
                    number: true,
                },
                inventory_par: {
                    number: true,
                }
            })
    );
};

product_validate_product_attribute = function() {
    $('#frm_product').validate(
        pvs.validate.options(
            {
                name: 'required',
                attr_class: 'required',
                company_id: 'required',
                //sku: 'required',
                unit_cost: {
                    number: true,
                    min: 0.0
                },
                handling_price: {
                    number: true,
                    min: 0.0
                },
                weight: {
                    number: true,
                    min: 0.0
                },
                prod_inventory: {
                    number: true,
                },
                inventory_par: {
                    number: true,
                }
            })
    );
};


var lastsel;
pvs.onload.push(function() {
    if ($('#inventory_container').length) {
        var fn = function(id) {
	    if(id && id!==lastsel){
		jQuery('#inventory').jqGrid('restoreRow',lastsel);
		jQuery('#inventory').jqGrid('editRow',id,true);
		lastsel=id;
	    }
	};

        $("#inventory").jqGrid({
   	    url: pvs.ajax.dialog({root: '/crm/product/inventory_list'}),
	    datatype: "json",
            height: 420,
            width: 1100,
   	    colNames: column_names,
   	    colModel: column_model,
   	    rowNum: 2000,
   	    //rowList: [100,200,300],
   	    pager: '#pager',
            sortname: 'fname',
            viewrecords: true,
            sortorder: 'asc',
            gridComplete: function(){
		var ids = jQuery("#inventory").jqGrid('getDataIDs');
		for(var i=0;i < ids.length;i++){
		    var cl = ids[i];
		    se = "<img src='/static/icons/silk/disk.png' alt='Save Changes' title='Save Changes' onclick=\"product_inventory_save('"+cl+"');\"  />";
		    jQuery("#inventory").jqGrid('setRowData',ids[i],{act:se});
		}
	    },
            onSelectRow: fn,
            ondblClickRow: fn,
	    editurl: "/crm/product/save_inventory",
        }).navGrid("#pager",{edit:true,add:false,del:false,search:false});
    }
});

product_inventory_save = function(product_id) {
    jQuery('#inventory').saveRow(product_id);
};


/*
product_show_list_impl = function(name, offset) {
    if ($_('#product_id')) {
        product_show_detail()
        pvs.ui.menu_highlight('link_'+name);
        $('#div_product_detail').load(pvs.ajax.dialog({root: '/crm/product/show_'+name+'/'+$_('#product_id'),
                                                      offset: offset}));
    }
};

product_show_history = function() {
    product_show_list_impl('history');
};
product_show_sales = function() {
    product_show_list_impl('sales');
};
product_show_returns = function() {
    product_show_list_impl('returns');
};
product_show_purchases = function() {
    product_show_list_impl('purchases');
};


product_gen_barcode = function(product_id) {
    if ($_('#product_id') && $('#barcode').length) {
        var btype = "ean8"; //        "ean13""std25""int25""code11""code39""code93""code128""codabar""msi""datamatrix"
        $("#barcode").html('').show().barcode(pvs.string.pad_left($_('#product_id'), 7, '0'), btype, {
            output:'canvas',
            bgColor: '#FFFFFF',
            color: '#000000',
            barWidth: 1,
            barHeight: 50,
            moduleSize: 5,
            addQuietZone: 0
        });
    }
};
pvs.onload.push(product_gen_barcode);

product_gen_barcode_impl = function(product_id, canvas_id) {
    var btype = "ean8"; //        "ean13""std25""int25""code11""code39""code93""code128""codabar""msi""datamatrix"
    $(canvas_id).html('').show().barcode(pvs.string.pad_left(product_id, 7, '0'), btype, {
        output:'canvas',
        bgColor: '#FFFFFF',
        color: '#000000',
        barWidth: 2,
        barHeight: 75,
        moduleSize: 5,
        addQuietZone: 0
    });
};

product_show_barcode = function(product_id) {
    if ($_('#product_id')) {
        pvs.browser.open_window('barcode',
                                pvs.ajax.dialog({root: '/crm/product/show_barcode/'+$_('#product_id')}),
                                100, 100);
    }
};
*/
