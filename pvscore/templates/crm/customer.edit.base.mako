<%inherit file="customer.base.mako"/>\

<style>
.dl-horizontal dt {
  width: 160px;
  margin-right: 10px;
}
.dl-horizontal dd {
  text-align: right;
}
</style>

${next.body()}

<%def name="left_col()">
<%
    balance = customer.get_current_balance()
%>
  <input type="hidden" id="customer_menu_selected" value="${request.url.split('/')[5]}"/>
  <div class="well sidebar-nav">
    % if customer.customer_id:
    <ul class="nav nav-list">
      % if customer.customer_id:
      <input type="hidden" name="customer_id" id="customer_id" value="${customer.customer_id}"/>
      <li><b>${customer.fname} ${customer.lname}</b></li>
      <li>
        % if customer.email:
        ${h.link_to(customer.email, 'javascript:customer_send_email()', id='link_send_email')}
        % else:
        No Email
        % endif
      </li>
      <li>${customer.phone}</li>
      <li id="edit">${h.link_to('Edit Customer', '/crm/customer/edit/%s' % customer.customer_id)}</li>
      <li><hr></li>
      % endif
      % if customer.customer_id:
      <li id="show_orders">${h.link_to('Orders', '/crm/customer/show_orders/%s' % customer.customer_id)}</li>
      % if request.ctx.user.priv.add_customer_order:
      <li id="add_order_dialog">${h.link_to('Add Order', '/crm/customer/add_order_dialog/%s' % customer.customer_id)}</li>
      % endif
      % if request.ctx.user.priv.add_customer_billing:
      <!--li>${h.link_to('Billing Method', 'javascript:customer_edit_billing_method()', id='link_add_billing')}</li-->
      % endif
      % if request.ctx.user.priv.send_customer_emails:
      <li>
        <a data-toggle="modal" data-target="#dlg_standard"
           href="/crm/communication/send_comm_dialog?customer_id=${customer.customer_id}&dialog=1">
          Send Email
        </a>
      </li>
      % endif
      % if request.ctx.user.priv.edit_customer:
      <li>
        <a data-toggle="modal" data-target="#dlg_standard"
           href="/crm/customer/status_dialog/${customer.customer_id}?dialog=1">
          Status
        </a>
      </li>
      % endif
      
      <li id="show_history">${h.link_to('History', '/crm/customer/show_history/%s' % customer.customer_id)}</li>
      % if request.ctx.user.priv.add_customer_billing:
      <li id="show_billings">${h.link_to('Billing', '/crm/customer/show_billings/%s' % customer.customer_id)}</li>
      % endif
      <li id="show_attributes">${h.link_to('Attributes', '/crm/customer/show_attributes/%s' % customer.customer_id)}</li>
      
      <li id="new_for_customer"><a href="/crm/appointment/new_for_customer/${customer.customer_id}">Add Appt</a></li>
      <li id="show_appointments">${h.link_to('Appointments', '/crm/appointment/show_appointments/%s' % customer.customer_id, id='link_appointments')}</li>
      
      % endif
      % if customer.customer_id:
        <li><hr></li>
        % for link_name in plugin_registry.category('customer_sidebar_link'):
          % if plugin_registry.is_applicable('customer_sidebar_link', link_name, request):
            <li><a href="${plugin_registry.getattr('customer_sidebar_link', link_name, 'href')}/${customer.customer_id}">${link_name}</a></li>
          % endif
        % endfor
        <li><hr></li>
        <li><a href="/crm/customer/new">New Customer</a></li>
      % endif
  </ul>
  % else:
    Create Customer...
  % endif
</div>
</%def>

