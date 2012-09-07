
<%inherit file="appointment.base.mako"/>\

<p>
<span>
<b><a href="/plugin/appointment/month_view/${c.last_month.year}/${c.last_month.month}">&lt;&lt;</a></b>
 | <b>${c.month_name} ${c.year}</b> | 
<b><a href="/plugin/appointment/month_view/${c.next_month.year}/${c.next_month.month}">&gt;&gt;</a></b>
</span>
</p>
<hr>

<div id="div_calendar" style="width: 100%;">
${h.literal(c.cal_content)}
</div>
