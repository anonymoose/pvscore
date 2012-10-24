<%inherit file="purchase.base.mako"/>\

<div> 
  <h1>Purchase Order Search</h1>
  <div class="container">
    <form id="frm_purchase_search" action="/crm/purchase/search" method="POST">
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="from_dt">From Date</label>
            ${h.text('from_dt', size=10)}
          </div>
          <div class="span3">
            <label for="to_dt">To Date</label>
            ${h.text('to_dt', size=10)}
          </div>
          <div class="span2">
            <label for="vendor_id">Vendor</label>
            ${h.select('vendor_id', None, vendors)}
          </div>
        </div>
        <div class="row">
          <div class="span2 offset10">
            <input type="submit" name="submit" class="btn btn-primary btn-large" value="Search"/>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>

% if purchases:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <td>Name</td>        
        <td>Created</td>
        <td>Total</td>
      </tr>
    </thead>
    <tbody>
      % for po in purchases:
      <tr>
        <td nowrap>${h.link_to(po.vendor.name, '/crm/purchase/edit/%s' % po.purchase_order_id)}</td>
        <td nowrap>${po.create_dt}</td>
        <td>${po.total()}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

<%def name="draw_body()">\
${self.draw_body_no_right_col()}
</%def>
