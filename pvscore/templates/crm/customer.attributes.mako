
<%inherit file="customer.edit.base.mako"/>\

<h1>Customer Attributes</h1>

<div id="result_list">
  <table width="100%" class="sortable results table table-striped">
    <thead>
      <tr>
        <th>Name</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      % for attr_name in attrs:
      <tr>
        <td nowrap valign="top">${attr_name}</td>
        <td> ${attrs[attr_name]}</td>
      </tr>
      % endfor
    </tbody>
  </table>
</div>
