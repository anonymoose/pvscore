${self.pre_pre_process()}
${self.pre_process()}

% if not h.is_dialog(request):
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
  <meta name="Description" content="${self.meta_description()}" />
  <meta name="Version" content="${self.meta_version()}" />
  <meta name="Keywords" content="${self.meta_keywords()}" />

  <title>${self.meta_title()}</title>

  ${h.stylesheet_link('/static/bootstrap/css/bootstrap.css')}
  <style type="text/css">
    body {
    padding-top: 60px;
    padding-bottom: 40px;
    }
  </style>
  ${h.stylesheet_link('/static/bootstrap/css/bootstrap-responsive.css')}

  ${h.stylesheet_link('/static/js/jquery/jqgrid/css/ui.jqgrid.css')}
  ${h.stylesheet_link('/static/bootstrap-extensions/datepicker/css/datepicker.css')}
  ${h.stylesheet_link('/static/css/pvs.css?rnd=123')}
  ${h.stylesheet_link('/static/css/appointment.css')}

  <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
  <%include file="style_override.mako"/>

  ${self.local_head()}
  ${self.other_head()}
</head>

<body>
  <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        <ul class="nav pull-left">
          ${self.top_bar_left()}
        </ul>
        <ul class="nav pull-right">
          ${self.top_bar_right()}
        </ul>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="row ${self.body_class()}">
      ${self.draw_body()}
    </div>
  </div>
</div>

<div class="container">
  <div class="row">
    <div class="span12 footer-break"></div>
  </div>
</div>

<hr/>

<footer>
&nbsp;  &copy; ${h.literal(request.ctx.enterprise.copyright if request.ctx.enterprise.copyright else '<a target="_blank" href="https://www.eyefound.it">EyeFound.IT</a>')}
</footer>


<!-- Modals -->
<div class="modal hide fade" id="dlg_standard">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    <h3 id="dlg_standard_title">Update Status</h3>
  </div>
  <div class="modal-body">
  </div>
  <div class="modal-footer">
    <button id="btn_ok_dlg_standard" class="btn btn-primary" onclick="$('#frm_dialog').submit()">Ok</button>
    <button class="btn btn-link" data-dismiss="modal" aria-hidden="true">Cancel</button>
  </div>
</div>

<div class="modal hide fade" id="dlg_email">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    <h3 id="dlg_standard_title">Send Email</h3>
  </div>
  <div class="modal-body">
  </div>
  <div class="modal-footer">
    <button id="btn_ok_dlg_standard" class="btn btn-primary" onclick="customer_send_email();">Ok</button>
    <button class="btn btn-link" data-dismiss="modal" aria-hidden="true">Cancel</button>
  </div>
</div>

<div class="modal hide fade" id="dlg_simple">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    <h3 id="dlg_standard_title">Note</h3>
  </div>
  <div class="modal-body">
  </div>
  <div class="modal-footer">
    <button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">Ok</button>
  </div>
</div>
<!-- /Modals -->


<div id="hidden" style="display:none;"></div>

<script src="/static/bootstrap/js/jquery.js"></script>
<script src="/static/bootstrap/js/bootstrap.js"></script>
<!--script src="/static/bootstrap-extensions/bootstrap-typeahead.js"></script-->
<script src="/static/bootstrap-extensions/datepicker/js/bootstrap-datepicker.js"></script>


<script src="/static/js/jquery/validate/jquery.validate.min.js"></script>
<script src="/static/js/jquery/validate/additional-methods.js"></script>
<script src="/static/js/jquery/spinner/jquery.spinner.js"></script>
<script src="/static/js/jquery/uploadify/swfobject.js"></script>
<script src="/static/js/jquery/uploadify/jquery.uploadify.v2.1.4.min.js"></script>
<script src="/static/js/jquery/json/jquery.json-2.2.min.js"></script>
<script src="/static/js/tinymce/tinymce/jscripts/tiny_mce/tiny_mce.js"></script>
<script src="/static/js/codemirror/CodeMirror-0.91/js/codemirror.js"></script>
<script src="/static/js/codemirror/CodeMirror-0.91/js/mirrorframe.js"></script>
<script src="/static/js/jquery/jqgrid/js/i18n/grid.locale-en.js"></script>
<script src="/static/js/jquery/jqgrid/js/jquery.jqGrid.min.js"></script>
<script src="/static/js/jquery/barcode/jquery-barcode-2.0.2.min.js"></script>
<script src="/static/js/jquery/tablesorter/jquery.tablesorter.min.js"></script>
<script src="/static/crm/js/pvs-jquery.js?rnd=234"></script>

${self.local_foot()}
${self.other_foot()}

<script>
window.onerror=function(msg){
    $("body").attr("js_error",msg);
};
</script>

</body>
</html>

