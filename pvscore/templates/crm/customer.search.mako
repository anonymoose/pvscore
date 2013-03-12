

<%inherit file="customer.base.mako"/>\

<div>
  <form method="POST" id="frm_customer_search" action="/crm/customer/search">
    <h1>Customer Search</h1>
    <div class="container">
      <div class="row">
        <div class="span11">
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="fname">First Name</label>
                ${h.text('fname', size=50, value=fname)}
              </div>
              <div class="span3">
                <label for="lname">Last Name</label>
                ${h.text('lname', size=50, value=lname)}
              </div>
              <div class="span3">
                <label for="email">Email Address</label>
                ${h.text('email', size=50, value=email)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="company_name">Company Name</label>
                ${h.text('company_name', size=50, value=company_name)}
              </div>
              <div class="span3">
                <label for="phone">Phone</label>
                ${h.text('phone', size=50, value=phone)}
              </div>
              <div class="span3">
                <label for="user_assigned">Assigned To</label>
                ${h.select('user_assigned', user_assigned, users)}
              </div>
            </div>
          </div>
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

% if customers:
<div id="result_list">
  <table class="results sortable table table-striped">
    <thead>
      <tr>
        <td>Email</td>
        <td>First</td>
        <td>Last</td>
        <td>Phone</td>
        <td>Company</td>
        <td>Created</td>        
      </tr>
    </thead>
    <tbody>
      % for cust in customers:
      <tr>
        <td>${h.link_to(cust.email if cust.email else '*no email*', '/crm/customer/edit/%s' % cust.customer_id)}</td>
        <td>${cust.fname}</td>
        <td>${cust.lname}</td>
        <td>${cust.phone}</td>
        <td>${cust.company_name}</td>
        <td nowrap>${h.words_date_time(cust.create_dt)}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

