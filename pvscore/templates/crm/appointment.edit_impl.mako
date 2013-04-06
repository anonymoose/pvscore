

  <div class="container">
    <form id="frm_appointment" method="POST" action="/crm/appointment/save" autocomplete="off">
      ${h.hidden('appointment_id', value=appointment.appointment_id)}
      ${h.hidden('customer_id', value=appointment.customer_id)}
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="title">Title</label>
                ${h.text('title', class_="input-xlarge", value=appointment.title)}
              </div>
              <div class="span2">
                <label for="phone">Phone</label>
                ${h.text('phone', class_="input-small", value=appointment.phone)}
              </div>
              <div class="span2">
                <label for="public">&nbsp;</label>
                ${h.chkbox('public', checked=appointment.public, label='Show on Website?')}
              </div>
            </div>
            <div class="row">
              <div class="span9">
                <label for="description">Description</label>
                ${h.textarea('description', style="width: 90%; height: 100px;", content=appointment.description)}
              </div>
            </div>
            <div class="row">
              <div class="span2">
                <label for="start_dt">Date</label>
                ${h.text('start_dt', class_="input-small datepicker", autocomplete="off", value=appointment.start_dt if appointment.start_dt else (request.GET.get('dt') if request.GET.get('dt') else tomorrow))}
              </div>
              <div class="span2">
                <label for="start_time">From</label>
                ${h.select('start_time', appointment.start_time if appointment.start_time else '08:00', hours, class_="input-small")}
              </div>
              <div class="span2">
                <label for="end_time">To</label>
                ${h.select('end_time', appointment.end_time if appointment.end_time else '09:00', hours, class_="input-small")}
              </div>
              <div class="span2">
                <label for="timezone">Timezone</label>
                ${h.select('timezone', appointment.timezone if appointment.timezone else request.ctx.user.default_timezone, timezones)}
              </div>
            </div>
            % if appointment.start_dt:
            <div class="row">
              <div class="span2">
                <a href="/crm/appointment/day_view/${appointment.start_dt.year}/${appointment.start_dt.month}/${appointment.start_dt.day}"
                   class="btn btn-link">Show Day</a>
              </div>
              <div class="span2">
                <a href="/crm/appointment/month_view/${appointment.start_dt.year}/${appointment.start_dt.month}"
                   class="btn btn-link">Show Month</a>
              </div>
            </div>
            % endif
          </div>
          <div class="row">
            <div class="span2 offset8">
              <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
            </div>
          </div><!-- well -->
        </div>
      </div>
    </form>
  </div>
