<%!
from datetime import date, timedelta
import app.lib.util as util
import app.lib.db as db
from app.model.cms.site import Site

def f(val):
   return float(val if type(val) == str or type(val) == float or type(val) == int else 0)

def m(val):
   return util.money(val)

%>

<%
def rptquery(st, end, site):
    entid = site.company.enterprise_id
    return db.get_result_set(("cost", "revenue", "profit", "shipping", "handling"),
                 """select sum(oi.unit_cost*oi.quantity) as cost, 
                           sum(oi.unit_price*oi.quantity) as revenue,
                           sum((oi.unit_price*oi.quantity)-(oi.unit_cost*oi.quantity)) as profit,
                           sum(coalesce(o.shipping_total, 0)) as shipping,
                           sum(coalesce(o.handling_total, 0)) as handling
                    from 
                    crm_customer_order o, crm_customer cust, 
                    crm_order_item oi, crm_campaign cmp, 
                    crm_company co, core_status cs, core_status_event cse, crm_product p
                    where
                    o.customer_id = cust.customer_id and 
                    o.order_id = oi.order_id and 
                    o.campaign_id = cmp.campaign_id and
                    oi.product_id = p.product_id and
                    cmp.company_id = co.company_id and
                    co.enterprise_id = {entid} and
                    o.delete_dt is null and
                    oi.delete_dt is null and
                    o.status_id = cs.status_id and
                    cs.event_id = cse.event_id and
                    o.create_dt between '{st}' and '{end}'""".format(st=st,
                                                                     end=end,
                                                                     entid=entid))[0]

rpt_custom = is_custom = False
start_dt = request.GET.get('rpt_start_dt') 
end_dt = request.GET.get('rpt_end_dt')
site = Site.find_by_host(request.host)
if start_dt and end_dt:
   is_custom = True
   rpt_custom = rptquery(start_dt, end_dt, site)
else:
   today = date.today()
   first_day_of_month = util.get_first_day(today)
   first_day_of_year = date(today.year, 1, 1)
   rpt_month_to_day = rptquery(util.format_date(first_day_of_month), util.format_date(today), site)
   rpt_year_to_day = rptquery(util.format_date(first_day_of_year), util.format_date(today), site)
%>

<form method="GET" action="/crm/report/mobile/${c.report.report_id}">
  <table>
    <tr>
      <td>Start Date</td><td>${h.text('rpt_start_dt', size=10, value=request.GET.get('rpt_start_dt'))}</td>
      <td>End Date</td><td>${h.text('rpt_end_dt', size=10, value=request.GET.get('rpt_end_dt'))}</td>
      % if h.is_mobile():
      <td>${h.submit('refresh', 'Refresh')}</td>
      % else:
      <td>${h.button('refresh', 'Refresh', onclick='report_refresh();')}</td>
      % endif
    <tr>
  </table>
</form>
% if is_custom:
   <table>
     <tr>
       <td>
         ${self.drawit('%s through %s' % (start_dt, end_dt), rpt_custom)}
       </td>
       <td width="5%">&nbsp;</td>
     </tr>
   </table>
% else:
   <table>
     <tr>
       <td>
         ${self.drawit('Month To Date', rpt_month_to_day)}
       </td>
       <td width="5%">&nbsp;</td>
       <td>
         ${self.drawit('Year To Date', rpt_year_to_day)}
       </td>
     </tr>
   </table>
% endif

<%def name="drawit(title, rpt)">
<h3>${title}</h3>
<table border="0" style="border:1px solid black;" cellspacing="1" cellpadding="1">
<tr><td>Ordinary Income/Expense</td><td></td><td></td></tr>
<tr><td></td><td>Merchandise</td><td align="right"> ${m(f(rpt.revenue))}</td></tr>
<tr><td></td><td>Shipping and Handling</td><td align="right">${m(f(rpt.shipping) + f(rpt.handling))}</td></tr>
<tr><td></td><td>Total Sales</td><td align="right">${m(f(rpt.revenue) + f(rpt.shipping) + f(rpt.handling))}</td></tr>
<tr><td></td><td>Total Income</td><td align="right">${m(f(rpt.revenue) + f(rpt.shipping) + f(rpt.handling))}</td></tr>
<tr><td>Cost of Goods Sold</td><td></td><td></td></tr>
<tr><td></td><td>Cost of Goods Sold</td><td align="right"> ${m(f(rpt.cost))}</td></tr>
<tr><td></td><td>Gross Profit</td><td align="right"> ${m((f(rpt.revenue) + f(rpt.shipping) + f(rpt.handling)) - f(rpt.cost))}</td></tr>
<tr><td></td><td>Net Ordinary Income</td><td align="right"> ${m((f(rpt.revenue) + f(rpt.shipping) + f(rpt.handling)) - f(rpt.cost))}</td></tr>
<tr><td>Other Income</td><td></td><td></td></tr>
<tr><td></td><td>Discounts</td><td align="right"> 0</td></tr>
<tr><td></td><td>Total Other Income</td><td align="right"> 0</td></tr>
<tr><td></td><td>Net Other Income</td><td align="right"> 0</td></tr>
<tr><td></td><td>Net Income</td><td align="right"> ${m((f(rpt.revenue) + f(rpt.shipping) + f(rpt.handling)) - f(rpt.cost))}</td></tr>
</table>
</%def>

