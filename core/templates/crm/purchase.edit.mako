
<%inherit file="purchase.base.mako"/>\

<%def name="left_col()">
% if purchase.purchase_order_id:
<div class="well sidebar-nav">
  <ul class="nav nav-list">
    % if not purchase.complete_dt:
    <li>${h.link_to('Complete', 'javascript:purchase_complete()')}</li>
    % endif
    
    % if len(events) > 0:
    <li><a href="#dlg_purchase_status" role="button" data-toggle="modal">Status</a></li>
    % endif
    <li>${h.link_to('History', 'javascript:purchase_show_history()', id='link_history')}</li>
  </ul>
</div>
% endif
</%def>

<div style="height:1000px">
  <div class="container">
    <div class="row">
      <div class="span4">
        <h1>Edit Supplier Order</h1>
      </div>
      <div class="span5">
        <h1><font color="green">${'Completed: %s' % purchase.complete_dt if purchase.complete_dt else ''}</font></h1>
      </div>
    </div>
    <div class="row">
    <div class="span9">
    <form action="/crm/purchase/save" method="POST" id="frm_purchase">
      ${h.hidden('purchase_order_id', value=purchase.purchase_order_id)}
      <div class="well"> 
        <h3>General Information</h3>
        <div class="row">
          <div class="span3">
            <div class="row">
              <div class="span3">
                <label for="vendor_id">Supplier</label>
                ${h.select('vendor_id', purchase.vendor_id, vendors)}
              </div>
              <div class="span3">
                <label for="company_id">Company</label>
                ${h.select('company_id', purchase.company_id, companies)}
              </div>
            </div>
            <div class="row">
              <div class="span3">
                <label for="shipping_cost">Shipping Cost</label>
                ${h.text('shipping_cost', value=h.money(purchase.shipping_cost))}
              </div>
              <div class="span3">
                <label for="tax_cost">Tax</label>
                ${h.text('tax_cost', value=h.money(purchase.tax_cost))}
              </div>
            </div>
          </div>
          <div class="span4">
            <div class="row">
              <div class="span4">
                <label for="note">Note</label>
                ${h.textarea('note', purchase.note, style="width: 100%; height: 200px;")}
              </div>
            </div>
          </div> 
        </div>
      </div>
    </form> 
    % if purchase.purchase_order_id:
    <h3>Edit Purchased Items</h3>
    <div class="well">
      <div class="row">
        <div class="span8">
          % if purchase.purchase_order_id:
          <form id="frm_order_item">
            <div id="result_list">
              <table id="po_items">
                <thead>
                  <tr>
                    <td>&nbsp;</td>                  
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Quantity</th>
                    <th>Rate</th>
                    <th>Amount</th>
                  </tr>
                </thead>
                % if not purchase.complete_dt:
                <tr>
                  <td>&nbsp;</td>
                  <td>&nbsp;</td>
                  <td>
                    <img src="/static/icons/silk/star.png" title="Accept" alt="Accept" class="clickable" border="0" onclick="purchase_accept_order_item()">
                  </td>
                  <td>
                    <input name="prod_complete" type="text"
                           placeholder="Product Search" 
                           id="prod_complete" data-provide="typeahead" data-source="[]" maxlength="30" autocomplete="off"/>
                    <input type="hidden" name="order_item_id" id="order_item_id" value=""/>
                    <input type="hidden" name="product_id" id="product_id" value=""/>
                  </td>
                  <td>${h.text('order_note', class_="input-small")}</td>
                  <td>${h.text('quantity', class_="input-small")}</td>
                  <td>${h.text('unit_cost', class_="input-small")}</td>
                  <td>${h.text('amount', class_="input-small", disabled=True)}</td>
                </tr>
                % endif
                % for poi in purchase.order_items:
                <tr>
                  % if not purchase.complete_dt and not poi.complete_dt:
                  <td><img src="/static/icons/silk/accept.png" class="clickable" title="Complete" alt="Complete" border="0" onclick="purchase_complete_order_item(this, ${poi.order_item_id})"></td>
                  <td><img src="/static/icons/silk/delete.png" class="clickable" title="Delete" alt="Delete" border="0" onclick="purchase_delete_order_item(this, ${poi.order_item_id})"></td>
                  <td><img src="/static/icons/silk/page_edit.png" class="clickable" title="Edit" alt="Edit" border="0" onclick="purchase_edit_order_item(this, ${poi.order_item_id})"></td>
                  % elif poi.complete_dt:
                  <td>&nbsp;</td> 
                  <td>&nbsp;</td>
                  <td>&nbsp;</td> 
                  % endif
                  <td nowrap>${poi.product.name}</td>
                  <td nowrap>${poi.note}</td>
                  <td>${poi.quantity}</td>
                  <td>${h.money(poi.unit_cost)}</td>
                  <td>${h.money(poi.total())}</td>
                </tr>
                % endfor
              </table>
            </div>
          </form>
        </div>
        % endif
      </div>
    </div>
    % endif
    
    % if not purchase.complete_dt:
    <div class="row">
      <div class="span2 offset8">
        <input type="button" name="submit" onclick="$('#frm_purchase').submit()" class="btn btn-primary btn-large" value="Save"/>
      </div>
    </div>
    % endif
  </div>
  <br>
  <div id="div_purchase_detail">
  </div>
</div>

<!-- Modals -->
<div class="modal hide fade" id="dlg_purchase_status">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
    <h3>Purchase Status</h3>
  </div>
  <div class="modal-body">
    <form id="frm_status" action="/crm/purchase/save_status/${purchase.purchase_order_id}" method="POST"> 
      <div class="row">
        <div class="span5">
          <label for="event_id">Event</label>
          ${h.select('event_id', None, events)}
        </div>
      </div>
      <div class="row">
        <div class="span5">
          <label for="note">Note</label>
          ${h.textarea('note', rows=10, style="width: 100%; height: 100px;", class_='content_editor')}
        </div>
      </div>
    </form>
  </div>
  <div class="modal-footer">
    <button class="btn btn-primary" onclick="$('#frm_status').submit()">Save changes</button>
    <button class="btn btn-link" data-dismiss="modal" aria-hidden="true">Cancel</button>
  </div>
</div>
