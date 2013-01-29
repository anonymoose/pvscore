;(function($) {

/*!
 * PVS wrapper library for JQuery
 * Copyright(c) 2010 Palm Valley Software, LLC.
 * http://www.palmvalleysoftware.comp
 */

pvs = function(){
    pub = {
        version : '1.0',
        error_color : '#F9CCCC',
        error_color_other : 'rgb(249, 204, 204)',
        over_color : 'yellow',

        is_true : function(val) {
            return (val === true || val === 'True' || val == 'true' || val === 'Y' || val === 'y');
        },

        confirm : function(msg, title, onclick) {
            if (!title) title = 'Confirm';
            window.pvs_alert_yes = function() {
                onclick();
                $('#modal-confirm').modal('hide');
            }
            $('#modal-confirm').remove();
            $('body').append('<div id="modal-confirm" class="modal hide fade">' +
                             '    <div class="modal-header">' +
                             '      <a href="#" class="close">&times;</a>' +
                             '      <h3>'+title+'</h3>' +
                             '    </div>' +
                             '    <div class="modal-body">' +
                             '      <p>'+msg+'</p>' +
                             '      <p>Do you want to proceed?</p>' +
                             '    </div>' +
                             '    <div class="modal-footer">' +
                             '      <a href="#" onclick="pvs_alert_yes()" class="btn danger">Yes</a>' +
                             '      <a href="#" class="btn btn-primary close">No</a>' +
                             '    </div>' +
                             '</div>');

            $('.close').click(function() {
                $('#modal-confirm').modal('hide');
            });
            $('#modal-confirm').modal({ backdrop: true });
            $('#modal-confirm').modal('show');
        },

        alert : function(msg, title, onclick) {
            if (!title) title = "Alert";
            window.pvs_alert_ok = function() {
                if (onclick) {
                    onclick();
                }
                window.pvs_alert_ok = null;
            }
            $('#modal-alert').remove();
            $('body').append('<div id="modal-alert" class="modal hide fade">' +
                             '    <div class="modal-header">' +
                             '      <a href="#" class="close">&times;</a>' +
                             '      <h3>'+title+'</h3>' +
                             '    </div>' +
                             '    <div class="modal-body">' +
                             '      <p>'+msg+'</p>' +
                             '    </div>' +
                             '    <div class="modal-footer">' +
                             '      <a href="#" class="btn btn-primary close" onclick="pvs_alert_ok()">Ok</a>' +
                             '    </div>' +
                             '</div>');
            $('.close').click(function() {
                $('#modal-alert').modal('hide');
            });
            $('#modal-alert').modal({ backdrop: true });
            $('#modal-alert').modal('show');
        },

        each : function(arr, func) {
            $.each(arr, func);
        }
    };

    return pub;
}();

pvs.validate = function() {
    pub = {
        options : function(rules, messages) {
            return {
                //errorClass:'error alert alert-error alert-pvs',
                errorClass:'error alert-pvs',
                validClass:'success',
                errorElement:'span',
                /*
                highlight: function (element, errorClass, validClass) {
                    //$(element).siblings('label').children('span').remove();
                    //$(element).parent().addClass(errorClass).removeClass(validClass);
                },
                unhighlight: function (element, errorClass, validClass) {
                    //$(element).siblings('label').children('span').remove();
                    //$(element).parent().addClass(validClass).removeClass(errorClass);
                },
                */
                errorPlacement : function(error, element) {
                    $(element).siblings('label').children('span').remove();
                    error.appendTo($(element).siblings('label'));
                },
                //errorLabelContainer: '#hidden',
                rules : rules,
                messages: messages
            };
        }
    };
    return pub;
}();


pvs.string = function(){
    pub = {
        urlencode : function(str) {
            return escape(str).replace('+', '%2B').replace('%20', '+').replace('*', '%2A').replace('/', '%2F').replace('@', '%40');
        },

        urldecode : function(str) {
            return unescape(str.replace('+', ' '));
        },

        get_date_from_format : function(val, format) {
            return Date.parseDate(val, format);
        },

        nvl : function(is, defalt) {
            if (is == '' || is == null) {
                return defalt;
            }
            return is;
        },

        return_digits : function(val) {
	    var retval = '';
	    var digits = '0123456789';

	    for (x=0; x<val.length; x++) {
		if (digits.indexOf(val.charAt(x)) >= 0) {
		    retval += val.charAt(x);
		}
	    }
	    return retval;
        },

        normalize_str : function(str) {
            return (str ? str : '');
        },

        clean_phonenumber : function(num) {
            if (num != null && num != '') {
                num = pvs.string.trim(num);
                num = num.replace(/[- ]/g, '').replace(/\./g, '').replace(/\(/g, '').replace(/\)/g, '');
                return num;
            }
        },

        trim : function(str) {
            var s = str;
            if (s) {
                s = s.replace(/^\s*/,'').replace(/\s*$/, '');
            }
	    return s;
        },

        /* 2007-11-09 13:41:22  -->  09/11/2007 */
        render_date : function(val) {
            if (val) {
                var ymd = val.substr(0,10);
                ymd = ymd.split('-');
                return ymd[1]+'/'+ymd[2]+'/'+ymd[0];
            } else {
                return '';
            }
        },

        render_date_time : function(val) {
            if (val) {
                return val;
            } else {
                return '';
            }
        },

        render_no_html : function(val) {
            if (val) {
                return val.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            } else {
                return '';
            }
        },

        render_phone : function(val) {
            if (val) {
                var len = val.length;
                var last4 = val.substr((len-4), 4);
                var mid3 = val.substr((len-7), 3);
                var area = val.substr((len-10), 3);
                return '('+area+') '+mid3+'-'+last4;
            } else {
                return '';
            }
        },

        render_float : function(val) {
            if (!isNaN(val)) {
    	        // force the variable to be a number so we can format it
    	        val = Number(val);
                val = val.toFixed(2);
            }
            return val;
        },

        render_hyperlink : function(val) {
            if (val) {
                if (!val.match(/^http:\/\//i)) {val = 'http://' + val;}
                val = '<a href="' + val + '" target="_blank">' + val + '</a>';
            }
            return val;
        },

        pad_left : function(str, n, pad) {
	    t = '';
	    if(n>str.length){
		for(i=0;i < n-str.length;i++){
		    t+=pad;
		}
	    }
	    return t+str;
        },

        pad_right : function(str, n, pad) {
	    t = str;
	    if(n>str.length){
		for(i=0;i < n-str.length;i++){
		    t+=pad;
		}
	    }
	    return t;
        }
    };

    return pub;
}();

pvs.cookie = function(){
    pub = {
        set : function(name, value, exp_y, exp_m, exp_d, path, domain, secure) {
            var cookie_string = name + "=" + escape(value);
            if (!exp_y)  {
                var now = new Date(exp_y, exp_m, exp_d);
                exp_y = now.getYear()+10;
                exp_d = 1;
                exp_m = 1;
            }

            var expires = new Date(exp_y, exp_m, exp_d);
            cookie_string += "; expires=" + expires.toGMTString();

            if (path) {
                cookie_string += "; path=" + escape(path);
            }

            if (domain) {
                cookie_string += "; domain=" + escape(domain);
            }

            if (secure) {
                cookie_string += "; secure";
            }

            document.cookie = cookie_string;
        },

        get : function(cookie_name){
            var results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
            if (results) {
                return unescape(results[2]);
            }
            return null;
        },

        remove : function(cookie_name) {
            var cookie_date = new Date();  // current date & time
            cookie_date.setTime(cookie_date.getTime() - 1);
            document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
        }
    };

    return pub;
}();

pvs.browser = function(){
    pub = {
        get_os : function() {
	    var ua=navigator.userAgent.toLowerCase(),
	    is=function(t){ return ua.indexOf(t) != -1; },
	    b=(!(/opera|webtv/i.test(ua))&&/msie (\d)/.test(ua))?('ie ie'+RegExp.$1):is('gecko/')? 'gecko':is('opera/9')?'opera opera9':/opera (\d)/.test(ua)?'opera opera'+RegExp.$1:is('konqueror')?'konqueror':is('applewebkit/')?'webkit safari':is('mozilla/')?'gecko':'',
	    os=(is('x11')||is('linux'))?' linux':is('mac')?' mac':is('win')?' win':'';
            return os;
        },

        is_browser : function(which) {
	    var ua = navigator.userAgent.toLowerCase(),
            is = function(t){ return ua.indexOf(t) != -1; };
            return is(which);
        },

        window_refresh : function() {
            window.location.reload(true);
        },

        set_status : function(msg) { window.status = msg; },

        open_window : function(windowName, url, width, height) {
            var winl = 0;
            var wint = 0;
            var newFeatures = "directories=no, width="+width+", height="+height+", menubar=no, location=no, status=no, scrollbars=yes, resizable=yes, left="+winl+", top="+wint;
            var win = window.open(url, windowName, newFeatures);
            return win;
        },

        open_full_window : function(windowName, url) {
            var win = window.open(url, windowName);
            return win;
        },

        goto_url : function(url) {
            window.location = url;
        }
    };
    return pub;
}();

pvs.dom = function(){
    pub = {
        get_value : function(id) {
            if (id) {
                var el = $(id);
                try {
                    if (el && el.length > 0) {
                        el = el[0]
                        if (el.tagName == 'DIV' || el.tagName == 'SPAN' || el.tagName == 'DD') {
                            return el.innerHTML;
                        } else {
                            if (el.options) {
                                return pvs.form.get_select_value(el);
                            } else {
                                return el.value;
                            }
                        }
                    }
                } finally {
                    el = null;
                }
            }
        },

        display : function(ref, disp) {
            if (ref) {
                var w = $(ref)
                if (w) {
                    w.setStyle('display', (disp == true ? 'block' : 'none'));
                    (disp == true ? pvs.dom.show(ref) : pvs.dom.hide(ref));
                }
            }
        },

        hide : function(ref) {
            if (ref) {
                if (typeof ref == 'string') {
                    ref = $(ref);
                }
                if (ref) {
                    ref.style.visibility = 'hidden';
                    var selects = ref.getElementsByTagName("SELECT");
                    if (selects) {
                        for (i=0 ; i<selects.length ; i++) {
                            selects[i].style.visibility = 'hidden';
                            //                selects[i].style.display = 'block';
                        }
                    }
                }
            }
        },

        /* KB: [2010-08-16]: Pass in 'inline' to get rid of unwanted carriage returns */
        show : function(ref, display_style) {
            var ds = 'block';
            if (display_style) {ds = display_style;}

            if (ref) {
                if (typeof ref == 'string') {
                    ref = $(ref);
                }
                if (ref) {
                    if (ref.style.display == 'none') {
                        ref.style.display = ds;
                    }
                    ref.style.visibility = 'visible';
                    var selects = ref.getElementsByTagName("SELECT");
                    if (selects) {
                        for (i=0 ; i<selects.length ; i++) {
                            selects[i].style.visibility = 'visible';
                            selects[i].style.display = ds;
                        }
                    }
                }
            }
        },

        disable : function(id) {
            $(id).disabled = true;
        },

        enable : function(id) {
            $(id).disabled = false;
        },

        /**
         * Utility to walk up the DOM tree from 'ref' until a tag with 'name' is found
         * at which time a handle the 'name's element is returned.
         *
         * params
         *  ref:  The reference element in the Documents DOM
         *  name: The tag name to search for.
         */
        find_ancestor_by_tag_name : function(ref, name) {
            var t;
            var r = ref;
            while (r && r.nodeName != 'BODY' && r.nodeName != name) {
                r=r.parentNode;
            }
            if (r.nodeName == name) t = r;
            return t;
        },

        /**
         * search the child elements of 'ref's DOM tree until a tag with
         * 'name' is found at which time a handle the 'name's element is returned.
         *
         * params
         *  ref:  The reference element in the Documents DOM
         *  name: The tag name to search for.
         */
        find_child_by_tag_name : function(base, name) {
            var v = base.getElementsByTagName(name);
            var r = v.item(0);
            return r;
        },

        /**
         * Find and return the specified element, or if the element can not be found,
         * print out the specified message.
         *
         * params
         *  id:    The id of the Element to find.
         *  alert: The alert to display if the element is not found.
         */
        find_element : function(id, alertMsg) {
            var v = document.getElementById(id );
            if (v == null && alertMsg) {
                pvs.dialog.alert(id+": No such element was found in the current document!\n"+alertMsg);
            }
            return v;
        },

        /**
         * Toggle the visibility of the specified element.
         * param:
         *  ref     The object reference of the element to toggle
         */
        toggle : function(ref) {
            var n = 'none';
            var b = false;
            var shown = ref.style.display;
            if (shown=='hidden') { n='visible'; b = true;
            } else if (shown=='visible') { n='hidden'; b = false;
            } else if (shown=='none') { n='block'; b = true;
            } else if (shown=='block') { n='none'; b = false;
            }
            ref.style.display = (n ? n : shown);
            return b;
        },

        /**
         * Determine if the specified node is visible (displayed).
         */
        is_displayed : function(base) {
            var shown = base.style.display;
            if (shown=='visible' || shown=='block') return true;
            return false;
        },

        /**
         * Modify the style display property of the specified
         */
        set_displayed : function(base, bool) {
            var show = "block";
            var hide = "none";
            if (base) base.style.display = (bool ? show : hide);
        },

        /**
         * Return a NodeList representing the child nodes of the parent of
         * the specified node. Note, this will include the ref itself
         */
        get_sibling_nodes : function(base) {
            var nodes = new Array();
            if (base && base.parent) {
                nodes = base.parent.childNodes;
            }
            return nodes;
        },

        is_defined : function(variable) {
            return (typeof(window[variable]) == "undefined")?  false: true;
        },

        delete_children : function(node) {
            if (!node) return;
            while (node.hasChildNodes()) {
                pvs.dom.delete_children(node.firstChild);
                //Need to make sure there is a first child before we try to delete it.
                if(node.firstChild){
	            if (node.firstChild.removeAllListeners) {
	                node.firstChild.removeAllListeners();
	            }
                    node.removeChild(node.firstChild);
                }else{break;}
            }
        },

        destroy : function(elem_id) {
            var e = $(elem_id);
            e.remove();
            e = null;
        }
    };

    return pub;
}();

/* KB: [2010-08-16]: Set up some short cuts to commonly used dom finding functions */
var $_ = pvs.dom.get_value;

pvs.json = function() {
    pub = {
        decode : function(str) {
            if (str) {
                return jQuery.parseJSON(str);
            }
            return null;
        },

        /* KB: [2010-11-18]: Requires:
           ${h.javascript_link('/js/jquery-1.4.2/jquery.json-2.2/jquery.json-2.2.min.js')}
        */
        encode : function(obj) {
            if (obj) {
                return jQuery.toJSON(obj);
            }
            return null;
        }
    };
    return pub;
}();


pvs.form = function(){
    pub = {
        init_editors : function() {
            tinyMCE.init({
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
        },

        init_editors_exact : function(element_id) {
            tinyMCE.init({
                //height: 520, width: 800,
	        mode : "exact",
                elements: element_id,
	        theme : "advanced",
                plugins: '',

                convert_urls: false,
                forced_root_block : false,
                force_p_newlines : 'false',
                remove_linebreaks : false,
                force_br_newlines : true,              //btw, I still get <p> tags if this is false
                remove_trailing_nbsp : false,
                verify_html : false,

                theme_advanced_buttons1 : "bold,italic,underline,separator,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink,separator,code",
                theme_advanced_buttons2 : "",
                theme_advanced_buttons3 : "",
	        theme_advanced_toolbar_location : "top",
	        theme_advanced_toolbar_align : "left",
	        theme_advanced_statusbar_location : "none",
	        theme_advanced_resizing : true
            });
        },

        set_checkbox : function(id, true_val, false_val) {
            if ($(id).checked) {
                $(id).value = true_val;
            } else {
                $(id).value = false_val;
            }
        },

        /* KB: [2010-08-16]:  Get the checked value of a like-named bunch of radio buttons */
        radio_value : function(node_name) {
            var radios = document.getElementsByName(node_name);
            for (var i=0 ; i<radios.length ; i++) {
                if (radios[i].checked) {
                    return radios[i].value;
                }
            }
        },

        /**
         * create an array of input objects within the specified reference node which
         * conform to the specified namePattern (if specified).
         *
         * Params:
         *  refNode         the parent node of the target inputs
         *  namePattern     Perl5 regular expression to match (null = *)
         *
         * Returns:
         *  An array of mathing input Objects
         */
        get_inputs : function(refNode, namePattern) {
            var results = new Array();
            var re = new RegExp(namePattern);
            l = function(nodes) {
                for(i=0;i<nodes.length;i++){
                    if (namePattern) {
                        if (re.test(nodes[i].name)) {
			    if (nodes[i].type == 'radio') {
				if (nodes[i].checked) {
				    results.push(nodes[i]);
				}
			    } else {
				results.push(nodes[i]);
			    }
                        }
                    } else {
			if (nodes[i].type == 'radio') {
			    if (nodes[i].checked) {
				results.push(nodes[i]);
			    }
			} else {
			    results.push(nodes[i]);
			}
                    }
                }
            };

            l(refNode.getElementsByTagName("INPUT"));
            l(refNode.getElementsByTagName("SELECT"));
            l(refNode.getElementsByTagName("TEXTAREA"));

            return results;
        },

        filter_inputs : function(inputs, namePattern) {
            var results = new Array();
            var regExp = new RegExp(namePattern);
            for(i=0;i<inputs.length;i++){
                if (namePattern) {
                    if (regExp.test(inputs[i].name)) {
                        results.push(inputs[i]);
                    }
                } else {
                    results.push(inputs[i]);
                }
            }
            return results;
        },

        /**
         * Returns the option label for a select element. If value is not
         * passed, the label for the currently selected option is returned.
         * If value is passed, the label for the option that corresponds
         * to the passed value is returned.
         */
        get_select_label : function(select, value) {
            var l = null;
	    var opt = null;

            if(select&& select.options) {
		if (value) {
		    var i,opts = select.options;
		    for(i=0;i<opts.length;i++) {
			if(opts[i].value==value) {
			    opt = opts[i];
			    break;
			}
		    }
		} else {
		    opt = select.options[select.selectedIndex];
		}
                if(opt.label) l = opt.label;
            }
            return l;
        },

        get_select_value : function(select) {
            var v = null;
            if (select && select.options && select.selectedIndex >= 0) {
                var sOpt = select.options[select.selectedIndex];
                if (sOpt.value) v = sOpt.value;
                else v = sOpt.innerHtml;
            }
            return v;
        },

        set_select_value : function(select, value) {
            if (select && select.options) {
                var i,opts = select.options;
                for (i=0 ; i<opts.length ; i++) {
                    if (opts[i].value==value) {
                        select.selectedIndex = i;
                        select.value = value;
                        return;
                    }
                }
            }
        },

        remove_select_options : function(select) {
	    var i;
            if (select && select.options) {
                for(i=select.options.length-1;i>=0;i--) {
                    pvs.form.remove_select_option(select, i);
                }
            }
        },

        remove_select_option : function(select, i) {
            if (select && select.options) {
                select.remove(i);
            }
        },

        add_select_option : function(select, k, v, id, lbl) {
            pvs.form.set_select_option(select, select.options.length, k, v, id, lbl);
        },

        clear_multi_select_options : function(select) {
            if (select) {
                var opts = select.options;
                for (var i=0 ; i<opts.length ; i++) {
                    opts[i].selected = false;
                }
            }
        },

        set_select_option : function(select, index, k, v, id, lbl) {
            select.options[index] = new Option(v, k);
            select.options[index].id = id;
            if (lbl != null) {
                select.options[index].label = lbl;
            } else {
                select.options[index].label = v;
            }
        },

        get_select_option_count : function(select, ignore_blank) {
            var i;
	    var cnt = 0;

	    if (!select) {return cnt;}
	    var opts = select.options;

            for(i=0;i<opts.length;i++) {
		var oval = opts[i].value;
                if(!opts[i].value) {
		    if (!ignore_blank) {cnt++;}
                } else {
		    cnt++;
		}
            }
	    return cnt;
        },

        reset_field : function(id) {
            if ($('__orig_'+id)) {
                var item = $(id);
                item.value = $_('__orig_'+id);
            }
        },

        reset_form : function(div_id) {
            var inputs = pvs.form.get_inputs($(div_id));
            for(var i=0; i<inputs.length; i++){
		if (inputs[i].id.substr(0, 7) == '__orig_') {
		    var orig_id = inputs[i].id;
		    var changed_id = orig_id.substr(7, orig_id.length-7);
		    if (changed_id) {
			var changed = $(changed_id);
			if (changed) {
                            if (inputs[i].value != 'null') {
                                changed.value = inputs[i].value;
                            }
			}
		    }
		}
	    }
        },

        clear_form : function(div_id) {
            var inputs = pvs.form.get_inputs($(div_id));
            for(var i=0; i<inputs.length; i++){
                inputs[i].value = '';
	    }
        },

        is_field_dirty : function(el_id) {
            if (el_id) {
                if ($(el_id) && $('__orig_'+el_id)) {
                    if ($_('__orig_'+el_id) != $_(el_id) && $_('__orig_'+el_id) != 'null') {
                        return true;
                    }
                }
            }
            return false;
        },

        is_dirty : function(div_id) {
            var inputs = pvs.form.get_inputs($(div_id));
            for(var i=0; i<inputs.length; i++){
		if (inputs[i].id.substr(0, 7) == '__orig_') {
		    var orig_id = inputs[i].id;
		    var changed_id = orig_id.substr(7, orig_id.length-7);
		    if (changed_id) {
			var changed = $(changed_id);
			if (changed) {
                            if (changed.value != inputs[i].value/* && inputs[i].value != 'null'*/) {
                                return true;
                            }
			}
		    }
		}
	    }
            return false;
        },

        is_form_blank : function(div_id) {
            var inputs = pvs.form.get_inputs($(div_id));
            for(var i=0; i<inputs.length; i++){
                if (inputs[i].type != 'hidden') {
                    if (inputs[i].value != '') {
                        return false;
                    }
                }
	    }
            return true;
        },

        un_reset_form : function(div_id) {
            var inputs = pvs.form.get_inputs($(div_id));
            for (var i=0; i<inputs.length; i++){
		if (inputs[i].id.substr(0, 7) == '__orig_') {
		    var orig_id = inputs[i].id;
		    var changed_id = orig_id.substr(7, orig_id.length-7);
		    if (changed_id) {
			var changed = $(changed_id);
			if (changed) {
			    inputs[i].value = changed.value;
			}
		    }
		}
	    }
        },

        /* KB: [2007-04-19]: Post a form and call a function if everything goes ok
         * this does not necessarily need to be a form.  "form_id" can be any element type.
         * Synchronous communicatoin does not appear to work in extjs
         */
        post : function (form_id, url, func) {
            pvs.ajax.post_array(url, func,
                                pvs.form.get_inputs_array(form_id));
        },

        // Return all the inputs under id as a key value array.
        get_inputs_array : function(id) {
            var kv = {};
            $(id+" :input").each(function(idx, elem) {
		if (elem.type == 'checkbox') {
                    kv[elem.name] = elem.checked
                } else {
                    kv[elem.name] = elem.value;
                }
            });

            try { return kv; } finally { kv = null; }
        },
        /* puts a semaphore around the action so users can't screw stuff up. */
        in_click : false,

        double_click_guard : function(func) {
            if (pvs.form.in_click) {
                //        alert("You only need to click once");
                pvs.form.in_click = false;
            } else {
                pvs.form.in_click = true;
                func();
                pvs.util.run_soon(function() {pvs.form.in_click = false;}, 400);
            }
        }

    };

    return pub;
}();

pvs.util = function(){
    pub = {
        /* KB: [2010-11-18]: This may not be such a good idea. */
        big_random : function() {
            return Date.parse(new Date());
        },
        run_soon : function(func, milliseconds) {
            setTimeout(func, milliseconds);
        },

        sleep : function(milliseconds) {
            var start = new Date().getTime();
            for (var i = 0; i < 1e7; i++) {
                if ((new Date().getTime() - start) > milliseconds){
                    break;
                }
            }
        },

        fork : function(func) {
            pvs.util.run_soon(func, 2);
        },

        loop : function(els, func) {
            for(var i = 0, len = els.length; i < len; i++){
                if(func(els, els[i], i) === false) {
                    break;
                }
            }
            return els;
        },

        get_page_title : function() {
            var matches = pvs.util.find("title");
            if (matches != null && matches.length > 0) {
                return matches[0].text;
            }
        },

        get_page_description : function() {
            var matches = pvs.util.find("meta[name=Description]");
            if (matches != null && matches.length > 0) {
                return matches[0].content;
            }
        },

        get_page_keywords : function() {
            var matches = pvs.util.find("meta[name=Keywords]");
            if (matches != null && matches.length > 0) {
                return matches[0].content;
            }
        },

        /* Lifted from this guy:  http://eriwen.com/javascript/js-stack-trace/ */
        show_stack : function(e, msg) {
            var callstack = [];
            var isCallstackPopulated = false;
            if (e.stack) { //Firefox
                var lines = e.stack.split("\n");
                for (var i = 0, len = lines.length; i < len; i++) {
                    if (lines[i].match(/^\s*[A-Za-z0-9\-_\$]+\(/)) {
                        callstack.push(lines[i]);
                    }
                }
                //Remove call to printStackTrace()
                callstack.shift();
                callstack.push(e.fileName+" ("+e.lineNumber+")");
                callstack.push(e.message);
                isCallstackPopulated = true;
            } else if (window.opera && e.message) { //Opera
                var lines = e.message.split("\n");
                for (var i = 0, len = lines.length; i < len; i++) {
                    if (lines[i].match(/^\s*[A-Za-z0-9\-_\$]+\(/)) {
                        var entry = lines[i];
                        //Append next line also since it has the file info
                        if (lines[i+1]) {
                            entry += " at " + lines[i+1];
                            i++;
                        }
                        callstack.push(entry);
                    }
                }
                //Remove call to printStackTrace()
                callstack.shift();
                isCallstackPopulated = true;
            }

            if (!isCallstackPopulated) { //IE and Safari
                callstack.push(e.message);
                //        var currentFunction = arguments.callee.caller.caller;
                //         if (currentFunction) {
                //             var fn = currentFunction.toString();
                //             callstack.push(fn.replace(new RegExp(/^ *}\n/gm), '').replace(new RegExp(/}/gm), '').replace(new RegExp(/{/gm), ''));
                //         }
            }

            if (msg) {
                callstack.push(msg);
            }
            pvs.dialog.alert(callstack.join("\n"));
        }
    };
    return pub;
}();



pvs.ajax = function(){
    function process_result(url, func, timeout, pre_process_func) {
        if (!pre_process_func) {
            pre_process_func = function(txt) {
                return txt;
            };
        }

        $.get(url, function(responseText){
            try {
                if (!check_session_expiration(responseText) && !check_server_error(responseText)) {
                    if (func) {
                        func(pre_process_func(responseText));
                    }
                }
            } catch(err) {
                pvs.util.show_stack(err, "A client error occurred.  Please send screenshot to your manager (a)");
                pvs.dialog.unwait();
            }
        });
    }

    function check_session_expiration(response) {
        if (response.match(/-LOGINPAGE-/)) {
            pvs.dialog.alert("You were away for too long.  Please log in again");
            pvs.browser.goto_url('/index.php');
            return true;
        }
        return false;
    }

    function check_server_error(response) {
        if (response.match(/ERROR:/) || response.match(/^ORA-/) || response.match(/oci_execute/)) {
            pvs.dialog.alert(unescape(response));
            pvs.dialog.unwait(); // just in case.
            return true;
        }
        return false;
    }

    pub = {
        populate_elem : function(url, div_id, mask, post_process_func, pre_process_func) {
            var el = $(div_id);
            mask && pvs.ui.mask(div_id);
            process_result(url, function(response_text) {
                mask && pvs.dom.unmask(div_id);
                $(div_id).empty();
                $(div_id).append(response_text);
                post_process_func && post_process_func(response_text);
            }, pre_process_func);
        },

        call : function(url, func, timeout) {
            process_result(url, func, timeout);
        },

        post_array : function(url, func, arr, timeout) {
            var obj = arr;
            $.post(url, arr, function(responseText) {
                try {
                    if (!check_session_expiration(responseText) && !check_server_error(responseText)) {
                        func(responseText);
                    }
                //} catch(err) {
                //  pvs.util.show_stack(err, "A client error occurred.  Please send screenshot to your manager (b)");
                } finally {
                    pvs.dialog.unwait();
                }
            });
        },

        url : function(params) {
            if (!params.root) {
                params.root = '/';
            }

            var url = params.root + '?';
            var first = true;
            for(var p in params){
                if (p != 'root') {
                    if (params[p] != undefined) {
                        if (!first) {
                            url += '&';
                        }
                        url += p + '=';
                        if (typeof params[p] == 'function') {
                            url += params[p]();
                        } else {
                            url += params[p];
                        }
                        first = false;
                    }
                }
            }
            url += "&_rnd="+Date.parse(new Date());
            return url;
        },

        api : function(params) {
            params['api'] = 1;
            return pvs.ajax.url(params);
        },

        dialog : function(params) {
            params['dialog'] = 1;
            return pvs.ajax.url(params);
        }
    };

    return pub;
}();

pvs.dialog = function() {

    function create_dialog_buttons_dialog0(params, on_ok, on_cancel) {
        return {
	    "Ok": on_ok,
	    "Cancel": on_cancel
	};
    };

    function create_dialog_buttons_dialog1(params, on_ok, on_cancel) {
        // do nothing because we don't want any buttons on this dialog.
    };

    function create_dialog_buttons_dialog2(params, on_ok, on_cancel) {
        return {
	    "Ok": on_ok
	};
    };

    function create_dialog_buttons_dialog3(params, on_ok, on_cancel) {
        return {
	    "Cancel": on_cancel
	};
    };

    // this is a hack to open 2 dialogs at the same time.
    function create_dialog_buttons_dialog4(params, on_ok, on_cancel) {
        return {
	    "Ok": on_ok,
	    "Cancel": on_cancel
	};
    };

    function create_dialog_buttons_dialog5(params, on_ok, on_cancel) {
        return {
	    "Done": on_ok
	};
    };

    function create_dialog(id, title) {
        $('body').after('<div id="'+id+'" title="'+title+'"><div id="'+id+'_body"></div></div>');
    };

    // was ax_popup_display_impl
    function dialog_display_impl(params) {
        var _on_ok = function() {
            if (!params.validator || (params.validator && $(params.validator.form).valid())) {
                if (params.on_ok) {
                    params.on_ok();
                }
                if (params.manual_destroy != true) {
                    pvs.dialog.destroy();
                }
            }
        };

        var _on_cancel = function() {
            if (params.on_cancel) {
                params.on_cancel();
            }
            pvs.dialog.destroy();
        };

        if (params.height && params.height > document.body.clientHeight) {
            if (!params.y) {params.y = 0;}
        }
        if (params.width && params.width > document.body.clientWidth) {
            if (!params.x) {params.x = 0;}
        }

        var buttons = {};
        eval("buttons = create_dialog_buttons_"+params.dialog_id+"(params, _on_ok, _on_cancel)");
	$('#'+params.dialog_id).dialog({autoOpen: false,
				        width: params.width,
                                        height: params.height,
                                        modal: true,
				        buttons: buttons,
                                        resizable: false,
                                        close: function(event, ui) {
                                            params.on_close && params.on_close();
                                            if (!params.preserve_on_close) {
                                                $('#'+params.dialog_id).remove();
                                                pvs.dialog.unwait();
                                            }
                                        },
                                        beforeClose: function(event, ui) {
                                            if (params.on_before_close) {
                                                return params.on_before_close();
                                            }
                                            return true;
                                        }
				       });

        if (!pvs.dialog.current) {
            pvs.dialog.current = [];
        }
        pvs.dialog.current.push($('#'+params.dialog_id));
        $('#'+params.dialog_id).dialog('open');
    };

    pub = {
        /* KB: [2010-08-17]:
            pvs.dialog.display({url:pvs.ajax.url({m:'prospect', c:'CDisplayEmail', prospect_id: $_('prospect_id')}),
                              title:'Send email',
                              width:520,
                              height:350,
                              on_ok:
                              function() {
                                  if ($('div_send_email')) {
                                      email_send_custom();
                                  } else if ($_('email.comm_id')) {
                                      email_select_message($_('email.comm_id'), $_('email.customize'));
                                  } else {
                                      ax_alert("Select email to send.");
                                  }
                              }
                });
        */
        display : function(params) {
            pvs.dialog.wait();
            create_dialog(params.dialog_id, params.title);
            params.render && params.render(params.dialog_id);
            if (params.url) {
                $('#'+params.dialog_id+'_body').load(params.url,
                                        function(response) {
                                            if (params.after_populate_elem) {
                                                params.after_populate_elem(response);
                                            }
                                            dialog_display_impl(params);
                                            if (params.validator) {
                                                $(params.validator.form).validate(params.validator);
                                            }
                                            if (params.after_display_impl) {
                                                params.after_display_impl(response);
                                            }
                                        });
            } else {
                dialog_display_impl(params);
                if (params.after_display_impl) {
                    params.after_display_impl();
                }
            }
        },

        alert : function(message) {
            alert(message);
        },

        failure : function(message) {
            pvs.dialog.alert('Failure Message:\n' + message)
        },

        /* msg     - main body of message
         * title   - top bar of the box
         * handler - function to handle the response from the user.
         * handlers- send a hash of callbacks indexed by btn values (yes, no, ok, cancel, etc)
         * multi   - whether or not to show a multiline prompt box.
         * anim    - element to animate from.
         * width   - duh
         * show_cancel - show Yes/No/Cancel instead of just Yes/No
         * Example:
         confirm({msg: 'howdy',
         title:'help',
         anim: 'search_method',
         multi: true,
         handler: function(btn,value) {
         alert(btn + ' | ' + value);
         }
         });
        */
        confirm : function(params) {
            return confirm(params['msg']);
        },

        /* msg     - main body of message
         * title   - top bar of the box
         */
        notice : function(params) {
        },

        /* KB: [2007-05-31]:
         * msg     - main body of message
         * title   - top bar of the box
         * handler - function to handle the response from the user.
         * multi   - whether or not to show a multiline prompt box.
         * anim    - element to animate from.
         * width   - duh
         * Example:
         pvs.dialog.prompt({msg: 'howdy',
             title:'help',
             anim: 'search_method',
             multi: true,
             handler: function(btn,value) {
             alert(btn + ' | ' + value);
             }
         });

        */
        prompt : function(params) {
        },

        /* KB: [2007-05-31]:
         * msg     - main body of message
         * title   - top bar of the box
         */
        wait : function(id) {
            pvs.ui.mask(id);
        },

        unwait : function(id) {
            pvs.ui.unmask(id);
        },

        current : '',

        destroy : function(dialog) {
            if (!dialog) {
                dialog = pvs.dialog.current.pop();
            }

            dialog.dialog('close');
            dialog = null;
            pvs.form.in_click = false;
            pvs.dialog.unwait();
            pvs.ui.unmask();
        },

        tool_tip : function(params) {
        }
    };

    return pub;
}();

pvs.ui = function(){
    pub = {
        hilight : function(id) {
            if ($(id).nodeName != "SELECT") {
                var s = $(id).style;
                if (s.backgroundColor != pvs.error_color && s.backgroundColor != pvs.error_color_other) {
                    s.backgroundColor = pvs.over_color;
                }
            }
        },

        unhilight : function(id, bg) {
            if ($(id).nodeName != "SELECT") {
                var s = $(id).style;
                if (s.backgroundColor != pvs.error_color && s.backgroundColor != pvs.error_color_other) {
                    s.backgroundColor = (bg ? bg : 'white');
                }
            }
        },

        menu_highlight : function(id) {
            $("a[id^='link_']").css("background-color", '');
            if (id) {
                $(id).css("background-color", pvs.error_color);
            }
        },

        mark_invalid : function(id) {
            if (id && $(id)) {
                var s = $(id).style;
                s.backgroundColor = pvs.error_color;
            }
        },

        mark_valid : function(id) {
            if (id && $(id)) {
                var s = $(id).style;
                s.backgroundColor = 'white';
            }
        },

        click_up : function(id) {
            $(id).setStyle('border-style', 'outset');
        },

        click_down : function(id) {
            $(id).setStyle('border-style', 'inset');
        },

        is_key_pressed : function(code, evt) {
            var is_key = false;
            if (evt && evt.keyCode == code) {
                is_key = true;
            }
            return is_key;
        },

       set : function(id, val, noorig) {
            var field = $(id);
            if (field && field.length > 0) {
                field = field[0];
                if (field.tagName == 'SELECT') {
                    //ax_set_select_value(field, val);
                } else if (field.tagName == 'DIV' || field.tagName == 'TD' || field.tagName == 'SPAN' || field.tagName == 'DD') {
                    $(id).empty();
                    $(id).append((val ? val : ''));
                } else if (field.type == 'checkbox') {
                    field.checked = (val == 'Y' ? 'checked' : '');
                    field.value = val;
                } else {
                    field.value = (val ? val : '');
                }
                if (!noorig) {
                    var orig = $('__orig_'+id);
                    if (orig) {
                        orig.value = (val ? val : '');
                    }
                }
            }
        },

        get : function(id) {
            return $_(id);
        },

        get_screen_height : function() {
            return $(document).height();
        },

        get_screen_width : function() {
            return $(window).width()
        },

        mask : function(id, fadein) {
            var t = 0;
            var l = 0;
            var h = $(document).height();
            var w = $(window).width();
            if (id) {
                var offset = $(id).offset();
                t = offset.top;
                l = offset.left;
                h = $(id).offsetParent().height();
                w = $(id).offsetParent().width();
            }
            $('body').after('<div id="__mask"></div>');

	    //Set heigth and width to mask to fill up the whole screen
	    $('#__mask').css({'width':w,
                              'height':h,
                              'top':t, 'left':l,
                              'z-index':999});

	    $('#__mask').fadeTo('fast', 0.3, function() {
	        $('#__mask').spinner({img: '/static/js/jquery/spinner/spinner-large.gif',
                                      position:'center',
				      height: 48,
				      width: 48});
            });
        },

        unmask : function(id, milliseconds) {
            if (milliseconds) {
                pvs.util.run_soon(function() {
                    pvs.dom.unmask(id);
                }, milliseconds);
            } else {
                var e = $('#__mask');
                if (e) {
                    $('#__mask').spinner('remove');
                    $('img[src*="spinner"]').remove();
                    e.hide(0.3, function() {
                        $('img[src*="spinner"]').remove();
                        e.remove();
                    });
                }
            }
        },

        init_datepickers : function() {
            /* KB: [2010-09-17]: http://jqueryui.com/demos/datepicker/ */
            if ($(".datepicker").datepicker) {
                $(".datepicker").datepicker({format: 'yyyy-mm-dd'});
            }
        }
    };

    return pub;
}();

pvs.map = function(){
    pub = {
        init_local : function(opt, lat, lng, id, marker_msg, icon) {
            var map = new google.maps.Map(document.getElementById(id), opt);
            map.setCenter(new google.maps.LatLng(lat, lng));
            var latlng = new google.maps.LatLng(lat, lng);
            var confirmation_map_loc_marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title:marker_msg,
                icon: icon
            });
            return map;
        },

        /*
          # this stuff has to be in HEAD
          <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
          ${h.javascript_link('http://maps.google.com/maps/api/js?sensor=false')}

          # then it has to be called onload
          pvs.onload.push(function() {
              pvs.map.init($_('#lat'), $_('#lng'), 'map_canvas');
          });

          # somewhere in the body add a div to taste.
          <div id="map_canvas" style="width:100%; height:100%"></div>
         */
        init : function(opt, default_lat, default_lng, id, marker_msg, icon) {
            var map = new google.maps.Map(document.getElementById(id), opt);
            if (navigator.geolocation) {
                // Try W3C Geolocation (Preferred)
                navigator.geolocation.getCurrentPosition(function(position) {
                    var lat = position.coords.latitude;
                    var lng = position.coords.longitude;
                    map.setCenter(new google.maps.LatLng(lat, lng));
                    var latlng = new google.maps.LatLng(lat, lng);
                    confirmation_map_loc_marker = new google.maps.Marker({
                        position: latlng,
                        map: map,
                        title:marker_msg,
                        icon: icon
                    });
                }, function() {
                    // no geo
                });
            } else if (google.gears) {
                // Try Google Gears Geolocation
                var geo = google.gears.factory.create('beta.geolocation');
                geo.getCurrentPosition(function(position) {
                    var lat = position.latitude;
                    var lng = position.longitude;
                    map.setCenter(new google.maps.LatLng(lat, lng));
                    var latlng = new google.maps.LatLng(lat, lng);
                    confirmation_map_loc_marker = new google.maps.Marker({
                        position: latlng,
                        map: map,
                        title:marker_msg,
                        icon: icon
                    });
                }, function() {
                    //no geo
                });
            }
            return map;
        },

        on : function(evt_name, map, onclick_func) {
            google.maps.event.addListener(map, evt_name, function(event) {
                onclick_func(map, event.latLng);
            });
        },

        mark : function(map, lat, lng, msg) {
            var latlng = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));
            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title:msg
            });
            return marker;
        }
    };

    return pub;
}();

pvs.button = function(){
    pub = {

        init : function(val) {
            //http://twitter.github.com/bootstrap/javascript.html#buttons
            if ($('.btn[data-loading-text]').on) {
                $('.btn[data-loading-text]').on('click', function () {
                    $(this).button('loading')
                });
            }
        },

        reset : function(msg, title, onclick) {
            $('.btn[data-loading-text]').on('click', function () {
                $(this).button('reset')
            });
        }
    };

    return pub;
}();


$(document).ready(function() {
    pvs.button.init();
});

$(document).ready(function() {
    pvs.ui.init_datepickers();
});

/* KB: [2010-08-16]:
   Append to this to get stuff to run at the end.
   pvs.onload.push(function() { pvs.popup.alert('kenny'); })
*/
pvs.onload = new Array();
$(document).ready(function() {
          for (var i in pvs.onload) {
             pvs.onload[i]();
          }
});



/*
// CSS Browser Selector   v0.2.5
// Documentation:         http://rafael.adm.br/css_browser_selector
// License:               http://creativecommons.org/licenses/by/2.5/
// Author:                Rafael Lima (http://rafael.adm.br)
// Contributors:          http://rafael.adm.br/css_browser_selector#contributors

var css_browser_selector = function() {
	var
		ua=navigator.userAgent.toLowerCase(),
		is=function(t){ return ua.indexOf(t) != -1; },
		h=document.getElementsByTagName('html')[0],
		b=(!(/opera|webtv/i.test(ua))&&/msie (\d)/.test(ua))?('ie ie'+RegExp.$1):is('gecko/')? 'gecko':is('opera/9')?'opera opera9':/opera (\d)/.test(ua)?'opera opera'+RegExp.$1:is('konqueror')?'konqueror':is('applewebkit/')?'webkit safari':is('mozilla/')?'gecko':'',
		os=(is('x11')||is('linux'))?' linux':is('mac')?' mac':is('win')?' win':'';
	var c=b+os+' js';
	h.className += h.className?' '+c:c;
}();
// KB: [2007-02-16]: This crazy thing allows us to have CSS dependant on browser */

})(jQuery);