//

pvs_aloha_onsave = function() {
    var content_data = Aloha.activeEditable.getContents();
    var editable_id = Aloha.activeEditable.obj[0].id;
    if ('content' == $('#'+editable_id+'_type').val()) {
        var content_id = $('#'+editable_id+'_content_id').val();
        var name = $('#'+editable_id+'_name').val();
        $.post('/cms/content/save_ajax', {
            content_id: content_id,
            name: name,
            data: content_data
        }).done(function(response) {
            if ('True' != response) {
                alert(response);
            }
        });
    } else if ('attribute' == $('#'+editable_id+'_type').val()) {
        var pk_id = $('#'+editable_id+'_pk_id').val();
        var attr = $('#'+editable_id+'_attr').val();
        var objtype = $('#'+editable_id+'_objtype').val();
        var module = $('#'+editable_id+'_module').val();
        $.post('/cms/content/save_dynamic_attribute', {
            pk_id: pk_id,
            objtype: objtype,
            module: module,
            attr: attr,
            data: content_data.trim()
        }).done(function(response) {
            if ('True' != response) {
                alert(response);
            }
        });

    }
};