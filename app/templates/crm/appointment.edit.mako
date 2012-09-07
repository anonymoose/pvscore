
<%inherit file="appointment.base.mako"/>\

<div id="frm_appointment"> 
  % if not h.is_dialog():
  <h1>Edit Appointment</h1>
  % endif
  ${h.secure_form(h.url('/plugin/appointment/save'), id="appointment_form")}
  ${h.hidden('a_appointment_id', value=c.appointment.appointment_id)}
  ${h.hidden('a_customer_id', value=c.appointment.customer_id)}
  <div class="_50">
    <label for="title">Title</label>
    ${h.text('a_title', size=50, value=c.appointment.title)}
  </div>
  <div class="_50">
    <label for="phone">Phone</label>
    ${h.text('a_phone', size=20, value=c.appointment.phone)}
  </div>
  <div class="_100">
    <label for="description">Description</label>
    ${h.textarea('a_description', style="width: 100%; height: 100px;", content=c.appointment.description)}
  </div>
  <div class="_100">
    <table>
      <tr>
        <td><label for="start_dt">Date</label></td><td>${h.text('a_start_dt', size=10, value=c.appointment.start_dt)}</td>
        <td><label for="start_time">From</label></td><td>${h.select('a_start_time', c.appointment.start_time, c.hours)}</td>
        <td><label for="end_time">To</label></td><td>${h.select('a_end_time', c.appointment.end_time, c.hours)}</td>
      </tr>
    </table>
  </div>
          
  % if c.appointment.appointment_id:
  <div class="_50">
    <label for="create_dt">Created</label>
    ${h.nvl(c.appointment.create_dt)}
  </div>
  % endif

  % if not h.is_dialog():
  <div class="align-right">
    ${h.submit('submit', 'Submit', class_="form-button")}
  </div>
  % endif

  ${h.end_form()}
</div>


