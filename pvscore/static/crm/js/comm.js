
comm_init = function() {
    pvs.form.init_editors_exact('data');
};


/* KB: [2010-10-22]: Show only the editor portion who's type is specified. */
comm_type_change = function() {
    if ($_('#type')) {
        $("div[id^='row_']").fadeOut(function() {
            $("div[id='row_"+$_('#type')+"']").fadeIn();
        });
    }
};

pvs.onload.push(comm_type_change);

comm_insert_token = function(token) {
    var ed = tinyMCE.get('data');
    ed.setContent(ed.getContent() + token);
};

comm_fixup_message = function() {
    /*
        tinyMCE.init({
            height: 235, width: 540,
	    mode : "exact",
            elements: "message",
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
        */
};