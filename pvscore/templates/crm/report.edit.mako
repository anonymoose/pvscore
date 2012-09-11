
<%inherit file="report.base.mako"/>\

<div style="height:1500px;"> 
  <h1>Edit Report</h1>
  <div class="container">
    
    <form id="frm_report" action="/crm/report/save" method="POST">
      ${h.hidden('report_id', value=report.report_id)}
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=report.name)}
          </div>
          <div class="span3">
            <label for="description">Description</label>
            ${h.text('description', size=50, value=report.description)}
          </div>
        </div>
        <div class="row">
          <div class="span8">
            <label for="sql">SQL</label>
            <div style="border: 1px solid #cccccc;">
              ${h.textarea('sql', content=report.sql)}
            </div>
          </div>
        </div>
        <div class="row">
          <div class="span3">
            <label for="override">Override</label>
            ${h.text('override', size=50, value=report.override)}
          </div>
          <div class="span3">
            <label for="company_id">Companies</label>
            ${h.select('company_id', None, companies, multiple=True)}
          </div>
        </div>
        <div class="row">
          <div class="span3">
            ${h.checkbox('show_start_dt', checked=report.show_start_dt, label=' Show Start Dt')}
            ${h.checkbox('show_end_dt', checked=report.show_end_dt, label=' Show End Dt')}
          </div>
          <div class="span3">
            ${h.checkbox('show_campaign_id', checked=report.show_campaign_id, label=' Show Campaign List')}
            ${h.checkbox('show_company_id', checked=report.show_company_id, label=' Show Company List')}
          </div>
          <div class="span3">
            ${h.checkbox('show_user_id', checked=report.show_user_id, label=' Show User List')}
            ${h.checkbox('show_product_id', checked=report.show_product_id, label=' Show Product List')}
          </div>
          <div class="span2">
            ${h.checkbox('show_vendor_id', checked=report.show_vendor_id, label=' Show Vendor List')}
            ${h.checkbox('is_vendor', checked=report.is_vendor, label=' Is Vendor Report?')}
          </div>
        </div>
        <div class="row">
          <div class="span3">
            <label for="p0_name">String P0 Text</label>
            ${h.text('p0_name', size=50, value=report.p0_name)}
          </div>
          <div class="span3">
            <label for="p1_name">String P1 Text</label>
            ${h.text('p1_name', size=50, value=report.p1_name)}
          </div>
          <div class="span3">
            <label for="p2_name">String P2 Text</label>
            ${h.text('p2_name', size=50, value=report.p2_name)}
          </div>
        </div>
        <div class="row">
          <div class="span8">
            <label for="column_names">Column Names</label>
            <div style="border: 1px solid #cccccc;">
              ${h.textarea('column_names', content=report.column_names)}
            </div>
          </div>
        </div>
        <div class="row">
          <div class="span8">
            <label for="column_model">Column Model</label>
            <div style="border: 1px solid #cccccc;">
              ${h.textarea('column_model', content=report.column_model)}
            </div>
          </div>
        </div>
        <div class="row">
          <div class="span8">
            <label for="on_dbl_click">On Double Click</label>
            <div style="border: 1px solid #cccccc;">
              ${h.textarea('on_dbl_click', content=report.on_dbl_click)}
            </div>
          </div>
        </div>
        <div class="row">
          <div class="span2 offset10">
            <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>





