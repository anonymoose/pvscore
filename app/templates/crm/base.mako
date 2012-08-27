${self.pre_pre_process()}
${self.pre_process()}

% if not h.is_dialog(request):
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
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
  
  ${h.stylesheet_link('/static/js/jquery/fancybox/jquery.fancybox-1.3.4.css')}
  ${h.stylesheet_link('/static/js/jquery/autocomplete/jquery.autocomplete.css')}
  ${h.stylesheet_link('/static/js/jquery/jqgrid/css/ui.jqgrid.css')}
  ${h.stylesheet_link('/static/js/jquery/jquery-ui/css/ui-lightness/jquery-ui-1.8.23.custom.css')}
  ${h.stylesheet_link('/static/css/pvs.css')}

  
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
  &copy; ${h.literal(request.ctx.enterprise.copyright if
  request.ctx.enterprise.copyright else '<a href="http://www.palmvalleysoftware.com">Palm Valley Software</a>')}
</footer>

<div id="hidden" style="display:none;"></div>

<script src="/static/bootstrap/js/jquery.js"></script>
<script src="/static/bootstrap/js/bootstrap.js"></script>
<script src="/static/bootstrap-extensions/bootstrap-typeahead.js"></script>

<script src="/static/js/jquery/validate/jquery.validate.min.js"></script>
<script src="/static/js/jquery/validate/additional-methods.js"></script>
<script src="/static/js/jquery/spinner/jquery.spinner.js"></script>
<script src="/static/js/jquery/tablesorter/jquery.tablesorter.min.js"></script>
<script src="/static/js/jquery/uploadify/swfobject.js"></script>
<script src="/static/js/jquery/uploadify/jquery.uploadify.v2.1.4.min.js"></script>
<script src="/static/js/jquery/json/jquery.json-2.2.min.js"></script>
<script src="/static/js/tinymce/tinymce/jscripts/tiny_mce/tiny_mce.js"></script>
<script src="/static/js/codemirror/CodeMirror-0.91/js/codemirror.js"></script>
<script src="/static/js/codemirror/CodeMirror-0.91/js/mirrorframe.js"></script>
<script src="/static/js/jquery/jqgrid/js/i18n/grid.locale-en.js"></script>
<script src="/static/js/jquery/jqgrid/js/jquery.jqGrid.min.js"></script>
<script src="/static/js/jquery/barcode/jquery-barcode-2.0.2.min.js"></script>

<script src="/static/crm/js/pvs-jquery.js"></script>

${self.local_foot()}
${self.other_foot()}

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
          <li>
            <form id="frm_customer_search" class="form-inline">
              <input type="text" class="pad10" placeholder="Customer Search"/>
            </form>
          </li>
          <li><a href="/crm/customer/advanced_search">Advanced Search</a></li>
            % if request.ctx.user.priv.edit_customer:
          <li><a href="/crm/customer/new">Add</a></li>
            % endif
        </ul>
      </li>
      % endif

      % if request.ctx.user.priv.view_users or request.ctx.user.priv.edit_users:
      <li><a href="/crm/users/edit_current">My Account</a></li>
      % endif

      % if request.ctx.user.priv.cms:
      <li><a href="/cms/siteedit/list">Website</a></li>
      % endif

      <li class="divider-vertical"></li>

      % if request.ctx.user.priv.view_product or request.ctx.user.priv.edit_product:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
          Product
          <b class="caret"></b></a>
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

      % if request.ctx.user.priv.edit_company or request.ctx.user.priv.view_company or request.ctx.user.priv.view_campaign or request.ctx.user.priv.edit_campaign or request.ctx.user.priv.view_enterprise or request.ctx.user.priv.edit_enterprise:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Company
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          % if request.ctx.user.priv.edit_company:
          <li><a href="/crm/company/new">Add New Company</a></li>
          % endif
          <li><a href="/crm/company/list">List All Companies</a></li>
          % if request.ctx.user.priv.edit_campaign:
          <li><a href="/crm/campaign/new">Add New Campaign</a></li>
          % endif
          <li><a href="/crm/campaign/list">List All Campaigns</a></li>
          % if request.ctx.user.priv.edit_enterprise:
          <li><a href="/crm/company/enterprise/new">Add New Enterprise</a></li>
          % endif
          <li><a href="/crm/company/enterprise/list">List All Enterprises</a></li>
        </ul>
      </li>
      % endif

      % if request.ctx.user.priv.edit_purchasing or request.ctx.user.priv.view_purchasing:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Suppliers
          <b class="caret"></b></a>
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

      % if request.ctx.user.priv.edit_event or request.ctx.user.priv.view_event:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Workflow
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          % if request.ctx.user.priv.edit_event:
          <li><a href="/crm/event/new">Add Workflow Event</a></li>
          % endif
          <li><a href="/crm/event/list">List All Workflow Events</a> </li>
        </ul>
      </li>
      % endif

      % if request.ctx.user.priv.view_communication or request.ctx.user.priv.edit_communication:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Email
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          % if request.ctx.user.priv.edit_communication:
          <li><a href="/crm/communication/new">Add Template</a></li>
          % endif
          <li><a href="/crm/communication/list">List Templates</a> </li>
        </ul>
      </li>
      % endif

      % if request.ctx.user.priv.view_report:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Reports
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          % if request.ctx.user.priv.edit_report or request.ctx.user.priv.edit_users:
          <li><a href="/crm/report/new">Add New Report</a></li>
            % endif
          <li><a href="/crm/report/list">List All Reports</a></li>
        </ul>
      </li>
      % endif

      % if request.ctx.user.priv.view_users or request.ctx.user.priv.edit_users:
      <li class="dropdown">
        <a href="#" class="dropdown-toggle"
           data-toggle="dropdown">Users
          <b class="caret"></b></a>
        <ul class="dropdown-menu">
          % if request.ctx.user.priv.edit_users:
          <li><a href="/crm/users/new">Add New User</a></li>
          % endif
          <li><a href="/crm/users/list">List All Users</a> </li>
        </ul>
      </li>
      % endif

</%def>


<%def name="top_bar_right()">\
## a <ul> that will make up the menu.
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
    <script src="/static/crm/js/customer.js"></script>
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
   import app.lib.util as util
   %>
${util.country_select_list()}
</%def>
