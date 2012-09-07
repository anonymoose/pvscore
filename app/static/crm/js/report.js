
report_setup_textarea = function(id) {
    if ($('#sql').length) {
        var maxwidth = $('#frm_report').width()*.9;
        CodeMirror.fromTextArea('sql', {
            height: "650px", width: maxwidth+"px",
            parserfile: "../contrib/sql/js/parsesql.js",
            stylesheet: "/static/js/codemirror/CodeMirror-0.91/contrib/sql/css/sqlcolors.css",
            path: "/static/js/codemirror/CodeMirror-0.91/js/",
            textWrapping: false
        });
        
        CodeMirror.fromTextArea('column_names', {
            height: "150px", width: maxwidth+"px",
            parserfile: ["tokenizejavascript.js", 
                         "parsejavascript.js"],
            stylesheet: "/static/js/codemirror/CodeMirror-0.91/css/jscolors.css",
            path: "/static/js/codemirror/CodeMirror-0.91/js/",
            textWrapping: false,
            autoMatchParens: true
        });
    
        CodeMirror.fromTextArea('column_model', {
            height: "150px", width: maxwidth+"px",
            parserfile: ["tokenizejavascript.js", 
                         "parsejavascript.js"],
            stylesheet: "/static/js/codemirror/CodeMirror-0.91/css/jscolors.css",
            path: "/static/js/codemirror/CodeMirror-0.91/js/",
            textWrapping: false,
            autoMatchParens: true
        });
    
        CodeMirror.fromTextArea('on_dbl_click', {
            height: "150px", width: maxwidth+"px",
            parserfile: ["tokenizejavascript.js", 
                         "parsejavascript.js"],
            stylesheet: "/static/js/codemirror/CodeMirror-0.91/css/jscolors.css",
            path: "/static/js/codemirror/CodeMirror-0.91/js/",
            textWrapping: false,
            autoMatchParens: true
        });
    }
};

report_edit = function() {
    if ($_('#report_id')) {
        pvs.browser.goto_url('/crm/report/edit/'+$_('#report_id'));
    }
};

var report_grid = null;

report_show = function(height, width) {
    if ($_('#report_id') && $('#rpt').length > 0) {
        if (report_grid) {
            report_grid.GridDestroy()
            $('#results_container').append('<table id="results"></table>');
            $('#pager_container').append('<table id="pager"></table>');
        }
        var col_names = '';
        eval('col_names = '+$_('#column_names'));
        var col_model = '';
        eval('col_model = '+$_('#column_model'));
        var function_dbc;
        if ($_('#on_dbl_click')) {
            eval('function_dbc = function(row) {'+$_('#on_dbl_click')+'}');
        }
        
        report_grid = $("#results").jqGrid({        
   	    url: pvs.ajax.dialog({root: '/crm/report/results/'+$_('#report_id'),
                                  rpt_start_dt : $_('#rpt_start_dt'),
                                  rpt_end_dt : $_('#rpt_end_dt'),
                                  rpt_campaign_id : $_('#rpt_campaign_id'),
                                  rpt_company_id : $_('#rpt_company_id'),
                                  rpt_vendor_id : $_('#rpt_vendor_id'),
                                  rpt_user_id : $_('#rpt_user_id'),
                                  rpt_product_id : $_('#rpt_product_id'),
                                  rpt_p0 : $_('#rpt_p0'),
                                  rpt_p1 : $_('#rpt_p1'),
                                  rpt_p2 : $_('#rpt_p2')
                                 }),
	    datatype: "json",
            height: (height ? height : 420),
            width: (width ? width : 600),
   	    colNames: col_names,
   	    colModel: col_model,
   	    rowNum:100,
   	    rowList:[100,200,300],
   	    pager: '#pager',
            sortname: 'fname',
            viewrecords: true,
            sortorder: 'asc',
            caption: $_('#description'),
            ondblClickRow: function_dbc
        }).navGrid("#pager",{edit:false,add:false,del:false});
    }
};

G = function(method, p0, p1, p2, p3) {
    return $("#results").jqGrid(method, p0, p1, p2, p3);
};

pvs.onload.push(function() {
    report_show($('#rpt').height()*0.63, $('#rpt').width()*0.95);
    report_setup_textarea();
});

report_refresh = function() {
    pvs.browser.goto_url(pvs.ajax.url({root: '/crm/report/show/'+$_('#report_id'),
                                       rpt_start_dt : $_('#rpt_start_dt'),
                                       rpt_end_dt : $_('#rpt_end_dt'),
                                       rpt_campaign_id : $_('#rpt_campaign_id'),
                                       rpt_company_id : $_('#rpt_company_id'),
                                       rpt_vendor_id : $_('#rpt_vendor_id'),
                                       rpt_user_id : $_('#rpt_user_id'),
                                       rpt_product_id : $_('#rpt_product_id'),
                                       rpt_p0 : $_('#rpt_p0'),
                                       rpt_p1 : $_('#rpt_p1'),
                                       rpt_p2 : $_('#rpt_p2')}));
};

report_export = function() {
    pvs.browser.open_window('csv', pvs.ajax.dialog({root: '/crm/report/results_export/'+$_('#report_id'),
                                   rpt_start_dt : $_('#rpt_start_dt'),
                                   rpt_end_dt : $_('#rpt_end_dt'),
                                   rpt_campaign_id : $_('#rpt_campaign_id'),
                                   rpt_company_id : $_('#rpt_company_id'),
                                   rpt_vendor_id : $_('#rpt_vendor_id'),
                                   rpt_user_id : $_('#rpt_user_id'),
                                   rpt_product_id : $_('#rpt_product_id'),
                                   rpt_p0 : $_('#rpt_p0'),
                                   rpt_p1 : $_('#rpt_p1'),
                                   rpt_p2 : $_('#rpt_p2')}), 20, 20);
};


