
<%inherit file="appointment.base.mako"/>\

<div> 
  % if appointment.appointment_id:
  <h1>Edit Appointment</h1>
  % else:
  <h1>New Appointment</h1>
  % endif
  <%include file="appointment.edit_impl.mako"/>
</div>


