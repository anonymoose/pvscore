
<%inherit file="appointment.base.mako"/>\

<div class="container">
  <div class="row">
    <div class="span9">
      <ul class="pager">
        <li class="previous">
          <a href="/crm/appointment/day_view/${yesterday.year}/${yesterday.month}/${yesterday.day}">&larr; prev</a> <!-- " -->
        </li>
        <li>${h.words_date(today)}</li>
        <li class="next">
          <a href="/crm/appointment/day_view/${tomorrow.year}/${tomorrow.month}/${tomorrow.day}">next &rarr;</a>
        </li>
      </ul>

      <hr/>
      
      <div id="div_calendar" style="width: 100%;">
        <table id="day_calendar" class="table table-striped table-condensed"> 
          <tbody>
            % for hr in hours_list:
            <tr>
              <td class="timeslot" style="">${hr[1]}</td>
              <td class="timeslot">
                <table>
                  <tr>
                    % for a in appointments:
                    % if a.start_time == hr[0]:
                    <td class="timeslot_appt">
                      <a href="javascript:appointment_edit(${a.appointment_id})"><b>${a.title} ${a.phone}</b></a>
                    </td>
                    % endif
                    % endfor
                  </tr>
                </table>
              </td>
            </tr>
            % endfor
          </tbody> 
        </table> 
      </div>
    </div>
  </div>
</div>
