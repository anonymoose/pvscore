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
  <div class="well sidebar-nav">
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
    <li>${h.link_to('Edit Customer', '/crm/customer/edit/%s' % customer.customer_id, id='link_edit')}</li>
    <li><hr></li>
    % endif
    % if customer.customer_id:
      <li><b>${h.link_to('Orders', '/crm/customer/show_orders/%s' % customer.customer_id, id='link_orders')}</b></li>
      % if request.ctx.user.priv.add_customer_order:
        <li>${h.link_to('Add Order', '/crm/customer/add_order_dialog/%s' % customer.customer_id, id='link_add_order')}</li>
      % endif
      % if request.ctx.user.priv.add_customer_billing:
        <!--li>${h.link_to('Billing Method', 'javascript:customer_edit_billing_method()', id='link_add_billing')}</li-->
      % endif
      % if request.ctx.user.priv.send_customer_emails:
        <li>${h.link_to('Communication', 'javascript:customer_send_email()', id='link_send_email')}</li>
      % endif
      % if request.ctx.user.priv.edit_customer:
        <li>${h.link_to('Status', 'javascript:customer_status()', id='link_status')}</li>
      % endif

        <li>${h.link_to('Add Appt', 'javascript:customer_edit_appointment()', id='link_add_appointment')}</li>

      <li>${h.link_to('History', '/crm/customer/show_history/%s' % customer.customer_id, id='link_history')}</li>
      % if request.ctx.user.priv.add_customer_billing:
        <li>${h.link_to('Billing', '/crm/customer/show_billings/%s' % customer.customer_id, id='link_billings')}</li>
      % endif
        <li>${h.link_to('Attributes', '/crm/customer/show_attributes/%s' % customer.customer_id, id='link_attr')}</li>

        <li>${h.link_to('Appointments', '/plugin/appointment/show_appointments/%s' % customer.customer_id, id='link_appointments')}</li>

    % endif
    % if customer.customer_id:
    <li><hr></li>
    <li><a href="/crm/customer/new">New Customer</a></li>
    % endif
  </ul>
</div>
</%def>

