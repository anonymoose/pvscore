
<%inherit file="customer.edit.base.mako"/>\

<h1>Customer Attributes</h1>

<%
   attrs = c.customer.get_attrs()
   %>
<div id="result_list">
  <table width="100%" class="sortable">
    <thead>
      <tr>
        <th>Name</th>
        <th>Value</th>
      </tr>
    </thead>
    % for attr_name in attrs:
    <tr>
      <td nowrap valign="top">${attr_name}</td>
      <td> ${attrs[attr_name]}</td>
    </tr>
    % endfor
  </table>
</div>
