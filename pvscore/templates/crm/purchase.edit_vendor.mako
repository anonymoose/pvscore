
<%inherit file="purchase.base.mako"/>\

<div> 
  <h1>Edit Vendor</h1>
  <div class="container">
    <form id="frm_vendor" action="/crm/purchase/vendor/save" method="POST">
      ${h.hidden('vendor_id', value=vendor.vendor_id)}
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="name">Name</label>
            ${h.text('name', size=50, value=vendor.name)}
          </div>
          <div class="span3">
            <label for="email">Email</label>
            ${h.text('email', size=50, value=vendor.email)}
          </div>
          <div class="span3">
            <label for="url">Url</label>
            ${h.text('url', size=50, value=vendor.url)}
          </div>
        </div>
      </div>

      <h3>Address and Phone</h3>
      <div class="well">
        <div class="row">
          <div class="span3">
            <label for="addr1">Address</label>
            ${h.text('addr1', size=50, value=vendor.addr1)}
            ${h.text('addr2', size=50, value=vendor.addr2)}
          
            <label for="city">City</label>
            ${h.text('city', size=50, value=vendor.city)}

            <label for="state">State</label>
            ${h.text('state', size=50, value=vendor.state)}

            <label for="zip">Zip</label>
            ${h.text('zip', size=50, value=vendor.zip)}
          </div>

          <div class="span3">
            <label for="phone">Phone</label>
            ${h.text('phone', size=20, value=vendor.phone)}
          </div>
          <div class="span3">
            <label for="alt_phone">Alternate Phone</label>
            ${h.text('alt_phone', size=20, value=vendor.alt_phone)}
          </div>
          <div class="span3">
            <label for="fax">Fax</label>
            ${h.text('fax', size=20, value=vendor.fax)}
          </div>
          <div class="span3">
            <label for="country">Country</label>
            <select id="country" name="country">
              ${self.country_list()}
            </select>
          </div>
        </div>
      </div>

      <h3>Miscellaneous</h3>
      <div class="well">      
        <div class="row">
          <div class="span3">
            <label for="note">Notes</label>
            ${h.textarea('note', vendor.note, style="width: 100%; height: 200px;")}
          </div>
          <div class="span3">
            <label for="revshare">Revenue Share</label>
            ${h.text('revshare', size=20, value=vendor.revshare)}
          </div>
          <div class="span2">
            ${h.checkbox('send_month_end_report', checked=vendor.send_month_end_report, label=' Send Month End Report')}
          </div>
        </div>    
      </div>
      <div class="row">
        <div class="span2 offset10">
          <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
        </div>
      </div>
    </form>
  </div>
</div>