% else:
  ${next.body()}\
% endif

<%def name="pre_pre_process()">
<%
%>
</%def>

<%def name="pre_process()">
</%def>

<%def name="top_menu()">
</%def>

<%def name="left_col()">\
</%def>

<%def name="right_col()">\
</%def>

<%def name="body_class()"></%def>

<%def name="footer_left()">\
${h.literal(c.pvs_crm_footer_links) if hasattr(c, 'pvs_crm_footer_links') else ''}
</%def>

<%def name="top_bar_left()">\
      % if request.ctx.user.priv.view_customer or request.ctx.user.priv.edit_customer:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
          Customer
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li><a href="/crm/customer/show_search">Advanced Search</a></li>
          % if request.ctx.user.priv.edit_customer:
          <li><a href="/crm/customer/new">Add New Customer</a></li>
          % endif
          % if 'recent_customers' in request.session:
          <li class="dropdown-submenu">
            <a tabindex="-1" href="#">Recent Customers</a>
            <ul class="dropdown-menu">
              % for recent_customer_id in request.session['recent_customers'].keys():
              <li><a href="/crm/customer/edit/${recent_customer_id}">${request.session['recent_customers'][recent_customer_id]}</a></li>
              % endfor
            </ul>
          </li>
          % endif
        </ul>
      </li>
      <li>
        <form id="frm_lname_complete" class="navbar-form pull-left">
          <input name="lname_complete" type="text"
                 placeholder="Last Name Search"
                 id="lname_complete" data-provide="typeahead" data-source="[]" maxlength="30" autocomplete="off"/>
        </form>
      </li>
      % endif

    <li class="dropdown">
      <a href="#" class="dropdown-toggle" data-toggle="dropdown">
        Calendar
        <b class="caret"></b></a>
      <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">
        <li><a href="/crm/appointment/this_day">Today</a></li>
        <li><a href="/crm/appointment/tomorrow">Tomorrow</a></li>
        <li><a href="/crm/appointment/this_month">This Month</a></li>
        <li><a href="/crm/appointment/show_search">Search</a></li>
        <li><a href="/crm/appointment/new">New Appointment</a></li>
      </ul>
    </li>

    <li class="dropdown">
      <a href="#" class="dropdown-toggle" data-toggle="dropdown">
        Administration
        <b class="caret"></b></a>
      <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">

        % if request.ctx.user.priv.edit_company or request.ctx.user.priv.view_company or request.ctx.user.priv.view_campaign or request.ctx.user.priv.edit_campaign or request.ctx.user.priv.view_enterprise or request.ctx.user.priv.edit_enterprise:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Company</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_company:
            <li><a href="/crm/company/new">Add New Company</a></li>
            % endif
            <li><a href="/crm/company/list">List All Companies</a></li>
            % if request.ctx.user.priv.edit_campaign:
            <li><a href="/crm/campaign/new">Add New Campaign</a></li>
            % endif
            <li><a href="/crm/campaign/list">List All Campaigns</a></li>
            % if request.ctx.user.enterprise_id == None:
            <li><a href="/crm/company/enterprise/new">Add New Enterprise</a></li>
            <li><a href="/crm/company/enterprise/list">List All Enterprises</a></li>
            % endif
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.edit_discount:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Discount</a>
          <ul class="dropdown-menu">
            <li><a href="/crm/discount/new">Add New Discount</a></li>
            <li><a href="/crm/discount/list">List All Discounts</a></li>
          </ul>
        </li>
        % endif


        % if request.ctx.user.priv.view_communication or request.ctx.user.priv.edit_communication:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Email</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_communication:
            <li><a href="/crm/communication/new">Add Template</a></li>
            % endif
            <li><a href="/crm/communication/list">List Templates</a> </li>
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.view_product or request.ctx.user.priv.edit_product:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Products</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_product:
            <li><a href="/crm/product/new">Add New Product</a></li>
            <li><a href="/crm/product/show_inventory">Edit Inventory</a></li>
            % endif
            <li><a href="/crm/product/list">List All Products</a></li>
            % if request.ctx.user.priv.edit_category:
            <li><a href="/crm/product/category/new">Add Product Category</a></li>
            % endif
            <li><a href="/crm/product/category/list">List Product Categories</a></li>
          </ul>
        </li>
        % endif


        % if request.ctx.user.priv.view_report:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Reports</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_report or request.ctx.user.priv.edit_users:
            <li><a href="/crm/report/new">Add New Report</a></li>
            % endif
            <li><a href="/crm/report/list">List All Reports</a></li>
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.edit_purchasing or request.ctx.user.priv.view_purchasing:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Suppliers</a>
          <ul class="dropdown-menu">
            <li><a href="/crm/purchase/show_search">Find Supplier Order</a></li>
            % if request.ctx.user.priv.edit_purchasing:
            <li><a href="/crm/purchase/new">Add Supplier Order</a></li>
            % endif
            <li><a href="/crm/purchase/list">List Supplier Orders</a></li>
            % if request.ctx.user.priv.edit_purchasing:
            <li><a href="/crm/purchase/vendor/new">Add Supplier</a></li>
            <li><a href="/crm/purchase/vendor/list">List Suppliers</a></li>
            % endif
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.view_users or request.ctx.user.priv.edit_users:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Users</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_users:
            <li><a href="/crm/users/new">Add New User</a></li>
            % endif
            <li><a href="/crm/users/list">List All Users</a> </li>
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.cms:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Website</a>
          <ul class="dropdown-menu">
            <li><a href="/cms/site/list">List Websites</a></li>
            <li><a href="/cms/site/new">New Website</a></li>
          </ul>
        </li>
        % endif

        % if request.ctx.user.priv.edit_event or request.ctx.user.priv.view_event:
        <li class="dropdown-submenu">
          <a tabindex="-1" href="#">Workflow</a>
          <ul class="dropdown-menu">
            % if request.ctx.user.priv.edit_event:
            <li><a href="/crm/event/new">Add Workflow Event</a></li>
            % endif
            <li><a href="/crm/event/list">List All Workflow Events</a> </li>
            % if request.ctx.user.priv.edit_event:
            <li><a href="/crm/phase/new">Add Customer Phase</a></li>
            % endif
            <li><a href="/crm/phase/list">List All Customer Phases</a> </li>
          </ul>
        </li>
        % endif

        % for link_name in plugin_registry.category('administration_link'):
          % if plugin_registry.is_applicable('administration_link', link_name, request):
            <li><a href="${plugin_registry.getattr('administration_link', link_name, 'href')}">${link_name}</a></li>
          % endif
        % endfor
      </ul>
    </li>
