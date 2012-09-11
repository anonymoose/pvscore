
<%inherit file="purchase.base.mako"/>\

<h1>Vendor List</h1>

% if vendors:
<div id="result_list">
  <table width="100%" class="results sortable table table-striped">
    <thead>
      <tr>
        <td>ID</td>
        <td>Name</td>
        <td>Created</td>
      </tr>
    </thead>
    <tbody>
      % for v in vendors:
      <tr>
        <td>${v.vendor_id}</td>
        <td>${h.link_to(v.name, '/crm/purchase/vendor/edit/%d' % v.vendor_id)}</td>
        <td nowrap>${v.create_dt}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
% endif

