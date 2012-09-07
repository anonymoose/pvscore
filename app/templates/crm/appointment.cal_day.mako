
<%inherit file="appointment.base.mako"/>\

<p>
<span>
<b><a href="/plugin/appointment/day_view/${c.yesterday.year}/${c.yesterday.month}/${c.yesterday.day}">&lt;&lt;</a></b>
 | <b>${c.today.year}-${c.today.month}-${c.today.day}</b> | 
<b><a href="/plugin/appointment/day_view/${c.tomorrow.year}/${c.tomorrow.month}/${c.tomorrow.day}">&gt;&gt;</a></b>
</span>
</p>
<hr>

<div id="div_calendar" style="width: 100%;">
${h.literal(c.cal_content)}
</div>
