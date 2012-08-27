${h.javascript_link('/public/js/jquery-1.4.2/core/jquery-1.4.2.js')}
${h.javascript_link('/public/js/jquery-current/barcode.2.0.2/jquery-barcode-2.0.2.min.js')}
${h.javascript_link('/public/js/pvs/pvs-jquery.js')}
${h.javascript_link('/public/crm/js/product.js')}

<html>
<body>

<table width="100%" >
<tr>
% for i,p in enumerate(c.products):
  <td width="50%">
    <table width="100%" >
      <tr>
        <td valign="top">
          <canvas id="barcode_${p.product_id}" width="175" height="175"></canvas> 
          <script>
            product_gen_barcode_impl('${p.product_id}', '#barcode_${p.product_id}');
          </script>
        </td>
        <td valign="top">
          <p>
            <h2>${p.vendor.name if p.vendor else ''}</h2>
          </p>
          <p>
          <b>${p.name} <font color="red">$${h.money(p.get_default_unit_price())}</font></b>
          </p>
        </td>
      </tr>
    </table>
  </td>
  % if ((i+1) % 2) == 0:
    </tr><tr>
  % endif
  % if i and (((i+1) % 8) == 0):
    </table>
<br><br>
    <table width="100%" >
      <tr>
  % endif
% endfor
</tr>

</body>
</html>
