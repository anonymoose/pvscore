
<%inherit file="appointment.base.mako"/>\
<%
c.title = (c.title if hasattr(c, 'title') else '')
c.description = (c.description if hasattr(c, 'description') else '')
%>
<p>
<h3>Appointment Search</h3>
<strong>Use full or partial matching on any/all fields to find appointments.  Values are combined to narrow results.</strong>
</p>
<hr>
<table>
  <tr valign="top">
    <td>
      <div id="frm_appointment_search"> 
        ${h.secure_form(h.url('/plugin/appointment/search'))}
        <table>
          <div class="_50">
            <label for="title">Title</label>
            ${h.text('title', size=50, value=c.title)}
          </div>
          <div class="_50">
            <label for="description">Description</label>
            ${h.text('description', size=50, value=c.description)}
          </div>
          <div class="align-right">
            ${h.submit('search', 'Search', class_="form-button")}
          </div>
        </table>
        ${h.end_form()}
      </div>
    </td>
    <td>
      % if hasattr(c, 'appointments'):
      <div id="result_list">
        <table class="results">
          % for a in c.appointments:
          <tr>
            <td nowrap>${h.link_to(a.title, '/plugin/appointment/edit/%d' % a.appointment_id)}</td>
            <td nowrap>${a.create_dt}</td>
          </tr>
          % endfor
        </table>
      </div>
      % endif
    </td>
  </tr>
</table>

