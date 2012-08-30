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
    if ($('#frm_product').length || $('#frm_category').length) {
        tinyMCE.init({
            height: 190, //width: ($('#div_product_edit').width()*.95),
	    mode : "textareas",
	    theme : "advanced",
            plugins: '',
            theme_advanced_buttons1 : "bold,italic,underline,separator,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink,separator,code",
            theme_advanced_buttons2 : "",
            theme_advanced_buttons3 : "",
	    theme_advanced_toolbar_location : "top",
	    theme_advanced_toolbar_align : "left",
	    theme_advanced_statusbar_location : "none",
	    theme_advanced_resizing : true
        });
    }
};

var _asset_id = null;

product_picture_edit_image = function() {
    url = '/cms/asset/add_picture';
    pvs.dialog.display({url:pvs.ajax.api({root: url}),
                        title: 'Add Image',
                        width:830,
                        height:520,
                        after_display_impl:
                        function() {
                            var url = pvs.ajax.api({root: '/cms/asset/upload_to_company/'+$_('#company_id')+'/Product/'+$_('#product_id')});
                            $('#file_upload').uploadify({
                                'uploader'     : '/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/uploadify.swf',
                                'script'       : url,
                                'cancelImg'    : '/public/js/jquery-1.4.2/jquery.uploadify-v2.1.4/cancel.png',
                                'folder'       : '/images',
                                'fileExt'      : '*.jpg;*.gif;*.png',
                                'scriptAccess' : 'sameDomain',
                                'wmode'        : 'transparent',
                                'auto'         : true,
                                'onComplete'   : function(event, ID, fileObj, response, data) {
                                    _asset_id = response;
                                    $('#uploaded_image').append('<img id="up_pi_'+_asset_id+'" src="/cms/asset/show/'+_asset_id+'" border="0"/>');
                                },
                                'onError'      : function (event,ID,fileObj,errorObj) {
                                    pvs.alert(errorObj.type + ' Error: ' + errorObj.info);
                                }
                            });
                        },
                        on_before_close:
                        function() {
                            _asset_id = null;
                            return true;
                        },
                        on_ok:
                        function() {
                            $('#product_images').append('<img id="pi_'+_asset_id+'" src="/cms/asset/show/'+_asset_id+'" border="0" onclick="product_picture_delete_image('+_asset_id+', true)"/>');
                        },
                        on_cancel:
                        function() {
                            product_picture_delete_image(_asset_id);
                        }
                });
};

product_picture_delete_image = function(asset_id, do_confirm) {
    if (do_confirm && !confirm('Delete Image?')) {
        return false;
    }
    if (asset_id) {
        pvs.ajax.call(pvs.ajax.api({root: '/cms/asset/delete/'+asset_id}),
                      function(response) {
                          if (pvs.is_true(response)) {
                              $('#pi_'+asset_id).remove()
                          } else {
                              pvs.alert(response);
                          }
                      });
    }
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

pvs.onload.push(function() {
    $('#product_search').typeahead({
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
                        return_list[i] = {id: data[i].product_id, value: data[i].name};
                    }
                    typeahead.process(return_list);
                }
            });
        },
        onselect: function(obj) {
            pvs.browser.goto_url('/crm/product/edit/'+obj.id);
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
		    se = "<img src='/public/images/icons/silk/disk.png' alt='Save Changes' title='Save Changes' onclick=\"product_inventory_save('"+cl+"');\"  />";
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
