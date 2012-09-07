
<%inherit file="appointment.base.mako"/>\

<div class="container">
  <div class="row">
    <div class="span9">

<span>
<b><a href="/crm/appointment/month_view/${last_month.year}/${last_month.month}">&lt;&lt;</a></b>
 | <b>${month_name} ${year}</b> | 
<b><a href="/crm/appointment/month_view/${next_month.year}/${next_month.month}">&gt;&gt;</a></b>
</span>
</p>
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
        <td class="${'weekend' if day_of_week in (0, 6) else 'weekday'}" id="day_${month_cal[w][day_of_week]}">
          <a href="/crm/appointment/day_view/${year}/${month}/${month_cal[w][day_of_week]}">${month_cal[w][day_of_week]}</a>
          <img src="/static/icons/silk/add.png" border="0" onclick="appointment_edit(null, ${year}, ${month}, ${month_cal[w][day_of_week]})"/>
          <div class="${'weekend' if day_of_week in (0,6) else 'weekday'}">
            % for a in appointments:
            % if a.start_dt == month_cal[w][day_of_week]:
            <a href="javascript:appointment_edit(${a.appointment_id})">${a.start_time} - ${a.end_time} <b>${a.title}</b></a><br>
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
