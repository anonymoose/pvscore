
<%inherit file="customer.edit.base.mako"/>\

<div>
  <div class="container">
    <form id="frm_customer" method="POST" action="/crm/customer/save">
      ${h.hidden('customer_id', value=customer.customer_id)}
      <div class="row">
        <div class="span4">
          % if customer.customer_id:
          <h1>Edit Customer</h1>
          % else:
          <h1>New Customer</h1>
          % endif
        </div>
        % if customer.phase:
        <div class="span6" style="text-align: center; background-color:${customer.phase.color};">
          <h1>Phase: ${customer.phase.display_name}</h1>
        </div>
        % endif
      </div>
      <div class="row">
        <div class="span9">
          <div class="well">
            <div class="row">
              <div class="span2">
                <label for="fname">First Name</label>
                ${h.text('fname', class_="input-small", value=customer.fname)}
              </div>
              <div class="span2">
                <label for="lname">Last Name</label>
                ${h.text('lname', class_="input-small", value=customer.lname)}
              </div>
              <div class="span2 offset1">
                <label for="phase_id">Customer Phase</label>
                ${h.select('phase_id', str(customer.phase_id), phases)}
              </div>
            </div>
            <div class="row">
              <div class="span2">
                <label for="email">Email</label>
                ${h.text('email', class_="input-small", value=customer.email)}
              </div>
              <div class="span2">
                <label for="password">Password</label>
                ${h.password('password', class_="input-small", value=customer.password)}
              </div>
              <div class="span2 offset1">
                <label for="balance">Balance</label>
                ${h.text('balance', size=10, value=h.money(customer.get_current_balance()), disabled=True)}
              </div>
            </div>
            <div class="row">
              <div class="span2">
                <label for="user_assigned">Assigned To</label>
                ${h.select('user_assigned', str(customer.user_assigned), users)}
              </div>
              <div class="span2 offset3">
                <label for="campaign_id">Campaign</label>
                ${h.select('campaign_id', str(customer.campaign.campaign_id), campaigns)}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="span9">
          <h3>Address and Phone</h3>
          <div class="well">
            <div class="row">
              <div class="span3">
                <label for="addr1">Address</label>
                ${h.text('addr1', value=customer.addr1)}
                ${h.text('addr2', value=customer.addr2)}

                <label for="city">City</label>
                ${h.text('city', class_="input-medium", value=customer.city)}

                <label for="state">State</label>
                ${h.text('state', class_="input-small", value=customer.state)}

                <label for="zip">Zip</label>
                ${h.text('zip', class_="input-small", value=customer.zip)}
              </div>

              <div class="span2">
                <label for="phone">Phone</label>
                ${h.text('phone', class_="input-small", value=customer.phone)}


                <label for="alt_phone">Alternate Phone</label>
                ${h.text('alt_phone', class_="input-small", value=customer.alt_phone)}


                <label for="fax">Fax</label>
                ${h.text('fax', class_="input-small", value=customer.fax)}


                <label for="country">Country</label>
                <select id="country" name="country">
                  ${self.country_list()}
                </select>
              </div>


              <div class="span2">
                <label for="title">Title</label>
                ${h.text('title', value=customer.title)}

                <label for="company_name">Company Name</label>
                ${h.text('company_name', value=customer.company_name)}

              </div>
            </div>
            <div class="row">
              <div class="span9">
                <label for="notes">Notes</label>
                ${h.textarea('notes', customer.notes, style="width: 90%; height: 120px;")}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="span6">
          <h3>Customer Attributes</h3>
          <table>
            <%
               attrs = customer.get_attrs()
               idx = 0
               %>
            % for attr_name in attrs:
            <tr>
              <td>${h.text('attr_name[%d]' % idx, class_="input-small", value=attr_name)}</td><td>${h.text('attr_value[%d]' % idx, size=30, value=attrs[attr_name])}</td>
            </tr>
            <% idx = idx + 1 %>
            % endfor
            % for i in range(idx,10):
            <tr>
              <td>${h.text('attr_name[%d]' % i, class_="input-medium")}</td><td>${h.text('attr_value[%d]' % i, class_="input-medium")}</td>
            </tr>
            <% idx = idx + 1 %>
            % endfor
          </table>
        </div>
      </div>

      % if request.ctx.user.priv.edit_customer:
      <div class="row">
        <div class="span3 offset7">
          <input type="submit" name="submit" class="btn btn-primary btn-large" value="Save"/>
          % if customer.customer_id:
          <button class="btn btn-warning btn-large" onclick="customer_delete()">Delete</button>
          % endif
        </div>
      </div>
      % endif

      % if customer.customer_id:
      <div class="span4">
        <table>
          <tr><td>Created&nbsp;</td><td>${h.nvl(h.date_time(customer.create_dt))}</td></tr>
          <tr><td>Modified&nbsp;</td><td>${h.nvl(h.date_time(customer.mod_dt))}</td></tr>
          <tr><td>Deleted&nbsp;</td><td>${h.nvl(h.date_time(customer.delete_dt))}</td></tr>
        </table>
      </div>
      % endif
    </form>
  </div>
</div>



