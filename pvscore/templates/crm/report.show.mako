
<%inherit file="report.base.mako"/>\

<div class="container" id="rpt" style="height:900px;">
  <form id="frm_report">
    ${h.hidden('enterprise_id', value=enterprise_id)}
    ${h.hidden('report_id', value=report.report_id)}
    
    <div class="well">
      <div class="row">
        <div class="span8">
          <h3>${h.literal(report.description if report.description else report.name)}</h3>
        </div>
      </div>
      
      % if report.override:
      <div class="row">
        <div class="span8">
          <%include file="reports/${report.override}" />
        </div>
      </div>
      % else:
      <div class="row">
        <div class="span8">
          <table>
            <tr>
              % if report.show_start_dt:
              <td>Start</td><td>${h.text('rpt_start_dt', class_="input-small datepicker", value=rpt_start_dt if rpt_start_dt else thirty_ago)}</td>
              % endif
              % if report.show_end_dt:
              <td>End</td><td>${h.text('rpt_end_dt', class_="input-small datepicker", value=rpt_end_dt if rpt_end_dt else today)}</td>
              % endif
              % if report.show_campaign_id:
              <td>Campaign</td><td>${h.select('rpt_campaign_id', request.GET.get('rpt_campaign_id'), campaigns)}</td>
              % endif
              % if report.show_company_id:
              <td>Company</td><td>${h.select('rpt_company_id', request.GET.get('rpt_company_id'), companies)}</td>
              % endif
              % if report.show_user_id:
              <td>User</td><td>${h.select('rpt_user_id', request.GET.get('rpt_user_id'), users)}</td>
              % endif
              % if report.show_product_id:
              <td>Product</td><td>${h.select('rpt_product_id', request.GET.get('rpt_product_id'), products)}</td>
              % endif
              % if report.show_vendor_id:
              <td>Vendor</td><td>${h.select('rpt_vendor_id', request.GET.get('rpt_vendor_id'), vendors)}</td>
              % endif
              % if report.p0_name:
              <td>${report.p0_name}</td><td>${h.text('rpt_p0', size=20, value=request.GET.get('rpt_p0'))}</td>
              % endif
              % if report.p1_name:
              <td>${report.p1_name}</td><td>${h.text('rpt_p1', size=20, value=request.GET.get('rpt_p1'))}</td>
              % endif
              % if report.p2_name:
              <td>${report.p2_name}</td><td>${h.text('rpt_p2', size=20, value=request.GET.get('rpt_p2'))}</td>
              % endif
              <button type="button" onclick="report_refresh()" class="btn btn-primary btn-small">Refresh</button>
              <button type="button" onclick="report_export()" class="btn btn-primary btn-link">Export</button>
            <tr>
          </table>               
        </div>
      </div> 
      <div class="row">
        <div class="span8">
          
          ${h.hidden('column_model', value=report.column_model)}
          ${h.hidden('column_names', value=report.column_names)}
          ${h.hidden('on_dbl_click', value=report.on_dbl_click)}
          <br/>
          <br/>
          <div id="results_container"><table id="results"></table></div>
          <div id="pager_container"><div id="pager"></div></div>
          
          <script>
            var rpt_start_dt = '${request.GET.get('rpt_start_dt')}';
            var rpt_end_dt = '${request.GET.get('rpt_end_dt')}';
          </script>
        </div>
      </div>
      % endif
    </div>
  </form>
</div>


<%def name="draw_body()">\
${self.draw_body_no_left_col()}
</%def>
