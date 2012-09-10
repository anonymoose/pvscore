
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
        <table id="" class="table table-striped table-condensed"> 
          <tbody>
            % for hr in hours_list[14:43]:
            <tr>
              <td>${hr[1]}</td>
              <td>
                <table>
                    <tr>
                    % for i,a in enumerate(appointments):
                      % if a.start_time == hr[0]:
                        <td>
                        % if a.customer_id:
                          <a href="/crm/appointment/edit_for_customer/${a.customer_id}/${a.appointment_id}">
                        % else:
                          <a href="/crm/appointment/edit/${a.appointment_id}">
                        % endif
                        <b>${a.title} ${h.nvl(a.phone)}</b>
                        </a>
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
