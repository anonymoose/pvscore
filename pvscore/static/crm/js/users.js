
/* KB: [2011-08-19]: @deprecated users.js :: users_change_password */
users_change_password = function() {
    pvs.dialog.display({url:pvs.ajax.url({root: '/crm/users/dialog/crm/users.change_password'}),
                        title:'Change Password',
                        width:550, 
                        height:200,
                        on_ok: 
                        function() {
                            pvs.form.post('#div_change_password',
                                          pvs.ajax.url({root: '/crm/users/save_password',
                                                        username: $_('#existing_username'),
                                                        pfx: 'dlg'}),
                                          function(response) {
                                              if (!pvs.is_true(response)) {
                                                 pvs.dialog.failure(response);
                                              }
                                          });
                        }});
};

users_change_email_type = function() {
    if ($_('#email_type') == 'Google') {
        $('#email_smtp_server').val('smtp.gmail.com:587');
        $('#email_imap_server').val('imap.gmail.com:993');
    } else {
        $('#email_smtp_server').val('');
        $('#email_imap_server').val('');
    }
};

pvs.onload.push(function() {
    $('#frm_users').validate(
        pvs.validate.options(
            {
                fname: 'required',
                lname: 'required',
                password: 'required',
                confirm: 'required',
                email: { 
                    required: true, 
                    email: true 
                }
            }
        )
    );
});