</%def>


<%def name="top_bar_right()">\
## a <ul> that will make up the menu.
  % if request.ctx.user.priv.view_users or request.ctx.user.priv.edit_users:
  <li><a href="/crm/users/edit_current">My Account</a></li>
  % endif

  <li><a href="/crm/dashboard">Dashboard</a></li>
  <li><a href="/crm/logout">Logout</a></li>
</%def>

<%def name="meta_title()"></%def>

<%def name="meta_keywords()"></%def>

<%def name="meta_description()"></%def>

<%def name="meta_version()"></%def>

<%def name="flashes()">
  % for flash in request.session.pop_flash():
    <div class="alert alert-success">${flash}</div>
  % endfor
</%def>

<%def name="local_foot()">\
    <script src="/static/crm/js/common.js"></script>
    <script src="/static/crm/js/users.js"></script>
    <script src="/static/crm/js/product.js"></script>
    <script src="/static/crm/js/report.js"></script>
    <script src="/static/crm/js/discount.js"></script>
    <script src="/static/crm/js/purchase.js"></script>
    <script src="/static/crm/js/comm.js"></script>
    <script src="/static/crm/js/content.js"></script>
    <script src="/static/crm/js/customer.js?rnd=12345"></script>
    <script src="/static/crm/js/appointment.js"></script>
    <script>
    $(document).ready(function() {
        $('.sortable').tablesorter();
    });
    </script>
</%def>

<%def name="other_foot()">\
## override this to provide additional javascript stuff that actually goes at the bottom
</%def>
<%def name="local_head()">\
## override this to provide additional CSS stuff that actually goes in <head>
</%def>
<%def name="other_head()">\
## override this to provide additional CSS stuff that actually goes in <head>
</%def>

<%def name="draw_body()">\
${self.draw_body_standard()}
</%def>

<%def name="draw_body_standard()">\
  <div class="span3">
    ${self.left_col()}
  </div>
  <div class="span6">
    <div class="right">
      ${self.flashes()}
      ${next.body()}
    </div>
  </div>
  <div class="span3">
    ${self.right_col()}
  </div>
</%def>

<%def name="draw_body_no_right_col()">\
  <div class="span3">
    ${self.left_col()}
  </div>
  <div class="span9">
    <div class="right">
      ${self.flashes()}
      ${next.body()}
    </div>
  </div>
</%def>

<%def name="draw_body_no_left_col()">\
  <div class="span9">
    <div class="right">
      ${self.flashes()}
      ${next.body()}
    </div>
  </div>
  <div class="span3">
    ${self.right_col()}
  </div>
</%def>

<%def name="draw_body_center_only()">\
  <div class="span12">
    <div class="right">
      ${self.flashes()}
      ${next.body()}
    </div>
  </div>
</%def>

<%def name="country_list()">
<%
   import pvscore.lib.util as util
   %>
${util.country_select_list()}
</%def>
