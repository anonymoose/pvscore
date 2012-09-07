appointment_init_calendar = function(id, name) {
    pvs.ui.init_datepicker(id);
};

pvs.onload.push(function() {
  appointment_init_calendar('#a_start_dt'); 
});

appointment_edit = function(appointment_id, year, month, current_day) {
    var url = pvs.ajax.dialog({root: '/crm/appointment/edit/'+appointment_id});
    var title = 'Edit Appointment';
    if (!appointment_id) {
        url = pvs.ajax.dialog({root: '/crm/appointment/new', customer_id: $_('customer_id')});
        title = 'Add Appointment';
    }
    pvs.dialog.display({url: url,
                       title: title,
                       width:590, 
                       height:400,
                       validator: {
                           form : '#appointment_form',
                           rules : {
                               a_title: 'required',
                               a_phone: { required: true, phoneUS: true },
                               a_start_dt: 'required'
                           }
                       },
                       after_display_impl:
                       function() {
                           appointment_init_calendar('#start_dt'); 
                           if ($_('#a_title') == '') {
                               if ($_('#fname') && $_('#lname')) {
                                   pvs.ui.set('#a_title', $_('#fname') + ' ' + $_('#lname')
                                             + ($_('#title') || $_('#company') ? ' - '  : '')
                                             + ($_('#title') ? $_('#title') + ', ' : '') 
                                             + ($_('#company') ? $_('#company') + '' : ''));
                               }
                           }
                           if ($_('#a_phone') == '') {
                               pvs.ui.set('#a_phone', $_('#phone'));
                           }
                           if ($_('#a_start_dt') == '' && year && month && current_day) {
                               pvs.ui.set('#a_start_dt', year+'-'+month+'-'+current_day)
                           }
                       },
                       on_ok: 
                       function() {
                           pvs.form.post('#appointment_form', 
                                         pvs.ajax.api({root: '/crm/appointment/save', customer_id: $_('#customer_id')}),
                                         function(response) {
                                             if (pvs.is_true(response)) {
                                                 $('#flashes').append('Saved appointment.');
                                                 if (pvs.dom.is_defined('customer_show_appointments')) {
                                                     customer_show_appointments();
                                                 } else {
                                                     window.location.reload(true);
                                                 }
                                             } else {
                                                 pvs.alert('Unable to save appointments:\n'+response);
                                             }
                                         });
                       }});
};
