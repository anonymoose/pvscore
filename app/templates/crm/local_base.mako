<%inherit file="crm_base.mako"/>\
<%!
    from app.model.core.users import Users
%>

${next.body()}

<%def name="tabs()">
<%
    from app.lib.plugin import plugin_registry
    controller = request.environ['pylons.routes_dict']['controller']
    plugin = None
    if 'plugin' in request.environ['pylons.routes_dict']:
        plugin = request.environ['pylons.routes_dict']['plugin']
    user = Users.load(session['user_id'])
    user_type = user.type
%>
% if user.priv.view_customer or user.priv.edit_customer:
    <a href="/crm/customer/dialog/crm/customer.search" class="${'selected' if controller in ['crm/customer'] else ''}">Customer</a> 
% endif
% if user.priv.view_users or user.priv.edit_users:
    <a href="/crm/users/dialog/crm/users.search" class="${'selected' if controller in ['crm/users'] else ''}">Users</a> 
% endif
% if user.priv.view_product or user.priv.edit_product:
    <a href="/crm/product/show_search" class="${'selected' if controller in ['crm/product'] else ''}">Product</a> 
% endif
% if user.priv.view_purchasing or user.priv.edit_purchasing:
    <a href="/crm/purchase/show_search" class="${'selected' if controller in ['crm/purchase'] else ''}">Purchasing</a> 
% endif
% if user.priv.view_event or user.priv.edit_event:
    <a href="/crm/event/dialog/crm/event.search" class="${'selected' if controller in ['crm/event'] else ''}">Event</a> 
% endif
% if user.priv.view_event or user.priv.edit_event:
    <a href="/crm/communication/show_search" class="${'selected' if controller in ['crm/communication'] else ''}">Comms</a> 
% endif
% if user.priv.view_report or user.priv.edit_report:
    <a href="/crm/report/list" class="${'selected' if controller in ['crm/report'] else ''}">Reports</a> 
% endif
% if user.priv.view_company or user.priv.edit_company:
    <a href="/crm/company/list" class="${'selected' if controller in ['crm/company'] else ''}">Company</a> 
% endif
    % for plugin_name in plugin_registry:
        % if plugin_registry[plugin_name].defines('render_crm_admin_tab') and user.type != 'External':
            <a href="${plugin_registry[plugin_name].path_to('render_crm_admin_tab')}" 
               class="${'selected' if plugin == plugin_name else ''}">${plugin_registry[plugin_name].display_name_of()}</a> 
        % endif
    % endfor
</%def>

<%def name="actions()">
  <ul>
    <li>
    </li>
  </ul>
</%def>

<%def name="top_name()">
<%
    user = Users.load(session['user_id'])
%>
${user.enterprise.name if user.enterprise else ''} CRM
</%def>






