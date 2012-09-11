<%

g_action = request.environ['pylons.routes_dict']['action']

%>
% if not h.is_dialog():
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    <meta name="Description" content="${self.meta_description()}" />
    <meta name="Version" content="${self.meta_version()}" />
    <meta name="Keywords" content="${self.meta_keywords()}" />

    <title>${self.meta_title()}</title>
    
    <script>
    </script>
    <!-- JQuery JS required stuff. -->
    ${h.stylesheet_link('/public/js/jquery-1.4.2/jquery-ui-1.8.4/css/smoothness/jquery-ui-1.8.4.custom.css')}
    ${h.javascript_link('/public/js/jquery-1.4.2/core/jquery-1.4.2.js')}
    ${h.javascript_link('/public/js/jquery-1.4.2/jquery-ui-1.8.6/js/jquery-ui-1.8.6.custom.min.js')}
    ${h.javascript_link('/public/js/jquery-1.4.2/jquery-validate-1.7/jquery.validate.min.js')}
    ${h.javascript_link('/public/js/jquery-1.4.2/jquery-validate-1.7/additional-methods.js')}
    ${h.javascript_link('/public/js/jquery-1.4.2/spinner/jquery.spinner.js')}
    ${h.javascript_link('/public/js/jquery-1.4.2/jquery.tablesorter/jquery.tablesorter.min.js')}

    <!-- PVS/EXT wrapper library -->
    ${h.javascript_link('/public/js/pvs/pvs-jquery.js')}
    ${h.javascript_link('/public/crm/js/common.js')}
    
    <!-- APP specific includes -->
    
    ${self.main_css()}
    ${h.stylesheet_link('/public/css/pvs-jquery.css')}
    ${self.other_head()}
</head>
<body>
    ${next.body()}\

    <div class="footer">
      ${self.footer()}\
    </div>
</body>
</html>
% else:
    ${next.body()}\
% endif

<%def name="main_css()">\
    ${h.stylesheet_link('/public/css/main.css')}
</%def>

## Don't show links that are redundant for particular pages
<%def name="footer()">\
</%def>

<%def name="header()">\
## override this to put stuff at the top of the page above the flash
</%def>

<%def name="other_head()">\
## override this to provide additional CSS stuff that actually goes in <head>
</%def>

<%def name="meta_title()"></%def>

<%def name="meta_keywords()"></%def>

<%def name="meta_description()"></%def>

<%def name="meta_version()"></%def>

<%def name="flashes()">
    <% flashes = h.flash.pop_messages() %>
    % if flashes:
      % for flash in flashes:
        <div class="flash">
          <span class="message">${flash}</span>
        </div>
      % endfor
    % endif
</%def>
