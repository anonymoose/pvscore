
<%inherit file="appointment.base.mako"/>\

<div>
  <form method="POST" id="frm_appointment_search" action="/crm/appointment/search">
    <h1>Appointment Search</h1>
    <div class="container">
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="fname">Title</label>
                ${h.text('title', value=title)}
              </div>
              <div class="span3">
                <label for="lname">Description</label>
                ${h.text('description', value=description)}
              </div>
            </div>
          </div>        
        </div>
      </div>
      <div class="row">
        <div class="span2 offset8">
          <input type="submit" name="submit" class="btn btn-primary btn-large" value="Search"/>
        </div>
      </div>
    </div>
  </form>
</div>

% if appointments:
<div id="result_list">
  <table class="results sortable table table-striped">
    <thead>
      <tr>
        <td>Description</td>        
        <td>Appointment Date</td>
      </tr>
    </thead>
    <tbody>
      % for app in appointments:
      <tr>
        % if app.customer_id:
          <td nowrap><a href="/crm/appointment/edit_for_customer/${app.customer_id}/${app.appointment_id}">${app.title}</a></td>
        % else:
          <td nowrap><a href="/crm/appointment/edit/${app.appointment_id}">${app.title}</a></td>
        % endif
        <td nowrap>${app.start_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

