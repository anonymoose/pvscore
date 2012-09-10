
<%inherit file="appointment.base.mako"/>\

<div class="container">
  <div class="row">
    <div class="span9">
      
      <ul class="pager">
        <li class="previous">
          <a href="/crm/appointment/month_view/${last_month.year}/${last_month.month}">&larr; prev</a> <!-- " -->
        </li>
        <li>${month_name} ${year}</li>
        <li class="next">
          <a href="/crm/appointment/month_view/${next_month.year}/${next_month.month}">next &rarr;</a>
        </li>
      </ul>
      
      <hr>
      
      <div id="div_calendar" style="width: 100%;">
        <table id="calendar" > 
          <thead> 
            <tr> 
              <th class="weekend">Sunday</th> 
              <th>Monday</th> 
              <th>Tuesday</th> 
              <th>Wednesday</th>
              <th>Thursday</th>
              <th>Friday</th>
              <th class="weekend">Saturday</th>
            </tr> 
          </thead> 
          <tbody> 
            % for w in range(0, len(month_cal)): 
            <tr>
              % for day_of_week in xrange(0,7): 
              <td class="${'weekend' if day_of_week in (0, 6) else 'weekday'} ${'today' if year == today.year and month == today.month and month_cal[w][day_of_week] == today.day else ''}" 
                  id="day_${month_cal[w][day_of_week]}">
                % if month_cal[w][day_of_week] > 0:
                <a href="/crm/appointment/day_view/${year}/${month}/${month_cal[w][day_of_week]}">${month_cal[w][day_of_week]}</a>
                <a href="/crm/appointment/new?dt=${year}-${month}-${month_cal[w][day_of_week]}">
                  <img src="/static/icons/silk/add.png" border="0"/></a>
                % endif
                <div class="${'weekend' if day_of_week in (0,6) else 'weekday'}">
                  % for a in appointments:
                  % if a.start_dt.year == year and a.start_dt.month == month and a.start_dt.day == month_cal[w][day_of_week]:
                  % if a.customer_id:
                  <a href="/crm/appointment/edit_for_customer/${a.customer_id}/${a.appointment_id}">
                    % else:
                    <a href="/crm/appointment/edit/${a.appointment_id}">
                      % endif
                      ${a.start_time} ${a.title[0:10]}...</a><br/>
                    % endif
                    % endfor
                </div>
              </td>
              % endfor
            </tr>
            % endfor
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
      
      
